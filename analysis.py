import streamlit as st
import pandas as pd
import boto3
from datetime import datetime

year_num, week_num, day_of_week = datetime.today().isocalendar() 

st.set_page_config(layout='wide')
st.title('Data Monitoring App')
col1, col2 = st.columns(2)
with col1:
    year = st.text_input(label='Year', value=year_num)
    environment = st.selectbox('Enviroment', options=['beta', 'prod'])
    num = st.selectbox('Number of rows to show:',
                options=[5, 10, 20])
    store = st.text_input(label='Store')
with col2:
    week = st.text_input(label='Week', value=week_num)
    script = st.selectbox('Script', options=['update', 'scrape'])
    head_tail = st.selectbox(
        'Top or Bottom', options=['top', 'bottom']
    )
    language = st.selectbox(label='Language', options=['all', 'en', 'fr'])

run_button = st.button('Run', use_container_width=True, type='primary')

AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']
BUCKET = st.secrets['BUCKET']

if 'session' not in st.session_state:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    s3 = session.resource('s3')
    st.session_state['s3'] = s3


def process_key(key: str):
    st.success(f'Key: {key}')
    st.session_state['s3'].Bucket(BUCKET).Object(key).download_file('data.json')
    df = pd.read_json('data.json')
    if head_tail == 'top':
        st.dataframe(df.head(num))
    else:
        st.dataframe(df.tail(num))

if run_button:
    bucket = st.session_state['s3'].Bucket('eezly-weekly-scripts')
    objects = list(bucket.objects.filter(Prefix=f'{environment}/{script}/{year}/{week}').all())
    obj_keys = [obj.key for obj in objects]
    with st.spinner():
        for key in obj_keys:
            language_match = (language == 'all') or key.endswith(f'{language}.json')
            store_match = (not store) or f'{store}_' in key
            if language_match and store_match:
                process_key(key)
        
            
                  

