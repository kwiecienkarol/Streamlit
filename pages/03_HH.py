import streamlit as st
import pandas as pd
import time
import datetime
import os
# from tkinter import filedialog
# import tkinter as tk
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
    # st.selectbox('your name',options=st.session_state['person'], index=1)
    # https://www.youtube.com/watch?v=8-GavXeFlEA
    id=st.selectbox('Your name - ID',('Karol Kwiecień - A86227','Katarzyna Czyż - A86361', 'Emil Twardowski - A93176', 'Chistian Gay - A60276',
                                       'Paweł Czaja - A89264', 'Hanna Źródlewska - 132693', 'Karmen Bautembach - 136182'),index=None,placeholder="Select your name")

    # if id is not None:
    #     # st.write(id[-6:])
    #     number_id = id[-6:]

    # st.write(nn)
    st.write(st.session_state['person'])
# selecting pricelist and folder directory
st.markdown('------------------------------------------------------------------')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])


st.markdown('------------------------------------------------------------------')
# ------------------------------------  TAR  -----------------------------------
st.markdown('### :small_blue_diamond:  TAR file ###')

btn1 = st.button(' Create TAR', type='primary')
if btn1:
    if pricelist is not None:
        st.success('Pricelist selected')

    else:
        st.error('no pricelist selected')