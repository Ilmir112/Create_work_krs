from open_pz import CreatePZ
merged_segments = [[410, 530], (2319, 2407), (2412, 2437), (2444, 2447)]
CreatePZ.head_column_additional = 1983
template = 'ПСШ ДП'
print(len(merged_segments))
print(f'вид шаблона - {template}')
merged_segments_new = []

for interval in merged_segments:
    if template in ['ПСШ ЭК', 'ПСШ ЭК без хвост', 'ПСШ ЭК открытый ствол']:
        merged_segments_new = merged_segments
    elif template in ['ПСШ ДП', 'ПСШ ДП без хвост',
                      'ПСШ СКМ в доп колонне + открытый ствол']:
        if interval[0] > float(CreatePZ.head_column_additional) and interval[1] > float(
                CreatePZ.head_column_additional):
            merged_segments_new.append(interval)

        elif interval[0] < float(CreatePZ.head_column_additional) and interval[1] > float(
                CreatePZ.head_column_additional):

            merged_segments_new.append((CreatePZ.head_column_additional+2, interval[1]))
            # print(f'2 {interval, merged_segments}')
    elif template in ['ПСШ Доп колонна СКМ в основной колонне']:
        if interval[0] < float(CreatePZ.head_column_additional) and interval[1] < float(CreatePZ.head_column_additional):
            merged_segments_new.append(interval)

        elif interval[0] < float(CreatePZ.head_column_additional) and interval[1] > float(CreatePZ.head_column_additional):
            # merged_segments.remove(interval)
            merged_segments_new.append((interval[0], CreatePZ.head_column_additional - 2))
            # print(f'4 {interval, merged_segments}')


print(f'5 {merged_segments_new}')

