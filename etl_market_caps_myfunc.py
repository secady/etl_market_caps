from datetime import  datetime
import pandas as pd
import sqlite3


logfile="code_log.txt"

def log_progress(message, logfile=logfile):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(timestamp + ", " + message + "\n")


def extract(url):
    df = pd.read_html(url)[1]
    df = df.rename({"Bank name": "Name", "Market cap (US$ billion)": "MC_USD_Billion"}, axis=1)
    df = df.drop("Rank", axis=1)
    log_progress(message="Data has been extracted")
    return df


def transform(df):
    exchange_rate = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv")
    df["MC_GBP_Billion"] = df["MC_USD_Billion"].transform(lambda x: round(x*exchange_rate.loc[1, "Rate"], 2))
    df["MC_EUR_Billion"] = df["MC_USD_Billion"].transform(lambda x: round(x*exchange_rate.loc[0, "Rate"], 2))
    df["MC_INR_Billion"] = df["MC_USD_Billion"].transform(lambda x: round(x*exchange_rate.loc[2, "Rate"], 2))
    log_progress(message="Data has been transformed")
    return df


def load_to_csv(df, csv_file):
    df.to_csv(csv_file)
    log_progress(message="Data has been loaded to CSV")


def load_to_db(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
    conn.close()
    log_progress(message="Data has been loaded to DB")


def load_from_db(df, db_name, query):
    conn = sqlite3.connect(db_name)
    db_table = pd.read_sql(sql=query, con=conn)
    conn.close()
    log_progress(message="Data on DB has been checked")
    return db_table