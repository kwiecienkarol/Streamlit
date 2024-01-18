import streamlit as st
import pandas as pd
import time
import datetime
import os
# from tkinter import filedialog
# import tkinter as tk
import numpy as np
from openpyxl import load_workbook
import io

today=datetime.datetime.today().strftime("%d.%m.%Y")

st.title('HUAWEI')
st.markdown('[Huawei Sharpoint](https://arrowelectronics.sharepoint.com/:f:/r/sites/EMEAProductCatalog/Shared%20Documents/A%20-%20Price%20Catalog/D%20-%20H/HUAWEI?csf=1&web=1&e=mkQgMK/) ')

st.markdown('------------------------------------------------------------------')

id=st.selectbox(':small_blue_diamond: Your name - ID',('Karol Kwiecień - A86227','Katarzyna Czyż - A86361', 'Emil Twardowski - A93176', 'Chistian Gay - A60276','Paweł Czaja - A89264', 'Hanna Źródlewska - 132693', 'Karmen Bautembach - 136182'),index=None,placeholder="Select your name")

if id is not None:
    # st.write(id[-6:])
    number_id = id[-6:]

st.markdown('------------------------------------------------------------------')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])


st.markdown('------------------------------------------------------------------')

# adding Iasset table
iasset_data = {'iAsset': [], 'No': []}
iasset = pd.DataFrame(iasset_data)


# ------------------------------------  TAR  -----------------------------------
st.markdown('### :small_blue_diamond:  TAR file ###')

col1, col2 = st.columns(2)
with col2:
    currency=st.selectbox('Select currency',('EUR','USD','GBP'))
with col1:
    data = st.date_input("Pricelist start date", value=datetime.date.today())
    t = str(data.strftime("%d.%m.%Y"))

btn1 = st.button(' Create TAR', type='primary')
if btn1:
    if pricelist is not None:
        if id is not None:
            with st.spinner('Procesing...'):
                pricelist_table = pd.read_excel(pricelist)
                TAR = pricelist_table.filter(["PartNumber", 'List Price\n (EUR)', 'Authorization Discount Off','Authorization Unit Price\n(EUR FOB HongKong)'])
                # # #zmiana nazw kolumn
                TAR.rename(columns={'PartNumber': 'SKU', 'List Price\n (EUR)': 'Public Price', 'Authorization Discount Off': 'StdRebate','Authorization Unit Price\n(EUR FOB HongKong)': 'Channel Price'}, inplace=True)
                # # #dodawanie nowych kolumn i uzupełnianie
                TAR.insert(loc=1, column='AccountCode', value="ALL")
                TAR.insert(loc=2, column='Currency', value="EUR")
                TAR.insert(loc=3, column='Quantity', value="1")
                TAR['Currency']=currency
                TAR['Valid From'] = t
                TAR['Valid To'] = ""
                TAR['SearchAgain'] = "YES"
                TAR['UnitID'] = "PCS0DEC"
                TAR['LegalEntity'] = "101-120-141-311-501-502-550-560-580-582-700"
                TAR['StdRebate'] = TAR['StdRebate'] * 100
                TAR['Item Group'] = 'HUAWEI'

                # TAR2=st.dataframe(TAR.set_index("SKU"))
                TAR = TAR[['SKU', 'AccountCode', 'LegalEntity', 'Currency', 'Quantity', 'Public Price', 'StdRebate', 'Channel Price', 'Valid From', 'Valid To','SearchAgain', 'UnitID', 'Item Group']]

                # Set up SKU number as index
                TAR.set_index('SKU', inplace=True)

                # usuwanie SKu z zerowymi cenami i uzupelnianie brakujacych wartość
                TAR = TAR[TAR['Public Price'] != 0]
                TAR.loc[TAR['Channel Price'] == ' ', 'Channel Price'] = TAR['Public Price']
                TAR['StdRebate'] = TAR['StdRebate'].replace(np.nan, 0)

                TAR['Channel Price'] = TAR['Channel Price'].astype('float64')

                st.write(TAR)

                # buffer to use for excel writer
                buffer = io.BytesIO()

                # download button 2 to download dataframe as xlsx
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    iasset.to_excel(writer, sheet_name='TAR', startrow=0, startcol=0, index=False)
                    TAR.to_excel(writer, sheet_name='TAR',startrow=1)
                    writer.close()

                    downloadTAR = st.download_button(
                        label="Download TAR",
                        data=buffer,
                        file_name='HUAWEI-'+ number_id +'-TAR-'+today+'-SKU.xlsx',
                        mime='application/vnd.ms-excel'
                    )
        else:
            st.error('Select your name')
    else:
        st.error('no pricelist selected')


st.markdown('------------------------------------------------------------------')
# ------------------------------------  UPD  -----------------------------------
st.markdown('### :small_blue_diamond:  UPD file ###')

ekstrakt=st.file_uploader(label='Select Extract Vendor file', accept_multiple_files=False, type=["csv"])

con_sub = pd.DataFrame()
subgroups=st.file_uploader(label='Select Subgroups files', accept_multiple_files=True, type=["xlsx"])
for uploaded_file in subgroups:
    sub_data = pd.read_excel(uploaded_file)
    con_sub=pd.concat([sub_data,con_sub])
    # st.write(con_sub)


btn2 = st.button(' Create UPD', type='primary')
if btn2:
    if pricelist is not None:
        if id is not None:
            if ekstrakt is not None:
                if con_sub.empty:
                    st.error('Select files with subgroups')
                else:
                    with st.status("Prepering UPD", expanded=True) as status:
                        pricelist_table = pd.read_excel(pricelist)
                        df2 = pd.read_csv(ekstrakt, delimiter=';', usecols=['ItemID', 'ItemDescription', 'ItemGroupIDSub1', 'ItemGroupIDSub2', 'ItemGroupIDSub3','ItemGroupIDSub4', 'ItemGroupIDSub5', 'CustomerEDI', 'ORIGCOUNTRYREGIONID'])

                        #usuwanie znakow specjalnych w SKU (regex-[r]-regular expresion) tutaj usuwane puste znaki space, tab, enter [regex= \s]
                        st.write("Removing special characters from description")
                        time.sleep(2)
                        pricelist_table['PartNumber'] = pricelist_table['PartNumber'].str.replace(r'\s', "", regex=True)

                        # usuwanie przecinków z description
                        pricelist_table['Description'] = pricelist_table['Description'].astype(str)
                        pricelist_table['Description'] = pricelist_table['Description'].str.replace(',', " ")
                        pricelist_table['Description'] = pricelist_table['Description'].str.replace(r'[|]', ' ', regex=True)
                        pricelist_table['Description'] = pricelist_table['Description'].str.replace('  ', " ")

                        UPD = pricelist_table.filter(["PartNumber", "Description", "Software and Hardware Attributes", "Pack Weight\n (kg) ", "Pack Dimension\n (D*W*H mm) ","Net Dimension\n (D*W*H mm) ", "Discount Category", "Product Line", "Product Family", "Sub Product Family"])

                        # #zmiana nazw kolumn
                        UPD.rename(columns={'PartNumber': 'SKU'}, inplace=True)

                        # ----  wymiary ------
                        st.write("Extracting weight and dimension")
                        time.sleep(2)

                        #   GROSS
                        UPD["Pack Dimension\n (D*W*H mm) "] = UPD["Pack Dimension\n (D*W*H mm) "].str.extract(
                            r'([0-9]{1,5}[*][0-9]{1,5}[*][0-9]{1,5})', expand=True)
                        UPD["Pack Dimension\n (D*W*H mm) "] = UPD["Pack Dimension\n (D*W*H mm) "].str.replace(r'[*]{2}', '*', regex=True)
                        UPD[['Gross width', 'Gross Height', 'Gross Depth']] = UPD["Pack Dimension\n (D*W*H mm) "].str.split(r'[*]', expand=True)

                        UPD['Gross width'] = UPD['Gross width'].fillna(0)
                        UPD['Gross Height'] = UPD['Gross Height'].fillna(0)
                        UPD['Gross Depth'] = UPD['Gross Depth'].fillna(0)
                        UPD = UPD.astype({'Gross width': 'int', 'Gross Height': 'int', 'Gross Depth': 'int'})

                        UPD['Gross width'] = UPD['Gross width'] / 1000
                        UPD['Gross Height'] = UPD['Gross Height'] / 1000
                        UPD['Gross Depth'] = UPD['Gross Depth'] / 1000

                        #  NET
                        UPD["Net Dimension\n (D*W*H mm) "] = UPD["Net Dimension\n (D*W*H mm) "].str.extract(r'([0-9]{1,5}[*][0-9]{1,5}[*][0-9]{1,5})', expand=True)
                        UPD["Net Dimension\n (D*W*H mm) "] = UPD["Net Dimension\n (D*W*H mm) "].str.replace(r'[*]{2}', '*', regex=True)
                        UPD[['Net width', 'Net Height', 'Net Depth']] = UPD["Net Dimension\n (D*W*H mm) "].str.split(r'[*]', expand=True)

                        UPD['Net width'] = UPD['Net width'].fillna(0)
                        UPD['Net Height'] = UPD['Net Height'].fillna(0)
                        UPD['Net Depth'] = UPD['Net Depth'].fillna(0)
                        UPD = UPD.astype({'Net width': 'int', 'Net Height': 'int', 'Net Depth': 'int'})

                        UPD['Net width'] = UPD['Net width'] / 1000
                        UPD['Net Height'] = UPD['Net Height'] / 1000
                        UPD['Net Depth'] = UPD['Net Depth'] / 1000

                        UPD.loc[(UPD['Net width'] == 0) & (UPD['Gross width'] != 0), 'Net width'] = UPD['Gross width']
                        UPD.loc[(UPD['Net Height'] == 0) & (UPD['Gross Height'] != 0), 'Net Height'] = UPD['Gross Height']
                        UPD.loc[(UPD['Net Depth'] == 0) & (UPD['Gross Depth'] != 0), 'Net Depth'] = UPD['Gross Depth']

                        UPD.loc[(UPD['Gross width'] == 0) & (UPD['Net width'] != 0), 'Gross width'] = UPD['Net width']
                        UPD.loc[(UPD['Gross Height'] == 0) & (UPD['Net Height'] != 0), 'Gross Height'] = UPD['Net Height']
                        UPD.loc[(UPD['Gross Depth'] == 0) & (UPD['Net Depth'] != 0), 'Gross Depth'] = UPD['Net Depth']

                        UPD["Pack Weight\n (kg) "] = UPD["Pack Weight\n (kg) "].fillna(0)
                        UPD.loc[(UPD["Pack Weight\n (kg) "] != 0) | ((UPD['Gross width'] != 0) & (UPD['Gross Height'] != 0) & (UPD['Gross Depth'] != 0)) | ((UPD['Net width'] != 0) & (UPD['Net Height'] != 0) & (UPD['Net Depth'] != 0)), 'W&D'] = 'HARD'

                        st.write("Categorize Activity 1,2,3")
                        time.sleep(2)
                        # # ------------  Activity 1 ------------------------------------------------
                        # # HARD
                        UPD.loc[(UPD['W&D'] == 'HARD'), 'Activity 1'] = 'HARD'
                        UPD.loc[(UPD["Software and Hardware Attributes"] == 'Hardware'), 'Activity 1'] = 'HARD'
                        UPD.loc[(UPD["Discount Category"] == 'Hardware'), 'Activity 1'] = 'HARD'

                        UPD.loc[(UPD['Description'].str.contains('support', case=False) & (UPD['W&D'] == 'HARD')), 'Activity 1'] = 'HARD +Support'
                        UPD.loc[(UPD['Description'].str.contains('Power Suply', case=False)) & (~UPD['Description'].str.contains('with', case=False) & (UPD['W&D'] == 'HARD')), 'Activity 1'] = 'HARD Power Suply'

                        # # SOFT
                        UPD.loc[(UPD['Software and Hardware Attributes'] == 'Self-developed software') | ((UPD['Software and Hardware Attributes'] == 'Software Annuity')), 'Activity 1'] = 'SOFT Licences'
                        UPD.loc[(UPD['Description'].str.contains('upgrade', case=False) & (UPD["Activity 1"] == 'SOFT Licences')), 'Activity 1'] = 'SOFT Upgrade'
                        UPD.loc[(UPD['Description'].str.contains('Subscription', case=False) & (UPD["Activity 1"] == 'SOFT Licences')), 'Activity 1'] = 'SOFT Subscription'
                        UPD.loc[(UPD['Description'].str.contains('Subscription', case=False) & (UPD['Description'].str.contains('Support', case=False)) & ( UPD["Activity 1"] == 'SOFT Subscription')), 'Activity 1'] = 'SOFT Subscript +Support'
                        UPD.loc[UPD['Discount Category'].str.contains("License", case=False, na=False), 'Activity 1'] = 'SOFT Licences'

                        # UPD.loc[(UPD['Description'].str.contains('subscript',case=False)&(UPD["Activity 1"]=='SOFT Licences')),
                        # 'Activity 1']='SOFT Subscription'
                        # UPD.loc[(UPD['Description'].str.contains('secur',case=False)&(UPD["Activity 1"]=='SOFT Licences')),'Activity 1']='SOFT
                        # SECURE'

                        # # SERVICE
                        UPD.loc[UPD["Software and Hardware Attributes"] == 'Service', 'Activity 1'] = 'SERVICE'
                        UPD.loc[((UPD['Discount Category'] == 'Outsourcing') & (UPD['W&D'] != 'HARD') & (UPD['Description'].str.contains('service', case=False))), 'Activity 1'] = 'SERVICE'
                        UPD.loc[(UPD['Description'].str.contains('Data visualization service', case=False)), 'Activity 1'] = 'SERVICE'
                        UPD.loc[(UPD['Description'].str.contains('Security Service', case=False) & (UPD['Description'].str.contains('Yearly', case=False))), 'Activity 1'] = 'SERVICE'
                        UPD.loc[UPD['Description'].str.match(r'(^Security Service)', case=False, na=False), ['Activity 1']] = 'SERVICE'
                        UPD.loc[UPD['Activity 1'].isnull(), 'Activity 1'] = 'SERVICE'

                        # UPD.loc[(UPD["Method of Delivery"]=='Electronic') & ((UPD['Description'].str.contains('service',case=False)) | (UPD[
                        # 'Description'].str.contains('support',case=False))),'Activity 1']='SERVICE'

                        # # ------------     Activity 2    --------------

                        UPD.loc[UPD['Activity 1'] == 'HARD', 'Activity 2'] = 'OTHERS'
                        UPD.loc[((UPD['Activity 1'] == 'HARD') & (UPD['Description'].str.contains('server', case=False))), 'Activity 2'] = 'SERVER'
                        UPD.loc[((UPD['Activity 1'] == 'HARD') & (UPD['Description'].str.contains('port', case=False))), 'Activity 2'] = 'SERVER'
                        UPD.loc[((UPD['Activity 1'] == 'HARD') & (UPD['Description'].str.contains('unit', case=False))), 'Activity 2'] = 'SERVER'
                        UPD.loc[((UPD['Activity 1'] == 'HARD') & (UPD['Description'].str.contains('SSD', case=False))), 'Activity 2'] = 'STORAGE'
                        UPD.loc[((UPD['Activity 1'] == 'HARD') & (UPD['Description'].str.contains('HDD', case=False))), 'Activity 2'] = 'STORAGE'
                        UPD.loc[UPD['Activity 1'] == 'HARD +Support', 'Activity 2'] = 'OTHERS'
                        UPD.loc[UPD['Activity 1'] == 'SOFT Licences', 'Activity 2'] = 'OTHERS'
                        UPD.loc[UPD['Activity 1'] == 'SOFT Upgrade', 'Activity 2'] = 'OTHERS'
                        UPD.loc[UPD['Activity 1'] == 'SOFT SECURE', 'Activity 2'] = 'SECURITY'
                        UPD.loc[UPD['Activity 1'] == 'SOFT Subscription', 'Activity 2'] = 'OTHERS'
                        UPD.loc[UPD['Activity 1'] == 'SOFT Subscript +Support', 'Activity 2'] = 'OTHERS'
                        UPD.loc[UPD['Activity 1'] == 'SERVICE', 'Activity 2'] = 'MAINT'
                        UPD.loc[(UPD['Activity 1'] == 'SERVICE') & (UPD['Discount Category'].str.contains('Training', case=False)) & (UPD['Product Family'].str.contains('Training', case=False)), 'Activity 2'] = 'TRAINING'

                        # # UPD.loc[(UPD['Activity 1']=='SOFT Subscription')&((UPD['Description'].str.contains('secur',case=False))'Activity
                        # 2']='OTHERS'
                        # UPD.loc[(UPD['Description'].str.contains('secur',case=False)&(UPD["Activity 1"]=='SOFT Subscription')),
                        # 'Activity 2']='SECURITY'
                        # UPD.loc[UPD['Activity 1']=='SERVICE','Activity 2']='OTHERS'

                        # # ------------     Activity 3    ---------------

                        UPD.loc[(UPD["Description"].str.contains('renewal', case=False)) & (UPD['Activity 1'] != 'HARD'), 'Activity 3'] = 'RENEWAL'
                        UPD.loc[UPD['Activity 3'] != 'RENEWAL', 'Activity 3'] = 'INITIAL'

                        # #dodawanie nowych kolumn i uzupełnianie
                        UPD.insert(loc=0, column='Item Group', value="HUAWEI")
                        UPD.insert(loc=2, column="Vendor SKU", value="")
                        UPD.insert(loc=3, column="Item Type", value='Item')
                        UPD['Inventory Model Group'] = 'FIFOARW03'
                        UPD['Life Cycle'] = 'Online'
                        UPD['Stock Management'] = 'BACK TO BACK'
                        UPD['Finance Project Category'] = UPD['Item Group']
                        UPD['ItemPrimaryVendId'] = ''
                        UPD['Volume'] = ''
                        UPD['Legacy Id'] = ''
                        UPD['Customer EDI'] = 'YES'
                        UPD['List Price UpDate'] = 'YES'
                        UPD['Dual Use'] = 'YES'
                        UPD['Virtual Item'] = 'NO'
                        UPD['Arrow Brand'] = 'HUA'
                        UPD['Purchase Delivery Time'] = ''
                        UPD['Sales Delivery Time'] = ''
                        UPD['Production Type'] = 'NONE'
                        UPD['Unit point'] = ''
                        UPD['Warranty'] = ''
                        UPD['Renewal term'] = ''
                        UPD['Origin'] = 'CHN'
                        UPD.rename(columns={"Pack Weight\n (kg) ": "Weight"}, inplace=True)
                        UPD['Tare Weight'] = UPD['Weight'] * 0.2152
                        UPD['Finance Activity'] = UPD['Activity 1']
                        UPD['Special marker'] = ''
                        UPD['Special VAT Code'] = ''

                        st.write("Adding subgroup SUBGRUPY 1 according files")
                        time.sleep(2)

                        UPD['ItemGroupIDSub1']='1'
                        UPD['ItemGroupIDSub2']='2'
                        UPD['ItemGroupIDSub3']='3'
                        UPD['ItemGroupIDSub4']='4'
                        UPD['ItemGroupIDSub5']='5'


                        st.write('adding brand , subbrand ...')

                        data = [('HARD', 'SECURITY', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'SERVER', 'INITIAL', '84714100', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'STORAGE', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'OTHERS', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD Cable', 'OTHERS', 'INITIAL', '85444210', 'HW', 'GROSS', 'HWR'),
                                ('HARD Power Suply', 'OTHERS', 'INITIAL', '85044030', 'HW', 'GROSS', 'HWR'),
                                ('HARD +Support', 'SECURITY', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'SERVER', 'INITIAL', '84714100', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'STORAGE', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'OTHERS', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),

                                #  SERVICES  #
                                ('SERVICE', 'CLOUD', 'INITIAL', '00000000', 'XAAS', 'NET', 'SAA'),
                                ('SERVICE', 'CLOUD', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'INTEG', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'INTEG', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'LOGISTICS', 'INITIAL', '00000000', 'HW', 'GROSS', 'FRT'),
                                ('SERVICE', 'LOGISTICS', 'RENEWAL', '00000000', 'HW', 'GROSS', 'FRT'),
                                ('SERVICE', 'MAINT', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'MAINT', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'OTHERS', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'OTHERS', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'SUBSCRIPT', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'SUBSCRIPT', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'PROFSERV', 'INITIAL', '00000000', 'SVC_TPP', 'NET', 'VPS'),
                                ('SERVICE', 'PROFSERV', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                # TRENING #
                                ('SERVICE', 'TRAINING', 'INITIAL', '00000000', 'SVC_TPP', 'NET', 'WAT'),

                                #  SOFT  #
                                ('SOFT CLOUD', 'CLOUD', 'INITIAL', '00000000', 'XAAS', 'NET', 'SAA'),
                                ('SOFT SECURE', 'SECURITY', 'INITIAL', '00000000', 'SW_AV', 'NET', 'SWV'),
                                ('SOFT SECURE', 'SECURITY', 'RENEWAL', '00000000', 'SW_AV', 'NET', 'SWV'),
                                ('SOFT Upgrade', 'OTHERS', 'INITIAL', '00000000', 'SW_U', 'GROSS', 'SWN'),
                                ('SOFT Upgrade', 'SECURITY', 'INITIAL', '00000000', 'SW_U', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'CLOUD', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'OTHERS', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'OTHERS', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'SECURITY', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'SECURITY', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'STORAGE MG', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'STORAGE MG', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licence + Support', 'OTHERS', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT Licence + Support', 'SECURITY', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT Licence + Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'OTHERS', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'SECURITY', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT Subscription', 'OTHERS', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'OTHERS', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscription', 'SECURITY', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'SECURITY', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscription', 'STORAGE MG', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'STORAGE MG', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscript +Support', 'OTHERS', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),
                                ('SOFT Subscript +Support', 'SECURITY', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),
                                ('SOFT Subscript +Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),

                                #  ELA  #
                                ('SOFT ELA', 'OTHERS', 'INITIAL', '00000000', 'ELA', 'NET', 'ELA'),
                                ('SOFT ELA', 'OTHERS', 'RENEWAL', '00000000', 'ELA', 'NET', 'ELA'),
                                #  HYBRYD  #
                                ('SOFT HYBD', 'CLOUD', 'INITIAL', '00000000', 'HYBD', 'NET', 'HYB'),
                                ('SOFT HYBD', 'OTHERS', 'INITIAL', '00000000', 'HYBD', 'NET', 'HYB')
                                ]

                        gn = pd.DataFrame.from_records(data, columns=['Activity 1', 'Activity 2', 'Activity 3', 'Intrastat Code','Gross/Net Classification', 'Gross/Net', 'SUBBRAND'])
                        gn['merge'] = gn['Activity 1'] + gn['Activity 2'] + gn['Activity 3']


                        gn1 = gn[['merge', 'Intrastat Code', 'Gross/Net Classification', 'Gross/Net', 'SUBBRAND']]

                        UPD['merge'] = UPD['Activity 1'] + UPD['Activity 2'] + UPD['Activity 3']

                        UPD2 = UPD.merge(gn1, on="merge", how='left')

                        st.write("Adding Special VAT Code")
                        time.sleep(2)
                        UPD2.loc[(UPD2['Activity 1'] == 'SERVICE') & (UPD2['Activity 2'] == 'MAINT') & (UPD2['Description'].str.contains('HARD' or 'warranty', case=False)), 'Special VAT Code'] = 'SPVAT0001'

                        # ### Dimension Group
                        UPD2["Dimension Group"] = "PHYSICAL"
                        UPD2.loc[UPD2["Intrastat Code"] == "00000000", "Dimension Group"] = "STDBATCH3"

                        #### Serial Number Group
                        UPD2['Serial Number Group'] = "SN-AECS"
                        serial = {'00000000': "SN-AECS", '85444210': "SN-AECS", '85044030': "SN-AECS", }
                        UPD2['Serial Number Group'] = UPD2["Intrastat Code"].map(serial)

                        UPD2.loc[UPD2['Intrastat Code'] == '00000000', 'Virtual Item'] = 'YES'
                        UPD2['Activity 1'] = UPD2['Activity 1'].str.extract(r'(HARD|SOFT|SERVICE)')
                        UPD2['Finance Activity'] = UPD2['Finance Activity'].str.extract(r'(HARD|SOFT|SERVICE)')

                        st.write("Adding Special marker")
                        time.sleep(2)

                        ###  Special marker
                        UPD2.loc[((UPD2['Activity 1'] == 'SERVICE') & (UPD2['Activity 2'] == 'TRAINING')) & (~UPD2['Description'].str.contains('|'.join(['fee', 'Travel costs', 'Travel expenses', 'Conference', 'event', 'training materials', 'books']),case=False)), 'Special marker'] = "GTU_12"
                        UPD2.loc[(UPD2['Activity 1'] == 'HARD'), 'Special marker'] = "MPP_GTU_06"

                        # #porzadkowanie kolumn
                        UPD2 = UPD2[['Item Group', 'SKU', 'Vendor SKU', 'Item Type', 'Intrastat Code', 'Dimension Group', 'Serial Number Group','Inventory Model Group', 'Life Cycle', 'Activity 1', 'Activity 2', 'Activity 3', 'Stock Management','ItemGroupIDSub1', 'ItemGroupIDSub2', 'ItemGroupIDSub3', 'ItemGroupIDSub4', 'ItemGroupIDSub5', 'Description','ItemPrimaryVendId', 'Weight', 'Tare Weight', 'Gross width', 'Gross Height', 'Gross Depth', 'Net width','Net Height', 'Net Depth', 'Volume', 'Legacy Id', 'Finance Project Category', 'Finance Activity', 'Customer EDI','List Price UpDate', 'Dual Use', 'Virtual Item', 'Arrow Brand', 'Gross/Net', 'Gross/Net Classification','Purchase Delivery Time', 'Sales Delivery Time', 'Production Type', 'Unit point', 'Warranty', 'SUBBRAND','Renewal term', 'Special VAT Code', 'Origin', 'Special marker']]

                        roznica = UPD2.loc[~UPD2['SKU'].isin(df2['ItemID'])]

                        # Set up SKU number as index
                        roznica.set_index('SKU', inplace=True)

                    status.update(label="UPD complete!", state="complete", expanded=False)

                    if not roznica.empty:

                        # buffer to use for excel writer
                        bufferupd = io.BytesIO()

                        # download button 2 to download dataframe as xlsx
                        with pd.ExcelWriter(bufferupd, engine='xlsxwriter') as writer:
                            # Write each dataframe to a different worksheet.
                            iasset.to_excel(writer, sheet_name='UPD', startrow=0, startcol=0, index=False)
                            roznica.to_excel(writer, sheet_name='UPD', startrow=1)
                            writer.close()

                            downloadTAR = st.download_button(
                                label="Download UPD",
                                data=bufferupd,
                                file_name='HUAWEI-' + number_id + '-UPD-' + today + '-SKU.xlsx',
                                mime='application/vnd.ms-excel'
                            )
                        row_count = str(len(roznica))
                        st.write(':point_right:  ' + row_count + " new items to create")

                    else:
                        st.info('No new items to create')

                    st.write(roznica)
            else:
                st.error('Add HUAWEI Extract file')
        else:
            st.error('Select your name ID')
    else:
        st.error('no pricelist selected')


st.markdown('------------------------------------------------------------------')
# ------------------------------------  AMD  -----------------------------------
st.markdown('### :small_blue_diamond:  AMD file ###')

# buffer to use for excel writer

btn3 = st.button(' Create AMD', type='primary')
if btn3:
    st.write(ekstrakt)
    ekstrakt_table = pd.read_csv(ekstrakt, delimiter=';')
    # ekstrakt_table = pd.read_csv(ekstrakt)
    st.write(ekstrakt_table)

    pricelist_table = pd.read_excel(pricelist)
    st.write(pricelist_table)

    # bufferamd = io.BytesIO()


    # download button 2 to download dataframe as xlsx
    # with pd.ExcelWriter(bufferamd, engine='xlsxwriter') as writer:
    #     # Write each dataframe to a different worksheet.
    #     iasset.to_excel(writer, sheet_name='UPD', startrow=0, startcol=0, index=False)
    #     roznica.to_excel(writer, sheet_name='UPD', startrow=1)
    #     writer.close()
    #
    #     downloadTAR = st.download_button(
    #         label="Download UPD",
    #         data=bufferamd,
    #         file_name='HUAWEI-' + number_id + '-UPD-' + today + '-SKU.xlsx',
    #         mime='application/vnd.ms-excel'
    #                             )