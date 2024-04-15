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

# st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"ColorMeBlue text”"}</h1>', unsafe_allow_html=True)

st.markdown('<style>stApp{background-color: green;}<style>', unsafe_allow_html=True)

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


import streamlit as st
import streamlit.components.v1 as components

st.title("Yellow component ")

html_content = "<div>Hello world</div>"
yellow_background = "<style>:root {background-color: rgb(223, 230, 237);}</style>"
components.html(yellow_background + html_content)

st.markdown(
        """
         background-color: rgb(223, 230, 237);}</style>
        <span style="color:blue">some *This is Blue italic.* text</span>
    """,
    unsafe_allow_html=True
    )

st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")

st.markdown(f'<h1 style="color:#33ff44;font-size:24px;">{"ColorMeBlue text”"}</h1>', unsafe_allow_html=True)

