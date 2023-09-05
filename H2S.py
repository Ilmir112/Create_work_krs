import openpyxl



def calc_SNPKH(self, wb2):

    import open_pz
    head_column_additional = open_pz.Create_PZ.head_column_additional
    shoe_column_additional = open_pz.Create_PZ.shoe_column_additional
    column_additional_diametr = open_pz.Create_PZ.column_additional_diametr
    column_additional_wall_thickness = open_pz.Create_PZ.column_additional_wall_thickness
    column_additional_diametr = open_pz.Create_PZ.column_additional_diametr
    column_additional_wall_thickness = open_pz.Create_PZ.column_additional_wall_thickness
    data_column_additional = open_pz.Create_PZ.data_column_additional
    bottomhole_artificial = open_pz.Create_PZ.bottomhole_artificial

    SNPKH = [
        ['Расчет расхода нейтрализатора сероводорода на модификацию раствора глушения*', None, None, None, None, None,
         None,
         None, None, None, None, None],
        ['Масса нейтрализатора сероводорода - по результатам расчета*', None, None, None, None, None, None, None,
         None, None, None, None],
        ['Объем раствора глушения - по объему скважины от устья до забоя', None, None, None, None, None, None, None,
         None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        ['№', 'Параметр', None, 'Результат расчета', None, None, None, None, None, None, None, None],
        [1, 'Параметры скважины', None, 'скв. 1', None, None, None, None, None, None, None, None],
        [1.1, 'Забой скважины', 'м', open_pz.Create_PZ.bottomhole_artificial, 'формула', None, None, None, None, None,
         None, None],
        [1.2, 'текущий забой', 'м', 1350.4, 'ввод', None, None, None, None, None, None, None],
        [1.3, 'Диаметр ЭК (ступень 1 верхняя)', 'мм', 114, 'ввод', None, None, None, None, None, None, None],
        ['1.3.1.', 'Толщина стенки ЭК (ступень 1 верхняя)', 'мм', 7.7, 'ввод', None, None, None, None, None, None,
         None],
        ['1.3.2.', 'Длина подвески ЭК (ступень 1 верхняя)', 'м', 1350.4, 'ввод', None, None, None, None, None, None,
         None],
        ['1.3.3.', 'Диаметр ЭК (ступень 2 хвостовик)', 'мм', 0, 'ввод', None, None, None, None, None, None, None],
        ['1.3.4.', 'Толщина стенки ЭК (ступень 2 хвостовик)', 'м', 0, 'ввод', None, None, None, None, None, None, None],
        ['1.3.5.', 'Длина подвески ЭК (ступень 2 хвостовик)', 'м', 0, 'ввод', None, None, None, None, None, None, None],
        ['1.3.6.', 'Глубина "головы" (ступень 2 хвостовик)', 'м', 0, 'ввод', None, None, None, None, None, None, None],
        ['1.3.7.', 'Глубина "башмака" (ступень 2 хвостовик)', 'м', 0, 'формула', None, None, None, None, None, None,
         None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [2, 'Параметры ГНО', None, None, None, None, None, None, None, None, None, None],
        ['2.1.', 'Общая глубина подвески НКТ', 'м', 1340.8, 'формула', None, None, None, None, None, None, None],
        ['1.4.1', 'Толщина стенки подвески НКТ (ступень 1 верхняя)', 'мм', 5.5, 'ввод', None, None, None, None, None,
         None, None],
        ['1.4.2', 'Внешний диаметр подвески НКТ (ступень 1 верхняя)', 'мм', 73, 'ввод', None, None, None, None, None,
         None, None],
        ['1.4.3', 'Длина подвески НКТ (ступень 1 верхняя)', 'м', None, 'ввод', None, None, None, None, None, None,
         None],
        ['1.4.4', 'Толщина стенки подвески НКТ (ступень 2 нижняя)', 'мм', None, 'ввод', None, None, None, None, None,
         None, None],
        ['1.4.5', 'Внешний диаметр подвески НКТ (ступень 2 нижняя)', 'мм', None, 'ввод', None, None, None, None, None,
         None, None],
        ['1.4.6', 'Длина подвески НКТ (ступень 2 нижняя)', 'м', None, 'ввод', None, None, None, None, None, None, None],
        ['2.2', 'Общая глубина подвески штанг', 'м', 1340.8, 'формула', None, None, None, None, None, None, None],
        ['2.2.1.', 'Длина штанг 25 мм', 'м', None, 'ввод', None, None, None, None, None, None, None],
        ['2.2.2.', 'Длина штанг 22 мм', 'м', None, 'ввод', None, None, None, None, None, None, None],
        ['2.2.3.', 'Длина штанг 19 мм', 'м', None, 'ввод', None, None, None, None, None, None, None],
        [3, 'Расчеты емкости', None, None, None, None, None, None, None, None, None, None],
        [3.1, 'Удельный  внутренний объем ЭК', 'дм3/м', 7.6317386, 'формула', None, None, None, None, None, None, None],
        [3.2, 'Удельный  внутренний объем хвостовика', 'дм3/м', 0, 'формула', None, None, None, None, None, None, None],
        [3.3, 'Объем жидкости под ГНО, в т.ч.:', 'м3', 0.07326469056000103, 'формула', None, None, None, None, None,
         None, None],
        ['3.3.1.', 'Объем скважины', 'м3', 10.30589980544, 'формула', None, None, None, None, None, None, None],
        ['3.3.1.', 'Удельное водоизмещение подвески НКТ (ступень 1 верхняя)', 'дм3/м', 1.1657249999999995, 'формула',
         None, None, None,
         None, None, None, None],
        ['3.3.2.', 'Удельное водоизмещение подвески НКТ  (ступень 2 нижняя)', 'дм3/м', 0, 'формула', None, None, None,
         None,
         None, None, None],
        ['3.3.3.', 'Водоизмещение подвески НКТ (объем жидкости притока при СПО)', 'м3/СПО', 0, 'формула', None, None,
         None,
         None, None, None, None],
        ['3.3.4.', 'Водоизмещение подвески штанг (объем жидкости притока при СПО)', 'м3/СПО', 0, 'формула', None, None,
         None, None,
         None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [4, 'Параметры добываемой жидкости и газа', None, None, None, None, None, None, None, None, None, None],
        [4.1, 'Газосодержание нефти', 'м3/тонну', 5.9, 'ввод', None, None, None, None, None, None, None],
        [4.2, 'Содержание сероводорода в газе (по данным проекта разработки)', '% (об)', 0.3, 'ввод', None, None, None,
         None, None, None, None],
        [4.3, 'Обводенность продукции', '% (масс.)', 80.5, 'ввод', None, None, None, None, None, None, None],
        [4.4, 'Содержание сероводорода в пластовом флюиде (устьевая проба, вода+нефть)', 'мг/дм3', 50, 'ввод', None,
         None,
         None, None, None, None, None],
        [4.5, 'Плотность воды', 'г/см3', 1.17, 'ввод', None, None, None, None, None, None, None],
        [4.6, 'Плотность нефти', 'г/см3', 0.9, 'ввод', None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [5, 'Расчет массы сероводорода в жидкости притока (в объеме водоизмещения подвески НКТ и штанг)', None, None,
         None,
         None, None, None, None, None, None, None],
        [5.1, 'Масса нефти ', 'т', 0, 'формула', None, None, None, None, None, None, None],
        [5.2, 'Объем сероводорода, м3', 'м3', 0, 'формула', None, None, None, None, None, None, None],
        [5.3, 'Масса сероводорода в нефти (выделяющаяся в газовую фазу при снижении давления)', 'г', 0, 'формула', None,
         None, None, None, None, None, None],
        [5.4, 'Масса сероводорода в жидкости (остаточная растворенная часть)', 'г', 0, 'формула', None, None,
         None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [6, 'Расчет массы сероводорода в поднасосной жидкости (в объеме скважины под ГНО)', None, None, None,
         None, None, None, None, None, None, None],
        [6.1, 'Масса нефти ', 'т', 0.01285795319328018, 'формула', None, None, None, None, None, None, None],
        [6.2, 'Объем сероводорода, м3', 'м3', 0.00022758577152105915, 'формула', None, None, None, None, None, None,
         None],
        [6.3, 'Масса сероводорода в нефти (доля, выделяющаяся в газовую фазу при снижении давления)', 'г',
         0.34949937812628773,
         'формула', None, None, None, None, None, None, None],
        [6.4, 'Масса сероводорода в жидкости (остаточная растворенная часть)', 'г', 3.6632345280000513, 'формула', None,
         None,
         None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [7, 'Масса сероводорода общая', 'г', 4.012733906126339, 'формула', None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [8, 'Параметр нейтрализатора сероводорода', None, None, None, None, None, None, None, None, None, None],
        [8.1, 'Емкость реагента по сероводороду (определяется по результатам ЛИ конкретной марки)', 'г/г H2S', 24,
         'ввод', None,
         None, None, None, None, None, None],
        [8.2, 'Плотность товарной формы (марки) реагента (по ТУ)', 'г/см3', 1.065, 'ввод', None, None, None, None, None,
         None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [9, 'Результат расчета расхода нейтрализатора сероводорода', None, None, None, None, None, None, None, None,
         None, None],
        [9.1, 'Расчетная масса реагента', 'кг', 0.09630561374703214, 'формула', None, None, None, None, None, None,
         None],
        [9.2, 'Коэффициент запаса по реагенту (решение ОГ)', 'крат', 1.25, 'ввод', None, None, None, None, None, None,
         None],
        [9.3, 'Масса реагента с запасом', 'кг', 0.12038201718379019, 'формула', None, None, None, None, None, None,
         None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [10, 'Удельный расход нейтрализатора сероводорода в растворе глушения', None, None, None, None, None, None,
         None, None, None, None],
        [10.1, 'Удельный массовый расход нейтрализатора сероводорода ', 'кг/м3', 0.01168088371286573, 'формула', None,
         None, None, None, None, None, None],
        [10.2, 'Удельный объемный расход нейтрализатора сероводорода ', 'м3/м3', 0.010967965927573455, 'формула', None,
         None, None, None, None, None, None],
        [
            'Примечание: * - расчет приблизительный, поскольку нет информации по содержанию H2S в каждой фазе (вода, нефть, газ) в одинаковых условиях',
            None,
            None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        ['Ячейки для заполнения данными параметров скважины', None, None, None, None, None, None, None, None, None,
         None, None],
        [None, 'По данным конструкции скважины', None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, 'По данным лабораторных исследований марки нейтрализатора сероводорода', None, None, None, None, None,
         None, None,
         None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None]]


    for row in range(1, 84):
        for col in range(1, 12):
            open_pz.Create_PZ.ws3.cell(row = row, column = col).value = SNPKH[row-1][col -1 ]










