from pandas_datareader.data import DataReader
import datetime as dt
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import psycopg2
import boto3

# Start and End dates
dt_start = dt.datetime(2019, 1,1)
dt_end = dt.datetime.now() - dt.timedelta(days=1)

def postgre_connection():
    #sudo apt install python3-dev libpq-dev
    #pip3 install psycopg2
    ENDPOINT = "db-test.cqwrfgluw2ec.us-east-1.rds.amazonaws.com"
    USER = "postgres"
    PORT = "5432"
    REGION = "us-east-1a"
    DBNAME = "bd-st-itba"

    # gets the credentials from .aws/credentials
    session = boto3.Session(profile_name='default')
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token,
                                sslrootcert="SSLCERTIFICATE")
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        st.markdown(query_results)
    except Exception as e:
        st.warning("Database connection failed due to {}".format(e))

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
                      'category':'Tecnol??gicas'},
              'AMZN':{'name':'Amazon',
                      'category':'E-commerces'},
              'BABA':{'name':'Alibaba',
                      'category':'E-commerces'},
              'NFLX':{'name':'Netflix',
                      'category':'Otros'},
              'MSFT':{'name':'Microsoft',
                      'category':'Tecnol??gicas'},
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
                       'category':'Tecnol??gicas'},
              'IBM':{'name':'Ibm',
                     'category':'Tecnol??gicas'},
              'INTC':{'name':'Intel',
                      'category':'Tecnol??gicas'},
              'NDAQ':{'name':'Nasdaq',
                      'category':'Otros'},
              'ORCL':{'name':'Oracle',
                      'category':'Tecnol??gicas'},
              'JP':{'name':'JP Morgan',
                    'category':'Bancos'}}
postgre_connection()

categories = ['E-commerces', 'Tecnol??gicas', 'Bancos', 'Otros']
st_categories = {cat:st.sidebar.checkbox(f'{cat}', False) for cat in categories}

st_graphics = {features['name']: create_graphic(stock, features) for stock, features in stock_dict.items()
               if features['category'] in [cat for cat, bool in st_categories.items() if bool==True]}

filter = st.sidebar.text_input('S??mbolo')
if filter:
    try:
        create_graphic(filter,filter)
    except:
        st.warning('El s??mbolo ingresado no existe')


