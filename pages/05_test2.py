import streamlit as st
import xlsxwriter
from io import BytesIO
import pandas as pd

output = BytesIO()

data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45],
    "random1": [5, 12, 1],
    "random2": [230, 23, 1]
}
df = pd.DataFrame(data)


# Write files to in-memory strings using BytesIO
# See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
workbook = xlsxwriter.Workbook(output, {'in_memory': True})
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello')
workbook.close()

st.download_button(
    label="Download Excel workbook",
    data=output.getvalue(),
    file_name="workbook.xlsx",
    mime="application/vnd.ms-excel"
)
con_sub = pd.DataFrame()
subgroups=st.file_uploader(label='Select Extract Vendor file', accept_multiple_files=True, type=["xlsx"])
for uploaded_file in subgroups:
    sub_data = pd.read_excel(uploaded_file)
    con_sub=pd.concat([sub_data,con_sub])
    st.write(con_sub)

if con_sub.empty:
    st.write('empty')
else:
    st.success('file loaded')
    # st.write(subgroups)

