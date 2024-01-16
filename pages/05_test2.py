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