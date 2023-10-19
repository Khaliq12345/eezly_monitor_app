import streamlit as st
import pandas as pd
import boto3

st.set_page_config(layout='wide')
st.title('Data Monitoring App')
num = st.selectbox('Number of rows to show:',
             options=[5, 10, 20])
head_tail = st.selectbox(
    'Head or Tail', options=['head', 'tail']
)
run_button = st.button('Run')

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

if run_button:
    objects = list(st.session_state['s3'].Bucket(BUCKET).objects.all())
    obj_keys = [obj.key for obj in objects if '2023/42' in obj.key]
    with st.spinner():
      for key in obj_keys:
          st.success(f'Key: {key}')
          st.session_state['s3'].Bucket(BUCKET).Object(key).download_file('data.json')
          df = pd.read_json('data.json')
          if head_tail == 'head':
              st.dataframe(df.head(num))
          else:
              st.dataframe(df.tail(num))
