import streamlit as st
import pandas as pd
import io

st.title('WATCHGUARD')
st.markdown('[Watchguard Sharpoint](https://arrowelectronics.sharepoint.com/:f:/r/sites/EMEAProductCatalog/Shared%20Documents/A%20-%20Price%20Catalog/P%20-%20Z/WATCHGUARD?csf=1&web=1&e=MOVW9J) ')


st.markdown('------------------------------------------------------------------')

pricelist=st.file_uploader(label=':small_blue_diamond: Select Pricelist file', accept_multiple_files=False, type=["xlsx"])

st.markdown('------------------------------------------------------------------')
st.markdown('### :small_blue_diamond:  TAR creator ###')

st.markdown('------------------------------------------------------------------')

st.markdown('### :small_blue_diamond:  UPD creator ###')

con_sub = pd.DataFrame()
subgroups=st.file_uploader(label=':small_blue_diamond: Select Subgroups files', accept_multiple_files=True, type=["xlsx"])
for uploaded_file in subgroups:
    sub_data = pd.read_excel(uploaded_file)
    con_sub=pd.concat([sub_data,con_sub])


con_sub = con_sub.reset_index()
con_sub.loc[con_sub['Sub group 1'].notnull(),'Description_sub1']=con_sub['Description']
con_sub.loc[con_sub['Sub group 2'].notnull(),'Description_sub2']=con_sub['Description']
con_sub.loc[con_sub['Sub group 3'].notnull(),'Description_sub3']=con_sub['Description']
con_sub.loc[con_sub['Sub group 4'].notnull(),'Description_sub4']=con_sub['Description']
con_sub['Description_sub4']=con_sub['Description_sub4'].str.lower()
con_sub.loc[con_sub['Sub group 5'].notnull(),'Description_sub5']=con_sub['Description']

st.write(con_sub)

UPD=pd.read_excel(pricelist)

UPD['Product Family']=UPD['Product Family'].str.strip()
UPD['Product Line']=UPD['Product Line'].str.strip()
UPD['Discount Category']=UPD['Discount Category'].str.strip().str.lower()
UPD['Sub Product Family']=UPD['Sub Product Family'].str.strip()

UPD=pd.merge(UPD,con_sub[['Sub group 1','Description_sub1']],left_on='Software and Hardware Attributes',right_on='Description_sub1', how='left')
UPD=pd.merge(UPD,con_sub[['Sub group 2','Description_sub2']],left_on='Product Family',right_on='Description_sub2', how='left')
UPD=pd.merge(UPD,con_sub[['Sub group 3','Description_sub3']],left_on='Product Line',right_on='Description_sub3', how='left')
UPD=pd.merge(UPD,con_sub[['Sub group 4','Description_sub4']],left_on='Discount Category',right_on='Description_sub4', how='left')
UPD=pd.merge(UPD,con_sub[['Sub group 5','Description_sub5']],left_on='Sub Product Family',right_on='Description_sub5', how='left')


UPD.loc[UPD['Software and Hardware Attributes']==' ','Sub group 1']='####'
UPD.loc[UPD['Product Family']==' ','Sub group 2']='####'
UPD.loc[UPD['Product Line']==' ','Sub group 3']='####'
UPD.loc[UPD['Product Line']=='','Sub group 3']='####'
UPD.loc[UPD['Discount Category']==' ','Sub group 4']='####'
UPD.loc[UPD['Discount Category'].isnull(),'Sub group 4']='####'
UPD.loc[UPD['Sub Product Family']==' ','Sub group 5']='####'
UPD.loc[UPD['Sub Product Family']=='','Sub group 5']='####'
UPD.loc[UPD['Sub Product Family'].isnull(),'Sub group 5']='####'

UPD.rename(columns={'Sub group 1':'SubGroup1','Sub group 2':'SubGroup2','Sub group 3':'SubGroup3','Sub group 4':'SubGroup4','Sub group 5':'SubGroup5'}, inplace=True)

# sprawdzanie brakujacych subgrup
new_sub=UPD.copy()

new_sub.loc[new_sub['SubGroup1'].isnull(),'NEW_Subgrup1']='NEW_SUB_1'
new_sub.loc[new_sub['NEW_Subgrup1']=='NEW_SUB_1','NEW_Subgrup1_description']=new_sub['Software and Hardware Attributes']


st.write(UPD)

# buffer to use for excel writer

bufferupd = io.BytesIO()

 # download button 2 to download dataframe as xlsx
with pd.ExcelWriter(bufferupd, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    UPD.to_excel(writer, sheet_name='UPD', startrow=1, index=False)
    writer.close()

downloadUPD = st.download_button(
    label=":inbox_tray: Download UPD-test",
    data=bufferupd,
    file_name='SUB-test.xlsx',
    mime='application/vnd.ms-excel')

# UPD=pd.merge(UPD,con_sub,left_on='Software and Hardware Attributes',right_on='Description_sub', how='left')
# UPD.loc[UPD['Software and Hardware Attributes']==' ','ItemGroupIDSub1']='####'
#
# UPD=pd.merge(UPD,con_sub,left_on='Product Family',right_on='Description_sub', how='left')
# UPD.loc[UPD['Product Family']==' ','ItemGroupIDSub2']='####'



st.markdown('------------------------------------------------------------------')
st.markdown('### :small_blue_diamond:  AMD creator ###')