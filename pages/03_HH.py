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

st.markdown('------------------------------------------------------------------')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])

st.markdown('------------------------------------------------------------------')

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
            # with st.spinner('Prepering file...'):
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

            # # Set up SKU number as index
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
                TAR.to_excel(writer, sheet_name='TAR', index=False)

                downloadTAR = st.download_button(
                    label="Download TAR",
                    data=buffer,
                    file_name='HUAWEI-TAR.xlsx',
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

btn2 = st.button(' Create UPD', type='primary')
if btn2:
    if pricelist is not None:
        if id is not None:
            st.success('ID and pricelist OK')
        else:
            st.error('Select your name')
    else:
        st.error('no pricelist selected')