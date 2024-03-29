from collections import namedtuple

Saddles = namedtuple('Saddles', ['saddle', 'ball'])

Gnkt_data = namedtuple("Gnkt_data", ["gnkt_length", "diametr_length", "pvo"])


gnkt_2 = Gnkt_data(2200, 38, 115)
gnkt_1 = Gnkt_data(3200, 38, 166)

dict_saddles = {
    'НТЦ ЗЭРС': {"ФПЗН1.114": {
                '114/70А': Saddles('67.90', '70.92'),
                '114/67А': Saddles('64.65', '67.57'),
                '114/64А': Saddles('61.5', '64.32'),
                '114/61А': Saddles('58.5', '61.19'),
                '114/58А': Saddles('55.55', '58.17'),
                '114/55А': Saddles('52.75', '55.25'),
                '114/52А': Saddles('49.8', '52.43'),
                '114/49А': Saddles('47.2', '49.71'),
                '114/47А': Saddles('45.06', '47.07'),
                '114/45А': Saddles('43.03', '45.02')
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
        '102/45': Saddles('43.03', '45.02')
    }
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



# print(dict_saddles)
