import streamlit as st
import pandas as pd


# st.set_page_config(page_title="App", layout="wide")

st.header(':taco: P.I.T.A')
st.header('Pricelist Information Tool for Automation')
# st.header(" :information_desk_person: PUPA - Pricelist Update Program Automat")

# st.header(':dancer:  PATI -  Pricelist Automat for Transforming Informations')
st.header('')
st.write('Program transform Pricelist files to UPD and TAR format. Once the price list data has been imported, it can be processed in a variety of ways')
st.markdown('-----------')


st.markdown('-----------')
st.markdown('<a href="mailto:kwiecienkarol@o2.pl">Contact me </a>', unsafe_allow_html=True)

# with st.expander('wprowadx dane do UPD'):
# st.text('tekst')
# st.info('jakis info')
# st.warning('uwaga')
# st.success('sukces')
# st.error('bład')


# st.text_input(label= ':book: Arrow ID')
# col1, col2= st.columns(2)
# var1=col1.checkbox('approve')
# var2=col2.checkbox('not agree')
# var3=col1.multiselect('curency',['USD','EUR'])
# col2.selectbox('lubisz psy?',('tak','nie'))


data = [('HARD', 'SECURITY', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'SERVER', 'INITIAL', '84714100', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'STORAGE', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD', 'OTHERS', 'INITIAL', '84714900', 'HW', 'GROSS', 'HWR'),
                                ('HARD Cable', 'OTHERS', 'INITIAL', '85444210', 'HW', 'GROSS', 'HWR'),
                                ('HARD Power Suply', 'OTHERS', 'INITIAL', '85044030', 'HW', 'GROSS', 'HWR'),
                                ('HARD +Support', 'SECURITY', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'SERVER', 'INITIAL', '84714100', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'STORAGE', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),
                                ('HARD +Support', 'OTHERS', 'INITIAL', '84714900', 'HW_SVC', 'GROSS', 'SBH'),

                                #  SERVICES  #
                                ('SERVICE', 'CLOUD', 'INITIAL', '00000000', 'XAAS', 'NET', 'SAA'),
                                ('SERVICE', 'CLOUD', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'INTEG', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'INTEG', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'LOGISTICS', 'INITIAL', '00000000', 'HW', 'GROSS', 'FRT'),
                                ('SERVICE', 'LOGISTICS', 'RENEWAL', '00000000', 'HW', 'GROSS', 'FRT'),
                                ('SERVICE', 'MAINT', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'MAINT', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'OTHERS', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'OTHERS', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'SUBSCRIPT', 'INITIAL', '00000000', 'SVC_MAINT', 'NET', 'SPN'),
                                ('SERVICE', 'SUBSCRIPT', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                ('SERVICE', 'PROFSERV', 'INITIAL', '00000000', 'SVC_TPP', 'NET', 'VPS'),
                                ('SERVICE', 'PROFSERV', 'RENEWAL', '00000000', 'RNW', 'NET', 'SPR'),
                                # TRENING #
                                ('SERVICE', 'TRAINING', 'INITIAL', '00000000', 'SVC_TPP', 'NET', 'WAT'),

                                #  SOFT  #
                                ('SOFT CLOUD', 'CLOUD', 'INITIAL', '00000000', 'XAAS', 'NET', 'SAA'),
                                ('SOFT SECURE', 'SECURITY', 'INITIAL', '00000000', 'SW_AV', 'NET', 'SWV'),
                                ('SOFT SECURE', 'SECURITY', 'RENEWAL', '00000000', 'SW_AV', 'NET', 'SWV'),
                                ('SOFT Upgrade', 'OTHERS', 'INITIAL', '00000000', 'SW_U', 'GROSS', 'SWN'),
                                ('SOFT Upgrade', 'SECURITY', 'INITIAL', '00000000', 'SW_U', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'CLOUD', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'OTHERS', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'OTHERS', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'SECURITY', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'SECURITY', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licences', 'STORAGE MG', 'INITIAL', '00000000', 'SW_P', 'GROSS', 'SWN'),
                                ('SOFT Licences', 'STORAGE MG', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Licence + Support', 'OTHERS', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT Licence + Support', 'SECURITY', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT Licence + Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWP_SVC', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'OTHERS', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'SECURITY', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT UPD Licence + Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWU_SVC ', 'GROSS', 'SBS'),
                                ('SOFT Subscription', 'OTHERS', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'OTHERS', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscription', 'SECURITY', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'SECURITY', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscription', 'STORAGE MG', 'INITIAL', '00000000', 'SW_FT', 'GROSS', 'SWF'),
                                ('SOFT Subscription', 'STORAGE MG', 'RENEWAL', '00000000', 'SW_R', 'GROSS', 'SWR'),
                                ('SOFT Subscript +Support', 'OTHERS', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),
                                ('SOFT Subscript +Support', 'SECURITY', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),
                                ('SOFT Subscript +Support', 'STORAGE MG', 'INITIAL', '00000000', 'SWFT_SVC', 'GROSS', 'SBF'),

                                #  ELA  #
                                ('SOFT ELA', 'OTHERS', 'INITIAL', '00000000', 'ELA', 'NET', 'ELA'),
                                ('SOFT ELA', 'OTHERS', 'RENEWAL', '00000000', 'ELA', 'NET', 'ELA'),
                                #  HYBRYD  #
                                ('SOFT HYBD', 'CLOUD', 'INITIAL', '00000000', 'HYBD', 'NET', 'HYB'),
                                ('SOFT HYBD', 'OTHERS', 'INITIAL', '00000000', 'HYBD', 'NET', 'HYB')
                                ]

gn = pd.DataFrame.from_records(data, columns=['Activity 1', 'Activity 2', 'Activity 3', 'Intrastat Code','Gross/Net Classification', 'Gross/Net', 'SUBBRAND'])
gn['merge'] = gn['Activity 1'] + gn['Activity 2'] + gn['Activity 3']

# def person ():
#     person_data=[('Karol Kwiecień', "A86227"),('Katarzyna Czyż','A86361'),('Emil Twardowski','A93176'),('Paweł Czaja','A89264')]
#     pd.DataFrame.from_records(person_data, columns=['Name', 'ID'])
    # st.write(person_ID)

person_list={"Karol Kwiecień":'A86227','Katarzyna Czyż':"A86"}



# st.session_state['gvn']=gn
# st.session_state['person']=person
# st.write(st.session_state['gvn'])
# var1
# var2
# var3[0]

# btn=st.button('Run', type='primary')
