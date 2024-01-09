import streamlit as st
import pandas as pd
import time
import datetime
import os
from tkinter import filedialog
import tkinter as tk
import numpy as np
from openpyxl import load_workbook

today=datetime.datetime.today().strftime("%d.%m.%Y")

st.title('HUAWEI')
st.markdown('[Huawei Sharpoint](https://arrowelectronics.sharepoint.com/:f:/r/sites/EMEAProductCatalog/Shared%20Documents/A%20-%20Price%20Catalog/D%20-%20H/HUAWEI?csf=1&web=1&e=mkQgMK/) ')

st.markdown('------------------------------------------------------------------')

col1, col2 = st.columns(2)
with col2:
    data=st.date_input("Pricelist start date", value=datetime.date.today())
    t=str(data.strftime("%d.%m.%Y"))

with col1:
    id=st.selectbox('Your name - ID',('Karol Kwiecień - A86227','Katarzyna Czyż - A86361', 'Emil Twardowski - A93176', 'Chistian Gay - A60276',
                                      'Paweł Czaja - A89264', 'Hanna Źródlewska - 132693', 'Karmen Bautembach - 136182'),index=None,placeholder="Select your name")

    if id is not None:
        # st.write(id[-6:])
        number_id = id[-6:]


# selecting pricelist and folder directory
st.markdown('------------------------------------------------------------------')

def select_file():
    root = tk.Tk()
    root.withdraw()
    folder_path = root.filename = tk.filedialog.askopenfilename(master=root, filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return folder_path

selected_folder_path = st.session_state.get("folder_path", None)

folder_select_button = st.button("Select Pricelist file",type='primary')

if folder_select_button:
    selected_folder_path = select_file()
    path = os.path.dirname(selected_folder_path)

    st.session_state.folder_path = selected_folder_path
    st.session_state.path =path

    st.success('Pricelist file added')


if 'folder_path' not in st.session_state:
    st.write('No file selected')
else:
    st.write(st.session_state['folder_path'])
    # st.write(st.session_state['path'])

st.markdown('------------------------------------------------------------------')
# ------------------------------------  TAR  -----------------------------------
st.markdown('### TAR file ###')

btn1 = st.button(' Create TAR', type='primary')
if btn1:
    if 'folder_path' not in st.session_state:
        st.error('No pricelist selected')

    else:
        if id is not None:
            number_id = id[-6:]

            # st.write(st.session_state['folder_path'])
            url = st.session_state['folder_path']

            with st.spinner('Prepering file...'):

                pricelist = pd.read_excel(url)
                TAR = pricelist.filter(["PartNumber", 'List Price\n (EUR)', 'Authorization Discount Off','Authorization Unit Price\n(EUR FOB HongKong)'])
            # # #zmiana nazw kolumn
                TAR.rename(columns={'PartNumber': 'SKU', 'List Price\n (EUR)': 'Public Price','Authorization Discount Off': 'StdRebate','Authorization Unit Price\n(EUR FOB HongKong)': 'Channel Price'}, inplace=True)
            # # #dodawanie nowych kolumn i uzupełnianie
                TAR.insert(loc=1, column='AccountCode', value="ALL")
                TAR.insert(loc=2, column='Currency', value="EUR")
                TAR.insert(loc=3, column='Quantity', value="1")
                TAR['Valid From'] = t
                TAR['Valid To'] = ""
                TAR['SearchAgain'] = "YES"
                TAR['UnitID'] = "PCS0DEC"
                TAR['LegalEntity'] = "101-120-141-311-501-502-550-560-580-582-700"
                TAR['StdRebate'] = TAR['StdRebate'] * 100
                TAR['Item Group'] = 'HUAWEI'


                # TAR2=st.dataframe(TAR.set_index("SKU"))
                TAR = TAR[['SKU', 'AccountCode', 'LegalEntity', 'Currency', 'Quantity', 'Public Price', 'StdRebate','Channel Price', 'Valid From', 'Valid To', 'SearchAgain', 'UnitID', 'Item Group']]

                # # Set up SKU number as index
                TAR.set_index('SKU', inplace=True)

                # usuwanie SKu z zerowymi cenami i uzupelnianie brakujacych wartość
                TAR = TAR[TAR['Public Price'] != 0]
                TAR.loc[TAR['Channel Price'] == ' ', 'Channel Price'] = TAR['Public Price']
                TAR['StdRebate'] = TAR['StdRebate'].replace(np.nan, 0)

                TAR['Channel Price'] = TAR['Channel Price'].astype('float64')


                TAR.to_excel(st.session_state['path'] + "/HUAWEI-"+number_id+"-TAR-" + today + "-SKU.xlsx", sheet_name='TAR', startrow=1)

                wbook = load_workbook(st.session_state['path'] + "/HUAWEI-"+number_id+"-TAR-" + today + "-SKU.xlsx")
                sheet = wbook.active
                sheet['A1'] = 'iAssetSync'
                sheet['B1'] = 'No'
                wbook.save(st.session_state['path'] + "/HUAWEI-"+number_id+"-TAR-" + today + "-SKU.xlsx")

                st.write(TAR)

                # st.write(st.session_state['folder_path'])
                # st.write(st.session_state['path'])
                st.success('TAR saved in pricelist file directory')
        else:
            st.error("Select your name -ID")

st.markdown('----------------------------------------------------------------------------------------------------')
# --------------------------------     UPD     -------------------------------------------------------------------
st.markdown('### UPD file ###')
with st.expander(':large_blue_circle: Data for UPD'):
# subgrups = st.file_uploader(label='Subgrups files',accept_multiple_files=True)

    ekstrakt=st.file_uploader(label=':small_blue_diamond: Extract file', accept_multiple_files=False, type=["csv"])

    subgroups=st.file_uploader(label=':small_blue_diamond: Subgroups', accept_multiple_files=True, type=["xlsx"])
    # pricelist = pd.read_csv(ekstrakt)
    # if pricelist is not None:
    #     pl=pd.read_excel(pricelist)
    #     with open(pricelist.name,"wb")as f:
    #         f.write(pricelist.getbuffer())
    #     st.success('Pricelist file added')

btn2 = st.button('Create UPD', type='primary')
if btn2:
        st.write("xxxx")
        if 'folder_path' not in st.session_state:
            st.error('No pricelist selected')
        else:
            if id is not None:
                number_id = id[-6:]

                # st.write(st.session_state['folder_path'])
                url = st.session_state['folder_path']

                if ekstrakt is not None:
                    with st.status("Prepering UPD", expanded=True) as status:

                        st.write("Comparing Pricelist files with extract")
                        pricelist = pd.read_excel(url)
                        df2 = pd.read_csv(ekstrakt, delimiter=';', usecols=['ItemID','ItemDescription','ItemGroupIDSub1','ItemGroupIDSub2','ItemGroupIDSub3','ItemGroupIDSub4','ItemGroupIDSub5','CustomerEDI','ORIGCOUNTRYREGIONID'])

                        # #usuwanie znakow specjalnych w SKU (regex-[r]-regular expresion) tutaj usuwane puste znaki space, tab, enter [regex= \s]
                        pricelist['PartNumber'] = pricelist['PartNumber'].str.replace(r'\s', "", regex=True)

                        # # usuwanie przecinków z description
                        pricelist['Description'] = pricelist['Description'].astype(str)
                        pricelist['Description'] = pricelist['Description'].str.replace(',', " ")
                        pricelist['Description'] = pricelist['Description'].str.replace(r'[|]', ' ', regex=True)
                        pricelist['Description'] = pricelist['Description'].str.replace('  ', " ")

                        UPD = pricelist.filter(["PartNumber", "Description", "Software and Hardware Attributes", "Pack Weight\n (kg) ", "Pack Dimension\n (D*W*H mm) ","Net Dimension\n (D*W*H mm) ", "Discount Category", "Product Line", "Product Family", "Sub Product Family"])

                        # #zmiana nazw kolumn
                        UPD.rename(columns={'PartNumber': 'SKU'}, inplace=True)

                        roznica = UPD.loc[~UPD['SKU'].isin(df2['ItemID'])]

                        st.write("saving file...")

                        roznica.to_excel(st.session_state['path'] + "/HUAWEI-" + number_id + "-UPD-" + today + "-SKU.xlsx", sheet_name='UPD', startrow=1,index=False)

                        st.write("merge files...")
                        time.sleep(2)
                        st.write("prepering TAR.")
                        time.sleep(1)
                        st.write("remove duplicates")
                        time.sleep(1)
                    status.update(label="UPD complete!", state="complete", expanded=False)


                    if not roznica.empty:
                        st.write("xxxx new items to create")
                        st.success('UPD saved in pricelist file directory')
                    else:
                        st.info('No new items to create')
                else:
                    st.error("Extract file NOT selected")
            else:
                st.error("Select your name -ID")
