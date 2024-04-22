import os

# Список папок и файлов для добавления
data_to_add = [
    ('data_base/data_base_well/database_well.py', '.'),  # Пример включения другой зависимости
    ('data_base/data_base_well/databaseWell.db', '.'),
    ('data_base/work_with_base.py', '.'),
    ('data_base/database_without_juming.db', '.'),
    ('gnkt_data/gnkt_data.py', '.'),
    ('imageFiles', '.'),
    ('users/login_users.py', '.'),
    ('work_py/acid_paker.py', '.'),
    ('work_py/acids.py', '.'),
    ('work_py/advanted_file.py', '.'),
    ('work_py/alone_oreration.py', '.'),
    ('work_py/calc_fond_nkt.py', '.'),
    ('work_py/change_fluid.py', '.'),
    ('work_py/claySolution.py', '.'),
    ('work_py/data_informations.py', '.'),
    ('work_py/descent_gno.py', '.'),
    ('work_py/dop_plan_py.py', '.'),
    ('work_py/drilling.py', '.'),
    ('work_py/emergencyWork.py', '.'),
    ('work_py/geophysic.py', '.'),
    ('work_py/gnkt_frez.py', '.'),
    ('work_py/gnkt_grp.py', '.'),
    ('work_py/gpp.py', '.'),
    ('work_py/grp.py', '.'),
    ('work_py/kompress.py', '.'),
    ('work_py/leakage_column.py', '.'),
    ('work_py/mkp.py', '.'),
    ('work_py/mouse.py', '.'),
    ('work_py/opressovka.py', '.'),
    ('work_py/perforation.py', '.'),
    ('work_py/raiding.py', '.'),
    ('work_py/rgdVcht.py', '.'),
    ('work_py/rir.py', '.'),
    ('work_py/sand_filling.py', '.'),
    ('work_py/swabbing.py', '.'),
    ('work_py/template_without_skm.py', '.'),
    ('work_py/template_work.py', '.'),
    ('work_py/vp_cm.py', '.'),
    ('block_name.py', '.'),
    ('category_correct.py', '.'),
    ('cdng.py', '.'),
    ('data_correct.py', '.'),
    ('data_correct_position_people.py', '.'),
    ('find.py', '.'),
    ('gnkt_after_grp.py', '.'),
    ('gnkt_opz.py', '.'),
    ('H2S.py', '.'),
    ('krs.py', '.'),
    ('main.py', '.'),
    ('open_pz.py', '.'),
    ('perforation_correct.py', '.'),
    ('perforation_correct_gnkt_frez.py', '.'),
    ('plan.py', '.'),
    ('plan23.py', '.'),
    ('podpisant.json', '.'),
    ('proverka.py', '.'),
    ('selectPlast.py', '.'),
    ('well_data.py', '.'),
    ('work_json.py', '.'),
    ('application_gis.py', '.'),
    ('application_pvr.py', '.'),
]

# Создаем команду PyInstaller
command = ["pyinstaller --onefile"]

# Добавляем опции --add-data для каждого элемента в списке
for data in data_to_add:
    command.extend([f"--add-data {data[0]}:{data[0]}"])


# Добавляем основной скрипт Python
command.append("main.py")
print(' '.join(command))
# # Выполняем команду PyInstaller
# os.system(" ".join(command))
