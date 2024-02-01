import etl_market_caps_myfunc as fun


logfile="code_log.txt"
url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
csv_file="./Largest_banks_data.csv"
db_name="Banks.db"
table_name="Largest_banks"


# market_caps_table = fun.extract(url=url)

# Alternative way by using BeautifulSoup
market_caps_table = fun.extract_v2(url=url)

market_caps_table = fun.transform(df=market_caps_table)

fun.load_to_csv(df=market_caps_table, csv_file=csv_file)

fun.load_to_db(df=market_caps_table, db_name=db_name, table_name=table_name)

fun.load_from_db(df=market_caps_table, db_name=db_name, query=f"SELECT * from {table_name}")


with open(logfile, "r") as f:
    all_logs = f.readlines()
    for log in all_logs:
        print(log)