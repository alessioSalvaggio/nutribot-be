import streamlit as st
from pymongo import MongoClient
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import ast

st.set_page_config(layout="wide")

# Configurazione MongoDB
mongo_conn_string = f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
client = MongoClient(mongo_conn_string)
db = client[os.getenv("MONGO_DB")]

# Recupera i log da MongoDB
logs = db["logs"].find().sort("ts", -1).to_list(length=None)  # Ordina per timestamp decrescente
n_logs = len(logs)

# Streamlit dashboard
st.title("Log Dashboard")

# Filtro per livello di log
log_levels = ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"]
selected_level = st.sidebar.selectbox("Seleziona il livello di log", log_levels)

# Filtro per granularità del tempo
time_granularity = st.sidebar.selectbox("Seleziona la granularità del tempo", ["Day", "Hour", "Minute"])

# Filtro per function
sorted_functions = sorted({k['function'] for k in logs})
selected_functions = st.sidebar.multiselect("Seleziona le funzioni:", sorted_functions)

# Filtro per intervallo di date
today = datetime.today()
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Data di inizio", value=today - timedelta(days=7))
end_date = col2.date_input("Data di fine", value=today)
# Filtro per intervallo di tempo
col1, col2 = st.sidebar.columns(2)
start_time = col1.time_input("Ora di inizio", value=datetime.min.time())
end_time = col2.time_input("Ora di fine", value=datetime.max.time())
# Combina data e ora
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)

# Free search text
search_text = st.sidebar.text_input("Cerca testo nei log")

# display the log number
st.sidebar.write(f"Numer of logs: {n_logs}")
 
# Converti i log filtrati in un DataFrame
df = pd.DataFrame(logs)
df.index = df['_id']
df['ts'] = pd.to_datetime(df['ts'])

# Filtra i log secodno i filtri precedenti
if selected_level != "ALL":
    df = df[df['level'] == selected_level]
df = df[(df['ts'] >= start_datetime) & (df['ts'] <= end_datetime)]
if search_text != "":
    df_idx = df.applymap(lambda cell: isinstance(cell, str) and search_text.lower() in cell.lower()).sum(axis=1)
    df = df[df_idx > 0]
if len(selected_functions) > 0:
    df = df[df["function"].isin(selected_functions)]


if len(df) > 0:
    # Raggruppa i log in base alla granularità del tempo selezionata
    if time_granularity == "Day":
        df['time_group'] = df['ts'].dt.date
    elif time_granularity == "Hour":
        df['time_group'] = df['ts'].dt.floor('H')
    elif time_granularity == "Minute":
        df['time_group'] = df['ts'].dt.floor('T')
    
    df_grouped = df.groupby(['time_group', 'level']).size().reset_index(name='count')
    color_map = {
        "INFO": "#1f77b4",
        "DEBUG": "green",
        "WARNING": "yellow",
        "ERROR": "red"
    }
    fig = px.line(
        df_grouped, 
        x='time_group', 
        y='count', 
        color='level', 
        title=f'Logs per {time_granularity.lower()}',
        markers=True,
        color_discrete_map=color_map  
    )
    st.plotly_chart(fig)
    
    # Visualizza i log come una tabella
    df = df[['ts', 'level' ,'environment', 'function', 'content']]
    st.dataframe(df)

    selected_log_index = st.selectbox("Seleziona un log per visualizzare i dettagli", df.index)
    if selected_log_index is not None:
        selected_log = [l for l in logs if l['_id'] == selected_log_index][0]
        try:
            selected_log['content'] = ast.literal_eval(selected_log['content'])
        except:
            pass
        st.write("Dettagli del log selezionato:")
        st.json(selected_log)
else:
    st.write(f"Nessun log di {selected_level} disponibile")