import streamlit as st
import pandas as pd
import time
import datetime
import os
import numpy as np
import io

today=datetime.datetime.today().strftime("%d.%m.%Y")

st.title('HP')
st.markdown('[HP - SharePoint](https://arrowelectronics.sharepoint.com/:f:/r/sites/EMEAProductCatalog/Shared%20Documents/A%20-%20Price%20Catalog/D%20'
            '-%20H/HP?csf=1&web=1&e=xKU7d4)')


st.markdown('------------------------------------------------------------------')

id=st.selectbox(':small_blue_diamond: Your name - ID',('Karol Kwiecień - A86227','Katarzyna Czyż - A86361', 'Emil Twardowski - A93176','Chistian Gay - A60276','Paweł Czaja - A89264', 'Hanna Źródlewska - 132693','Karmen Bautembach - 136182', 'Agnieszka Szarmach - A89210', 'Wojciech Sroczyński - 142049','AFIF Mouad - 152179', 'Chafika Bahi - 157981'),index=None,placeholder="Select your " "name")

if id is not None:
    # st.write(id[-6:])
    number_id = id[-6:]

st.markdown('------------------------------------------------------------------')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])
ekstrakt=st.file_uploader(label=':date: Select Extract Vendor file', accept_multiple_files=False, type=["csv"])


# adding Iasset table
iasset_data = {'iAsset': [], 'No': []}
iasset = pd.DataFrame(iasset_data)

st.markdown('------------------------------------------------------------------')

# **********************************************          TAR      *********************************************************************
st.markdown('### :small_blue_diamond:  TAR creator ###')

col1, col2 = st.columns(2)
with col2:
    currency=st.selectbox('Select currency',('EUR','USD','GBP'))
with col1:
    data = st.date_input("Pricelist start date", value=datetime.date.today())
    t = str(data.strftime("%d.%m.%Y"))

pl_file=st.file_uploader(label=':small_blue_diamond: Select file with PL numbers', accept_multiple_files=False, type=["xlsx"])
# pl=pd.read_excel(pl_file)

btn1 = st.button(' Create TAR', type='primary')

if btn1:
    if pricelist is not None:
        if id is not None:
            if pl_file is not None:
                pl = pd.read_excel(pl_file)
                with st.spinner('Procesing...'):
                    pricelist_table = pd.read_excel(pricelist)

                    TAR = pricelist_table.filter(['Product Number', 'List Price', 'Net Price', 'PA Discount Percentage', 'PL'])
                    # # #zmiana nazw kolumn
                    TAR.rename(columns={'Product Number': 'SKU', 'List Price': 'Public Price', 'PA Discount Percentage': 'StdRebate','Net Price': 'Channel Price'}, inplace=True)
                    # # #dodawanie nowych kolumn i uzupełnianie
                    TAR['AccountCode'] ="ALL"
                    TAR['Quantity']="1"
                    TAR['Currency'] = currency
                    TAR['Valid From'] = t
                    TAR['Valid To'] = ""
                    TAR['SearchAgain'] = "YES"
                    TAR['UnitID'] = "PCS0DEC"
                    TAR['LegalEntity'] = "120-311-550-560-580-581"
                    TAR['StdRebate'] = (1-(TAR['Channel Price']/TAR['Public Price']))*100
                    TAR['StdRebate'] = TAR['StdRebate'].replace(np.nan, 0)
                    TAR['StdRebate'] = TAR['StdRebate'].round(2)
                    TAR['Item Group'] = 'HP'


                    # TAR_pl = TAR.merge(pl, on="PL", how='left')
                    TAR_pl = pd.merge(TAR, pl, left_on='PL', right_on='Product Line', how='left')
                    TAR_pl.loc[TAR_pl["PL"] == TAR_pl['Product Line'], 'PL check'] = "item with correct PL"
                    TAR_pl= TAR_pl.loc[TAR_pl['PL check'] == "item with correct PL"]

                    # Set up SKU number as index
                    TAR_pl.set_index('SKU', inplace=True)

                    TAR_pl = TAR_pl[['AccountCode', 'LegalEntity', 'Currency', 'Quantity', 'Public Price', 'StdRebate', 'Channel Price', 'Valid From','Valid To', 'SearchAgain', 'UnitID', 'Item Group']]

                    st.write(TAR_pl)
                    # buffer to use for excel writer
                    buffer = io.BytesIO()

                    # download button 2 to download dataframe as xlsx
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        # Write each dataframe to a different worksheet.
                        iasset.to_excel(writer, sheet_name='TAR', startrow=0, startcol=0, index=False)
                        TAR_pl.to_excel(writer, sheet_name='TAR', startrow=1)
                        writer.close()

                        downloadTAR = st.download_button(
                            label="Download TAR",
                            data=buffer,
                            file_name='HP-' + number_id + '-TAR-' + today + '-SKU.xlsx',
                            mime='application/vnd.ms-excel'
                        )
            else:
                st.error('Select file with PL numbers')
        else:
            st.error('Select your name')
    else:
        st.error('no pricelist selected')

st.markdown('------------------------------------------------------------------')

st.markdown('### :small_blue_diamond:  UPD creator ###')

con_sub = pd.DataFrame()
subgroups=st.file_uploader(label=':small_blue_diamond: Select Subgroups files', accept_multiple_files=True, type=["xlsx"])


st.markdown('------------------------------------------------------------------')
st.markdown('### :small_blue_diamond:  AMD creator  ###')