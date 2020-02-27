# ЗАДАНИЕ 1

import requests
import pandas as pd
import json
from datetime import datetime
pd.options.display.max_rows = 100

# подключение
response = requests.post('http://84.201.129.203:4545/get_structure_course')
if response.status_code != 200:
    print(f'Response status_code: {response.status_code}')
else:
    print(f'Response status_code: {response.status_code}')

    # редко, но иногда вылетает ошибка JSONDecodeError, по причине пустого ответа от сервера или "битого" json
    response_json = response.json()

    # JSON в Pandas
    table_pandas = pd.read_json(json.dumps(response_json))
    table_pandas_new = table_pandas['blocks']

    # создаем новый DafeFrame для Курсов
    kurs = pd.DataFrame({
        'number': [],
        'display_name': [],
        'block_id': []
    })

    # создаем новый DafeFrame для Children Курсов
    children_kurs = pd.DataFrame({
        'number_kursa': [],
        'display_name': [],
        'block_id': []
    })

    # Перебираем JSON ответ, записываем нужные столбцы в новый DateFrame
    for row in range(len(table_pandas_new.index)):
        kurs = kurs.append([{'number': f'{row}', 'display_name': f'{table_pandas_new[row]["display_name"].strip()}', 'block_id': f'{table_pandas_new[row]["block_id"]}'}])
        # проверяем если ли children у данного курса
        try:
            # перебираем всех children которые записаны в курс
            for row_children in range(len(table_pandas_new[row]['children'])):
                # индефикатор записаный в children в данном курсе
                children = table_pandas_new[row]['children'][row_children]
                # записываем полную информацию по индефикатору о children в DateFrame Children
                children_kurs = children_kurs.append([{'number_kursa': f'{row}', 'display_name': f'{table_pandas["blocks"][children]["display_name"].strip()}', 'block_id': f'{table_pandas["blocks"][children]["block_id"]}'}])
        except KeyError:
            pass

    # сортируем Курсы по display_name
    kurs = kurs.sort_values('display_name')

    # создаем новый DafeFrame для объеденения Курсов с их Children
    kurs_bd = pd.DataFrame({
        'display_name': [],
        'block_id': []
    })

    # заполняем новый DateFrame
    for row in range(len(kurs.index)):
        kurs_bd = kurs_bd.append([{'display_name': f'{kurs.iloc[row]["display_name"]}', 'block_id': f'{kurs.iloc[row]["block_id"]}'}])

        # фильтруем и делаем выборку всех children которые есть в данном курсе
        children = children_kurs[children_kurs.number_kursa == kurs.iloc[row]["number"]][['display_name', 'block_id']]

        # сортируем Children по display_name
        children = children.sort_values('display_name')

        # записываем Children для данного курса
        for row_children in range(len(children.index)):
            kurs_bd = kurs_bd.append([{'display_name': f'{children.iloc[row_children]["display_name"]}', 'block_id': f'{children.iloc[row_children]["block_id"]}'}])

    # записываем последнее время обновления данных
    last_update_date = datetime.strftime(datetime.now(), "%H:%M %d.%m.%Y")
    kurs_bd = kurs_bd.append([{'display_name':'ВРЕМЯ ОБНОВЛЕНИЯ ДАННЫХ:', 'block_id': f'{last_update_date}'}])

    # выводим курсы с их children (50 шт)
    print(kurs_bd.head(50))

    # сохраняем для записи в базу для задания 2
    kurs_bd.to_csv('C:\\kurs.csv', encoding='utf-8', index_label=False, index=False)