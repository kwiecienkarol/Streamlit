import streamlit as st

st.title('ItemActivation Tool ')
# st.header('to naglówek')
# st.markdown('# HUAWEI #')
# st.markdown('### UPD ###')

with st.expander('wprowadx dane do UPD'):
# st.text('tekst')
# st.info('jakis info')
# st.warning('uwaga')
# st.success('sukces')
# st.error('bład')
    st.text_input(label= ':book: Arrow ID')

    col1, col2= st.columns(2)
    var1=col1.checkbox('approve')
    var2=col2.checkbox('not agree')
    var3=col1.multiselect('curency',['USD','EUR'])
    col2.selectbox('lubisz psy?',('tak','nie'))

# var1
# var2
# var3[0]

btn=st.button('Run', type='primary')