import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os

def select_file():
   root = tk.Tk()
   root.withdraw()
   folder_path =root.filename= tk.filedialog.askopenfilename(master=root, filetypes=[("Excel files", "*.xlsx")])
   root.destroy()
   return folder_path


folder_select_button = st.button("Select Pricelist")
if folder_select_button:
    selected_folder_path = select_file()
    path = os.path.dirname(selected_folder_path)

    st.write("Folder:", path)
    st.write(st.session_state['gvn'])
# https://medium.com/@kjavaman12/how-to-create-a-folder-selector-in-streamlit-e44816c06afd