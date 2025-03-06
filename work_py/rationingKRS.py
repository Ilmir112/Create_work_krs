# Подьем фондовых НКТ
def liftingGNO(dict_nkt):

    norm = 0.67 +0.05+0.17+0.33+0.07+0.5+.32
    for key, value in dict_nkt.items():
        if '48' in str(key) or '60' in str(key):
            norm += value/10 * 0.03
        elif '73' in str(key):
            norm += value/10 * 0.038
        elif '89' in str(key) or '102' in str(key):
            norm += value/10 * 0.048
    return round(norm, 2)
#Подьем труб
def lifting_nkt_norm(depth, layout):
    norm = 0.14 + 0.14
    if depth > 2000:
        norm += 1000 / 10 * 0.028
        # print(norm)
        norm += 1000 / 10 * 0.031
        # print(norm)
        norm += (depth - 2000) / 10 * 0.036
        # print(norm)
    if 1000 <= depth <= 2000:
        norm += 1000 / 10 * 0.028
        # print(norm)
        norm += (depth-1000)/10 * 0.031
        # print(norm)

    if depth < 1000:
        norm += depth / 10 * 0.028
    norm = norm * layout
    # print(norm,layout)
    norm += depth / 400 * 3.2 * 0.053
    # print(norm)
    return round(norm, 2)

#Спуск труб
def descentNKT_norm(depth, layout):
    norm = 0.17 + 1.25 + 0.14 +0.7
    norm += float(depth)/10 * 0.026
    norm *= layout
    return round(norm, 2)

def well_volume_norm(well_volume):
    norm = 0.48
    norm += well_volume * 0.033
    return round(norm,2)

# Нормы глушения скважины в зависимости от объема  скважины
def well_jamming_norm(volume_jamming):
    norm = 0.9 + 2 # ПЗР + тех отстой
    norm += volume_jamming * 0.08
    return round(norm,2)

# нормы спуска штанг
def descent_sucker_pod(depth):
    norm = 0.68+0.03+0.8+1.63+0.73
    norm += depth/10 *0.017
    return round(norm,2)

# Нормы подьема штанг
def lifting_sucker_rod(dict_sucker_rod):
    norm = 0
    for key, value in dict_sucker_rod.items():
        if '19' in str(key):
            norm += int(value/8) * 0.015
        elif '22' in str(key):
            norm += int(value/8) * 0.017
        elif '25' in str(key):
            norm += int(value/8) * 0.017
    norm += 0.8 + 0.13 +0.5 + 2 + 0.67 + 0.5
    return round(norm,2)