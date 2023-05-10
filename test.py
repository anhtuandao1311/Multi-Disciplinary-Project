# from io import BytesIO
# import pandas as pd
# import streamlit as st
# import requests



# response = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSyeT46fqUWeI0_mNwttYawLnTo5nuI_ivXmiFjFk6nNofUZ2VbVhJevgf-uY3HvBv9mkH-kJCRTtPY/pub?gid=0&single=true&output=csv')
# assert response.status_code == 200, 'Wrong status code'


# st.set_page_config(
#     page_title="Real-Time Data Science Dashboard",
#     page_icon="✅",
#     layout="wide",
# )

# dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# # dashboard title
# st.title("Real-Time / Live Data Science Dashboard")


# @st.experimental_memo
# def get_data() -> pd.DataFrame:
#     return pd.read_csv(BytesIO(response.content), index_col=0)


# df = get_data()
# with st.container():
#     st.dataframe(df)



from io import BytesIO
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time


# Ultility function to graph timeline

# Set the auto-refresh interval (in seconds)
refresh_interval = 10

# Display a countdown timer until the next auto-refresh


# Force a rerun (refresh) of the app after the countdown


def graph_timeline(df: pd.DataFrame):
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby('date')[['gas', 'fire']].mean().reset_index()

    gas_trace = go.Scatter(
        x=df.date,
        y=df.gas,
        name='Gas',
        line=dict(color='#1DB954', width=3))

    temp_trace = go.Scatter(
        x=df.date,
        y=df.fire,
        name="Temperature",
        line=dict(color='#FF8C00', width=3))

    fig = go.Figure(data=[gas_trace, temp_trace])
    fig.update_layout(
        width=800,
        height=600,
        title='Gas and Temperature Observations')

    fig.add_shape(
        type="line",
        yref="y",
        y0=600,
        y1=600,
        x0=df.date.min(),
        x1=df.date.max(),
        line=dict(color="red", dash="dash"),
        name="Threshold",
    )

    fig.update_yaxes(title='Observed Value')
    fig.update_xaxes(title='Date')
    return fig


# Main page
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)


response = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSyeT46fqUWeI0_mNwttYawLnTo5nuI_ivXmiFjFk6nNofUZ2VbVhJevgf-uY3HvBv9mkH-kJCRTtPY/pub?gid=0&single=true&output=csv')
assert response.status_code == 200, 'Wrong status code'

# Title and member
st.markdown("""<h1 style='
                font-family: Recoleta-Regular; font-weight: 400; text-align: center;
                font-size: 3.5rem'>Fire and Smoke Alarm System</h1>""",
            unsafe_allow_html=True)



dataset_url = BytesIO(response.content)



def get_data() -> pd.DataFrame:
    df = pd.read_csv(dataset_url, header=None)
    df = df.rename(columns={0: "date", 1: "name", 2: "fire", 3: "gas"})
    return df


df = get_data()
df=df.drop(columns=['name'])
st.write("##")
with st.container():
    left, right = st.columns([1, 2])
    with left:
        st.header("Data observed")
        st.dataframe(df)
    with right:
        fig = graph_timeline(df)
        st.plotly_chart(fig, True)


time.sleep(10)
st.experimental_rerun()
