# ЗАДАНИЕ 2

import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Подключаемся к базе данных
try:
    connect = create_engine('mysql+pymysql://user2:qtybcgt++H6@84.201.129.203:32769/test')
except:
    print("Нет подключения")
else:
    print("Успешное подклчение к БД")
    kurs = pd.read_csv('C:\\kurs.csv', encoding='utf-8', index_col=False)
    print(kurs)

    # Записываем в базу
    print("\nЗапись в БД...")
    kurs.to_sql('kurs', con=connect, if_exists='replace', method='multi', index=False, index_label=None)
    print('\nDone!')