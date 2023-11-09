#import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
print('ok')

st.title('hello !')
uploaded_file=st.file_uploader('upload pricelist')

# st.set_page_config(page_title="Superstore",page_icon=":bar_chart:",layout="wide")
# st.title (":bar_chart:Sample Store")