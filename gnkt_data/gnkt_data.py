import sqlite3
from datetime import datetime
from collections import namedtuple

Saddles = namedtuple('Saddles', ['saddle', 'ball'])

Gnkt_data = namedtuple("Gnkt_data", ["gnkt_length", "diametr_length", "iznos", "pipe_mileage", 'pipe_fatigue', "pvo"])



gnkt_2 = Gnkt_data(2200, 38, 20, 35025, 25, 115)
gnkt_1 = Gnkt_data(3200, 38, 20, 42006, 25, 166)
gnkt_dict = {}

gnkt_dict["Ойл-сервис"] = ['', 'ГНКТ №1', 'ГНКТ №2']

dict_saddles = {
    'НТЦ ЗЭРС': {
        "ФПЗН1.114": {
                '114/70А': Saddles('67.90', '70.92'),
                '114/67А': Saddles('64.65', '67.57'),
                '114/64А': Saddles('61.5', '64.32'),
                '114/61А': Saddles('58.5', '61.19'),
                '114/58А': Saddles('55.55', '58.17'),
                '114/55А': Saddles('52.75', '55.25'),
                '114/52А': Saddles('49.8', '52.43'),
                '114/49А': Saddles('47.2', '49.71'),
                '114/47А': Saddles('45.06', '47.07'),
                '114/45А': Saddles('43.03', '45.02'),
                '114': Saddles('25', '32')
        },
    "ФПЗН.102": {
        '102/70': Saddles('67.90', '70.92'),
        '102/67': Saddles('64.65', '67.57'),
        '102/64': Saddles('61.5', '64.32'),
        '102/61': Saddles('58.5', '61.19'),
        '102/58': Saddles('55.55', '58.17'),
        '102/55': Saddles('52.75', '55.25'),
        '102/52': Saddles('49.8', '52.43'),
        '102/49': Saddles('47.2', '49.71'),
        '102/47': Saddles('45.06', '47.07'),
        '102/45': Saddles('43.03', '45.02')}
    },
    'Зенит':
        {"ФПЗН1.114":
             {'1.952"': Saddles('48.1', '49,6'),
              '2,022"': Saddles('49.8', '51.4'),
              '2,092"': Saddles('51.6', '53.1'),
              '2,162"': Saddles('53.4', '54.9'),
              '114/58А': Saddles('55.2', '56.9'),
              '2,322"': Saddles('57.2', '59'),
              '2,402"': Saddles('59.2', '61'),
              '2,487"': Saddles('61.3', '63.2'),
              '2,577"': Saddles('63.4', '65.5'),
              '2,667"': Saddles('65.7', '67.7'),
              '2,757"': Saddles('68', '70'),
              '2,547"': Saddles('70.3', '72.2')
              }
         },

    'Барбус':
        {"гидравлич":
             {'51,36t20': Saddles('48.86', '51.36'),
              '54,00t20': Saddles('51.5', '54'),
              '56,65t20': Saddles('54.15', '56.65'),
              '59,80t20': Saddles('51.5', '54'),
              '62,95t20': Saddles('56.8', '59.8'),
              '66,10t20': Saddles('63.1', '66.1')
              }

         }
}

def read_database_gnkt(contractor, gnkt_number):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('data_base\data_base_gnkt\gnkt_base.dp')
    cursor = conn.cursor()

    if 'ойл-сервис' in contractor.lower():
        contractor = 'oil_service'

    cursor.execute(f"SELECT * FROM gnkt_{contractor} WHERE gnkt_number =?", (gnkt_number,))

    result = cursor.fetchall()
    print(result)
    well_previus_list = [(well[8], well[9]) for well in result]
    well_previus_list = sorted(well_previus_list, key=lambda x:  datetime.strptime(x[1], "%d.%m.%Y"))
    well_previus_list = list(filter(lambda x: x[0], well_previus_list))
    print(f'список ремонтов {result}')
    # Закрытие соединения с базой данных
    conn.close()

    return well_previus_list


def insert_data_base_gnkt(contractor, gnkt_number, gnkt_length, diametr_length,
                     iznos, pipe_mileage, pipe_fatigue, pvo, previous_well):

    # Подключение к базе данных SQLite
    conn = sqlite3.connect('data_base\data_base_gnkt\gnkt_base.dp')
    cursor = conn.cursor()

    if 'ойл-сервис' in contractor.lower():
        contractor = 'oilservice'

    current_datetime = datetime.today().strftime('%d.%m.%Y')

    data_values = (gnkt_number, '1963', gnkt_length, diametr_length, iznos,
                   pipe_mileage, pipe_fatigue, pvo, current_datetime, previous_well)

    # Подготовленный запрос для вставки данных с параметрами
    query = f"INSERT INTO gnkt_{contractor} " \
            f"(gnkt_number, well_number, length_gnkt, diameter_gnkt, wear_gnkt, mileage_gnkt, tubing_fatigue, " \
            f"pvo_number, today, previous_well) " \
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Выполнение запроса с использованием параметров
    cursor.execute(query, data_values)

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()
def create_data_base(contractor, gnkt_number):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('D:\python\Create_work_krs\data_base\data_base_gnkt\gnkt_base.dp')
    cursor = conn.cursor()
    if 'ойл-сервис' in contractor.lower():
        contractor = 'oil_service'

        # Удаление всех данных из таблицы
        cursor.execute(f"DROP TABLE gnkt_{contractor}")

    # Создание таблицы в базе данных
    cursor.execute(f'CREATE TABLE IF NOT EXISTS gnkt_{contractor}'
                   f'(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   f'gnkt_number INT NOT NULL,'
                   f'well_number TEXT,'
                   f'length_gnkt INT NOT NULL, '
                   f'diameter_gnkt DECIMAL(10,2) NOT NULL,'
                   f'wear_gnkt DECIMAL(5,2) NOT NULL,'
                   f'mileage_gnkt DECIMAL(10,2) NOT NULL,'
                   f'tubing_fatigue TEXT NOT NULL,'
                   f'previus_well TEXT NOT NULL,'
                   f'today TEXT NOT NULL,'
                   f'pvo_number INT NOT NULL)'
                   )
    Gnkt_data = namedtuple("Gnkt_data",
                           ["gnkt_length", "diametr_length", "iznos", "pipe_mileage", 'pipe_fatigue',
                            "pvo"])
    gnkt_2 = Gnkt_data(2200, 38, 20, 35025, '25', 115)
    gnkt_1 = Gnkt_data(3200, 38, 20, 42006, '25', 166)
    for ind, gnkt in enumerate([gnkt_1, gnkt_2]):
        if ind == 0:
            gnkt_number = 'ГНКТ №1'
        else:
            gnkt_number = 'ГНКТ №2'
        data_values = (gnkt_number, '1963', gnkt.gnkt_length, gnkt.diametr_length, gnkt.iznos,
                       gnkt.pipe_mileage, gnkt.pipe_fatigue, '1923', '26.04.2024', gnkt.pvo)
        # Подготовленный запрос для вставки данных с параметрами
        query = f"INSERT INTO gnkt_{contractor} " \
                f"(gnkt_number, well_number, length_gnkt, diameter_gnkt, wear_gnkt, mileage_gnkt, tubing_fatigue, previus_well, today, pvo_number) " \
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Выполнение запроса с использованием параметров
        cursor.execute(query, data_values)

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()
contractor = 'ООО "Ойл-Сервис'
print()
create_data_base(contractor, 'ГНКТ №1')
