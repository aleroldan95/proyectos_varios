from pandas_datareader.data import DataReader
import datetime as dt
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import psycopg2
import boto3
import json

# Start and End dates
dt_start = dt.datetime(2019, 1,1)
dt_end = dt.datetime.now() - dt.timedelta(days=1)

def postgre_connection():
    #sudo apt install python3-dev libpq-dev
    #pip3 install psycopg2
    ENDPOINT = "db-st.cqwrfgluw2ec.us-east-1.rds.amazonaws.com"
    USER = "postgres"
    PORT = "5432"
    REGION = "us-east-1"
    DBNAME = "bd-st"


    # gets the credentials from .aws/credentials
    #session = boto3.Session(profile_name='LabInstanceProfile')
    #client = session.client('rds')


    #token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
    token = 'FwoGZXIvYXdzEAAaDI8vDFzWyYAu+/8jLyLNAURfxCc9rBzK85sjOIgB9es+0MPhtPEoSGDrpTLcn7LmPcWNAXISqmjoPyCTR9AIrr4+xrmeIFaHexpImUdUqEhUQqBbPPQvzLQBzjH0IB/fi6oULmaB4XHAkbKqH5R4bSrtwgtmCPstBHpdu9H7kQLoA1VqEinmDzLPPhCHJuLFww2Ozz2ZtRDxJAfD/sfLSbzY5NnEpyaMoUuQf6isQ22XyeVo8fjYWuvIxin2eGBq8Vwnm9VwtEOWumJtri/hGjqwlypOfQW1xKDYnGIojZmalwYyLWFSS1bJMj2jyNT7fDZvs3vuM/kqSvCSGlBZPEe83JLXZrwNR550DEncnp+JOw=='

    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token,
                                sslrootcert="SSLCERTIFICATE")
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        st.markdown(query_results)
    except Exception as e:
        st.warning("Database connection failed due to {}".format(e))

def send_sms(client_sns):


    # Send your sms message.
    #client_sns.publish(
    #    PhoneNumber="+541157231165",
    #    Message="Hello World!"
    #)
    #client_sns.publish(
    #    TopicArn='arn:aws:sns:us-east-1:240819703795:st-msm',
    #    Message="Hello World! 2"
    #)
    while True:
        response = sqs_client.receive_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/240819703795/ST-SQS",
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
        )
        if len(response.get('Messages', [])) > 0:

            for message in response.get("Messages", []):
                body = json.loads(message["Body"])

                client_sns.publish(
                    PhoneNumber="+541157231165",
                    Message=body['text']
                 )

                st.write(f"Message: {body['text']} - Sended")

                sqs_client.delete_message(
                    QueueUrl="https://sqs.us-east-1.amazonaws.com/240819703795/ST-SQS",
                    ReceiptHandle=message['ReceiptHandle'])

        else:
            break



def add_sqs(sqs_client, text_input, col2):

    message = {"text": f"{text_input}"}
    sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/240819703795/ST-SQS",
        MessageBody=json.dumps(message)
    )
    with col2:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.write('Enviado!')

def receive_message(sqs_client):

    response = sqs_client.receive_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/240819703795/ST-SQS",
        MaxNumberOfMessages=10,
        WaitTimeSeconds=5,
    )

    st.write(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        st.write(f"Message body: {json.loads(message_body)}")

def clean_messages(sqs_client):

    sqs_client.purge_queue(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/240819703795/ST-SQS",
    )

    st.write('All Cleaned!')

def send_email():
    ses_client = boto3.client(
        "ses",
        aws_access_key_id="ASIATQEPZB7ZZBSPL5C2",
        aws_secret_access_key="/BdXokboPveLCjuuYZvTK7skTQAUsyeEvIlFWQ9A",
        aws_session_token='FwoGZXIvYXdzEAAaDI8vDFzWyYAu+/8jLyLNAURfxCc9rBzK85sjOIgB9es+0MPhtPEoSGDrpTLcn7LmPcWNAXISqmjoPyCTR9AIrr4+xrmeIFaHexpImUdUqEhUQqBbPPQvzLQBzjH0IB/fi6oULmaB4XHAkbKqH5R4bSrtwgtmCPstBHpdu9H7kQLoA1VqEinmDzLPPhCHJuLFww2Ozz2ZtRDxJAfD/sfLSbzY5NnEpyaMoUuQf6isQ22XyeVo8fjYWuvIxin2eGBq8Vwnm9VwtEOWumJtri/hGjqwlypOfQW1xKDYnGIojZmalwYyLWFSS1bJMj2jyNT7fDZvs3vuM/kqSvCSGlBZPEe83JLXZrwNR550DEncnp+JOw==',

        region_name="us-east-1"
    )
    CHARSET = "UTF-8"

    ses_client.send_email(
        Destination={
            "ToAddresses": [
                "alejandro.d.roldan@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, world!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="abhishek@learnaws.org",
    )
    st.write('Enviado!')

def create_graphic(stock, title):
    # Download historical Adjusted Closing prices of Apple stock
    df = DataReader(stock, 'yahoo', dt_start, dt_end)  # ['Adj Close']
    # Index(['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close'], dtype='object')

    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in df.index]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])
                          ])

    fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            #dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2020-12-25", "2021-01-01"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
    #fig.update_xaxes(
    #    rangeselector=dict(
    #        buttons=list([
    #            dict(count=1, label="day", step="day", stepmode="todate"),
    #            dict(count=24, label="montly", step="month", stepmode="todate"),
    #            dict(count=1, label="year", step="year", stepmode="todate"),
    #            dict(step="all")
    #        ])
    #    ))
    fig.update_layout(
        title=f'{title}',
        yaxis_title=f'Stock [USD]',
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        # shapes = [dict(
        #    x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        #    line_width=2)],
        # annotations=[dict(
        #    x='2016-12-09', y=0.05, xref='x', yref='paper',
        #    showarrow=False, xanchor='left', text='Increase Period Begins')]
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=35  # top margin
        )
    )

    st.plotly_chart(fig, use_container_width=False, sharing='streamlit')

    st.markdown("---", unsafe_allow_html=True)

stock_dict = {'MELI':{'name':'Mercado Libre',
                      'category':'E-commerces'},
              'DESP':{'name':'Despegar',
                      'category':'Otros'},
              'AAPL':{'name':'Apple',
                      'category':'Tecnológicas'},
              'AMZN':{'name':'Amazon',
                      'category':'E-commerces'},
              'BABA':{'name':'Alibaba',
                      'category':'E-commerces'},
              'NFLX':{'name':'Netflix',
                      'category':'Otros'},
              'MSFT':{'name':'Microsoft',
                      'category':'Tecnológicas'},
              'YPF':{'name':'YPF',
                     'category':'Otros'},
              'BBAR':{'name':'Banco BBVA',
                      'category':'Bancos'},
              'GGAL':{'name':'Banco Galicia',
                      'category':'Bancos'},
              'TX':{'name':'Ternium',
                    'category':'Otros'},
              'AGRO':{'name':'AdecoAgro',
                      'category':'Otros'},
              'EBAY':{'name':'Ebay',
                      'category':'E-commerces'},
              'GOOGL':{'name':'Google',
                       'category':'Tecnológicas'},
              'IBM':{'name':'Ibm',
                     'category':'Tecnológicas'},
              'INTC':{'name':'Intel',
                      'category':'Tecnológicas'},
              'NDAQ':{'name':'Nasdaq',
                      'category':'Otros'},
              'ORCL':{'name':'Oracle',
                      'category':'Tecnológicas'},
              'JP':{'name':'JP Morgan',
                    'category':'Bancos'}}


#VARIALBES-----------------------------------------------------------------------------------------------------------------------

aws_access_key_id = "ASIATQEPZB7ZZBSPL5C2"
aws_secret_access_key = "/BdXokboPveLCjuuYZvTK7skTQAUsyeEvIlFWQ9A"
aws_session_token = 'FwoGZXIvYXdzEAAaDI8vDFzWyYAu+/8jLyLNAURfxCc9rBzK85sjOIgB9es+0MPhtPEoSGDrpTLcn7LmPcWNAXISqmjoPyCTR9AIrr4+xrmeIFaHexpImUdUqEhUQqBbPPQvzLQBzjH0IB/fi6oULmaB4XHAkbKqH5R4bSrtwgtmCPstBHpdu9H7kQLoA1VqEinmDzLPPhCHJuLFww2Ozz2ZtRDxJAfD/sfLSbzY5NnEpyaMoUuQf6isQ22XyeVo8fjYWuvIxin2eGBq8Vwnm9VwtEOWumJtri/hGjqwlypOfQW1xKDYnGIojZmalwYyLWFSS1bJMj2jyNT7fDZvs3vuM/kqSvCSGlBZPEe83JLXZrwNR550DEncnp+JOw=='

region_name = "us-east-1"

client_sns = boto3.client(
    "sns",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)
#SNS----------------------

if st.button('Test Connection'):
    postgre_connection()

col1, col2 = st.columns(2)
with col1:
    text_input = st.text_input('Añadir Mensaje')
    if st.button('Add Message to Queu'):
        add_sqs(sqs_client, text_input, col2)


#if st.button('Send EMAIL'):
#    send_email(aws_access_key_id, aws_secret_access_key, aws_session_token, region_name)


col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Messages'):
        receive_message(sqs_client)

with col2:
    if st.button('Send SMS'):
        send_sms(client_sns)

with col3:
    if st.button('Clean Queu'):
        clean_messages(sqs_client)


#STOCKS------------------------------

categories = ['E-commerces', 'Tecnológicas', 'Bancos', 'Otros']
st_categories = {cat:st.sidebar.checkbox(f'{cat}', False) for cat in categories}

st_graphics = {features['name']: create_graphic(stock, features) for stock, features in stock_dict.items()
               if features['category'] in [cat for cat, bool in st_categories.items() if bool==True]}

filter = st.sidebar.text_input('Símbolo')
if filter:
    try:
        create_graphic(filter,filter)
    except:
        st.warning('El símbolo ingresado no existe')


