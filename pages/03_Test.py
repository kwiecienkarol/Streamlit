import datetime as dt
import os
import tkinter.filedialog
from tkinter import *
from tkinter import filedialog
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import streamlit as st
import tkinter as tk


pricelist=st.file_uploader(label=':small_blue_diamond: Pricelist file', accept_multiple_files=False, type=["xlsx"])
if pricelist is not None:
    pl=pd.read_excel(pricelist)
    with open(pricelist.name,"wb")as f:
        f.write(pricelist.getbuffer())
    st.success('Pricelist file added')


def select_file():
    root = tk.Tk()
    root.withdraw()
    folder_path = root.filename = tk.filedialog.askopenfilename(master=root, filetypes=[("Excel files", "*.xlsx")])
    root.destroy()
    return folder_path

# selected_folder_path = st.session_state.get("folder_path", None)
folder_select_button = st.button("Select Pricelist file",type='primary')
if folder_select_button:
    selected_folder_path = select_file()
    path = os.path.dirname(selected_folder_path)
    # st.session_state.folder_path = selected_folder_path

    st.write("Folder:", path)
    st.write("Folder:", selected_folder_path)
    pricelist = pd.read_excel(selected_folder_path)
    st.success('Pricelist file added')

# st.write("Folder:", pricelist)


# st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
    st.write(st.session_state)
# else:
#     st.write('Goodbye')
#
# if st.button('Say yo'):
#     st.write('yo')
# else:
#     st.write('Goodbye')

st.multiselect('curency',['USD','EUR'])