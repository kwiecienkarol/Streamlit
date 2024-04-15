import pandas as pd
from io import BytesIO
# from pyxlsb import open_workbook as open_xlsb
import streamlit as st

# st.set_page_config(layout="wide")
data = {
    "a": [420, 380, 390],
    "b": [50, 40, 45],
    "c": [5, 12, 1],
    "d": [230, 23, 1]
}
df = pd.DataFrame(data)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='TAR')
    workbook = writer.book
    worksheet = writer.sheets['TAR']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data
df_xlsx = to_excel(df)
st.download_button(label='📥 Download Current Result',data=df_xlsx ,file_name= 'Test_2.xlsx')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])


# --------------------------------------------------------------------------------------------------------------------------


import streamlit as st
import pandas as pd
import io
import datetime

today=datetime.datetime.today().strftime("%d.%m.%Y")

# buffer to use for excel writer
buffer = io.BytesIO()

# data = {
#     "calories": [4200000, 3800000, 39000000],
#     "duration": [50, 40, 45],
#     "random1": [5, 12, 1],
#     "random2": [230, 23, 1]
# }
# df = pd.DataFrame(data)

iasset_data={'iAsset':[],'No':[]}
iasset=pd.DataFrame(iasset_data)


# display the dataframe on streamlit app

st.write(df)

t='22'
# download button 2 to download dataframe as xlsx
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    iasset.to_excel(writer, sheet_name='TAR', startrow=0, startcol=0, index=False)
    df.to_excel(writer, sheet_name='TAR',startrow=1, index=False)
    writer.close()

    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='HUAWEI-TAR-'+today+'-SKU.xlsx',
        mime='application/vnd.ms-excel'
    )



