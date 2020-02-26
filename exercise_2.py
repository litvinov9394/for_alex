# ЗАДАНИЕ 2

import pandas as pd
from sqlalchemy import create_engine

# Подключаемся к базе данных
try:
    connect = create_engine('postgres://gdpnholffmuoje:58f39f2f092ceee47d64b9203b6a561bb780958ce44673032c9de6aa1aad4951@ec2-46-137-156-205.eu-west-1.compute.amazonaws.com:5432/d8i67gibqaftom')
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