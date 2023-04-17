import csv
from datetime import datetime

import psycopg2
from django.http import HttpResponse
from docx import Document

from .models import SecondOrdersModel, MainOrders


class SendSqlReq:

    def __init__(self, *args):
        self.conn = psycopg2.connect(f"dbname= user= password=AxqwKNn4")
        self.curs = self.conn.cursor()
        self.drone_id = args

    @property
    def standart_req(self):
        self.curs.execute("SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones")
        res = self.curs.fetchall()
        return res

    @property
    def newest_req(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY id DESC")
        res = self.curs.fetchall()
        return res

    @property
    def oldest_req(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY dt_first ")
        res = self.curs.fetchall()
        return res

    @property
    def search_drone_id(self):
        self.curs.execute(
            f"SELECT serial_no, product_type, dt_first, dt_last,"
            f" id FROM vidma.vidma_drones WHERE serial_no='{self.drone_id[0]}'")
        res = self.curs.fetchall()
        return res


'''second sql req on'''


class SecondSQLReq:

    def __init__(self, *args):
        self.conn = psycopg2.connect(f"dbname= user= password=AxqwKNn4")
        self.curs = self.conn.cursor()
        self.drone_id = args

    @property
    def make_sql(self):
        self.curs.execute(
            "SELECT serial_no, product_type, longitude, latitude, height, altitude,"
            "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt,"
            " frame_id FROM vidma.vidma_frames"
            " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ")
        res = self.curs.fetchall()
        return res

    @property
    def newest_req(self):
        self.curs.execute(
            "SELECT serial_no, product_type, longitude, latitude, height, altitude,"
            "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt FROM vidma.vidma_frames"
            " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ORDER BY dt DESC")
        res = self.curs.fetchall()
        return res

    @property
    def oldest_req(self):
        self.curs.execute(
            "SELECT serial_no, product_type, longitude, latitude, height, altitude,"
            "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt FROM vidma.vidma_frames"
            " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ORDER BY dt")
        res = self.curs.fetchall()
        return res

    @property
    def search_by_drone_id(self):
        self.curs.execute(
            f"SELECT serial_no, product_type, longitude, latitude, height,"
            f" altitude, phone_app_latitude, phone_app_longitude, home_latitude,"
            f" home_longitude, dt FROM vidma.vidma_frames WHERE serial_no='{self.drone_id} AND home_latitude != 0.0 '")
        res = self.curs.fetchall()
        return res

    @property
    def update_data(self):
        self.curs.execute(
            f"SELECT serial_no, product_type, longitude, latitude, height,"
            f" altitude, phone_app_latitude, phone_app_longitude, home_latitude,"
            f" home_longitude, dt FROM vidma.vidma_frames WHERE frame_id > {self.drone_id[0]} "
            f"AND serial_no != 'fakefake' AND home_longitude != 0.0  "
        )
        res = self.curs.fetchall()
        return res


'''sql second_online_req'''


class SecondOnlineSQLReq:

    def __init__(self, *args):
        self.drone_id = args

    @property
    def make_sql(self):
        return SecondOrdersModel.objects.all()

    @property
    def newest_req(self):
        return SecondOrdersModel.objects.all().order_by('-dt')

    @property
    def oldest_req(self):
        return SecondOrdersModel.objects.all().order_by('dt')

    @property
    def search_by_drone_id(self):
        return SecondOrdersModel.objects.filter(serial_no=self.drone_id[0])


'''sql req on production'''


class OnlineSQLReq:
    def __init__(self, *args):
        self.drone_id = args

    @property
    def standart_req(self):
        res = MainOrders.objects.all()
        return res

    @property
    def newest_req(self):
        res = MainOrders.objects.all().order_by('-dt_last')
        return res

    @property
    def oldest_req(self):
        res = MainOrders.objects.all().order_by('dt_first')
        return res

    @property
    def search_drone_id(self):
        res = MainOrders.objects.filter(serial_no=self.drone_id[0])
        return res


'''download orders in local'''


class DownloadOrders(SendSqlReq):
    @property
    def download_order(self):
        self.curs.execute("SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_newest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY id DESC")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_oldest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY dt_last DESC")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="oldest_date_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
        for el in res:
            writer.writerow(el)
        return response


'''download second order on local'''


class DownloadSecondOrders(SecondSQLReq):
    @property
    def download_order(self):
        self.curs.execute("SELECT serial_no, product_type, longitude, latitude, height, altitude,"
                          "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude,"
                          " dt FROM vidma.vidma_frames"
                          " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="download_second_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(["SELECT serial_no, product_type, longitude, latitude, height, altitude,"
                         "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt"
                         ])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_newest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, longitude, latitude, height, altitude,"
            "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude,"
            " dt FROM vidma.vidma_frames"
            " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ORDER BY dt DESC"
        )
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="second_newest_date_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['SELECT serial_no, product_type, longitude, latitude, height, altitude,'
                         'phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt'])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_oldest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, longitude, latitude, height, altitude,"
            "phone_app_latitude, phone_app_longitude, home_latitude, home_longitude,"
            " dt FROM vidma.vidma_frames"
            " WHERE serial_no != 'fakefake' AND home_longitude != 0.0 ORDER BY dt"
        )
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="second_oldest_date_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['SELECT serial_no, product_type, longitude, latitude, height, altitude,'
                         'phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt'])
        for el in res:
            writer.writerow(el)
        return response


'''download orders on production'''


class DownloadOnlineOrders:

    @property
    def download_order(self):

        model = MainOrders.objects.values()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['id', 'serial_no', 'product_type', 'dt_first', 'dt_last'])
        for el in model:
            writer.writerow(el.values())

        return response

    @property
    def download_newest_order(self):
        model = MainOrders.objects.values().order_by('-dt_last')
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['id', 'serial_no', 'product_type', 'dt_first', 'dt_last'])
        for el in model:
            writer.writerow(el.values())

        return response

    @property
    def download_oldest_order(self):
        model = MainOrders.objects.values().order_by('id')
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['id', 'serial_no', 'product_type', 'dt_first', 'dt_last'])
        for el in model:
            writer.writerow(el.values())

        return response


'''download second orders on production '''


class DownloadSecondOnlineOrders:

    @property
    def download_order(self):

        model = SecondOrdersModel.objects.values()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['SELECT serial_no, product_type, longitude, latitude, height, altitude,'
                         'phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt'])
        for el in model:
            writer.writerow(el.values())

        return response

    @property
    def download_newest_order(self):
        model = SecondOrdersModel.objects.values().order_by('-dt')
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['SELECT serial_no, product_type, longitude, latitude, height, altitude,'
                         'phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt'])
        for el in model:
            writer.writerow(el.values())

        return response

    @property
    def download_oldest_order(self):
        model = SecondOrdersModel.objects.values().order_by('dt')
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['SELECT serial_no, product_type, longitude, latitude, height, altitude,'
                         'phone_app_latitude, phone_app_longitude, home_latitude, home_longitude, dt'])
        for el in model:
            writer.writerow(el.values())

        return response


'''logic for CombatOrder'''


class CombatLogic:

    def __init__(self, *args):
        if len([*args]) == 0:
            self.date_search = []
        else:
            self.date_search = [*args][0]

    @property
    def today_req(self):
        model_set = SecondOrdersModel.objects.filter(
            dt__icontains=datetime.today().strftime('%y-%m-%d')).values().order_by(
            'serial_no')

        model = []

        if len(model_set) == 1:
            quantity = SecondOrdersModel.objects.filter(dt__icontains=datetime.today().strftime('%y-%m-%d'),
                                                        serial_no=model_set[0][
                                                            'serial_no']).values().count()

            model_data = {'serial_no': model_set[0]['serial_no'],
                          'dt': model_set[0]['dt'],
                          'product_type': model_set[0]['product_type'],
                          'quantity': quantity,
                          'action': 0,
                          }

            model.append(model_data)

        else:
            for el in range(len(model_set)):
                if el == 0:
                    quantity = SecondOrdersModel.objects.filter(dt__icontains=datetime.today().strftime('%y-%m-%d'),
                                                                serial_no=model_set[el][
                                                                    'serial_no']).values().count()

                    model_data = {'serial_no': model_set[el]['serial_no'],
                                  'dt': model_set[el]['dt'],
                                  'product_type': model_set[el]['product_type'],
                                  'quantity': quantity,
                                  'action': 0,
                                  }

                    model.append(model_data)
                else:
                    if model_set[el]['serial_no'] != model_set[el - 1]['serial_no']:
                        quantity = SecondOrdersModel.objects.filter(dt__icontains=datetime.today().strftime('%y-%m-%d'),
                                                                    serial_no=model_set[el][
                                                                        'serial_no']).values().count()

                        model_data = {'serial_no': model_set[el]['serial_no'],
                                      'dt': model_set[el]['dt'],
                                      'quantity': quantity,
                                      'action': 0,
                                      }

                        model.append(model_data)
        return model

    @property
    def search_by_date(self):
        model_set = SecondOrdersModel.objects.filter(dt__icontains=self.date_search).values().order_by('serial_no')

        model = []
        if len(model_set) == 1:
            model.append(model_set)

        else:
            for el in range(len(model_set)):
                if el == 0:
                    quantity = SecondOrdersModel.objects.filter(dt__icontains=self.date_search,
                                                                serial_no=model_set[el][
                                                                    'serial_no']).values().count()

                    model_data = {'serial_no': model_set[el]['serial_no'],
                                  'dt': model_set[el]['dt'],
                                  'product_type': model_set[el]['product_type'],
                                  'quantity': quantity,
                                  'action': 0,
                                  }

                    model.append(model_data)
                else:
                    if model_set[el]['serial_no'] != model_set[el - 1]['serial_no']:
                        quantity = SecondOrdersModel.objects.filter(dt__icontains=self.date_search,
                                                                    serial_no=model_set[el][
                                                                        'serial_no']).values().count()

                        model_data = {'serial_no': model_set[el]['serial_no'],
                                      'dt': model_set[el]['dt'],
                                      'product_type': model_set[el]['product_type'],
                                      'quantity': quantity,
                                      'action': 0,
                                      }

                        model.append(model_data)
        return model


'''Combat orders download docx logic'''


class BuildCombatOrders:

    def __init__(self, *args):
        self.start_cut = args[0]
        self.end_cut = args[1]

    @property
    def build_orders(self):

        drone_id = []

        logic = CombatLogic(self.start_cut)

        if len(logic.search_by_date) == 0:
            text = Document()
            text.add_heading(f"""Доповідь командира СПР Око 1го СтрБ 67ї ОМБр ДУК станом на 03:00, {self.start_cut}.
                            """, level=1)

            text.add_paragraph(f"""Обстановка в смузі відповідальності бригади стабільна, контрольована.

Змін в стані та положенні підрозділів бригади  немає.

Аероскоп: За період 16:00 {self.start_cut} - 03:00 {self.end_cut} в повітрі над зоною н.п. Липці - Лук'янці - Борисівна - Зелене - Середа- Нескучне  не зафіксовано жодних БпЛА системи DJI та схожої з нею системи.

Розвідка технічними засобами підрозділу від 16:00 {self.start_cut} до 03:00 {self.end_cut}:
            1.Технічними засобами спостереження, відеофіксації та розвідки СПР Око 1го СтрБ 67ї ОМБр ДУК  за звітний період не зафіксовано ніяких значущих подій.         
            
            2.Засобами аеророзвідки за звітний період  не зафіксовано ніяких значущих подій з причини підготовки обладнання та технічних засобів до виконання бойових завдань.
Спостереження, розвідка з використанням технічних засобів підрозділу триває.

Втрати:
    о/с- 0
    в/т- 0
    а/т- 0

Виконання вогневих завдань- не виконувались. 
Обладнання територій в інженерному та фортифікаційному відношенні - без змін.
Розвідка - 1 сб проводив огляд місцевості (позицій, розвідку) за допомогою технічних засобів відеоспостереження, розрахунків БпЛА та іншого обладнання, пристроїв СПР Око 1го СтрБ 67ї ОМБр ДУК.

Заходи бойової підготовки:
    Проведена роботи по злагодженю та взаємодії між особовим складом підрозділу із бойової підготовки. Також особовий склад провів закріплення правил поведінки в умовах бойових дій в складі підрозділу.
    Проблемні питання - відсутні.

Оперативний черговий                                                                              Володимир Расько.                
солдат                                                          
                            """)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                headers={'Content-Disposition': 'attachment; filename="combat_orders.docx"'},
            )
            text.save(response)
            return response

        else:
            for el in logic.search_by_date:
                if el['product_type'] == 58:
                    drone_id.append('mavic air')
                elif el['product_type'] == 60:
                    drone_id.append('M 300 RTK')
                elif el['product_type'] == 63:
                    drone_id.append('mini 2')
                elif el['product_type'] == 66:
                    drone_id.append('Air 2s')
                elif el['product_type'] == 67:
                    drone_id.append('M 30')
                elif el['product_type'] == 68:
                    drone_id.append('mavic 3')
                elif el['product_type'] == 69:
                    drone_id.append('mavic 2 Enterprise')
                elif el['product_type'] == 70:
                    drone_id.append('mini se')
                elif el['product_type'] == 77:
                    drone_id.append('mavic 3')
                else:
                    drone_id.append('mavic 3')

            text = Document()
            text.add_heading(f"Доповідь командира СПР Око 1го СтрБ 67ї ОМБр ДУК станом на 03:00 {self.start_cut}.",
                             level=1)
            text.add_paragraph(f"""
Обстановка в смузі відповідальності бригади стабільна, контрольована
Змін в стані та положенні підрозділів бригади  немає

Аероскоп: За період 16:00 {self.start_cut} - 03:00 {self.end_cut} в повітрі над зоною н.п. Липці - Лук'янці - Борисівна - Зелене - Середа- Нескучне  зафіксовано  такі дрони {*drone_id,}

Розвідка технічними засобами підрозділу від 16:00 {self.start_cut} до 03:00 {self.end_cut}:
        1. Технічними засобами спостереження, відеофіксації та розвідки СПР Око 1го СтрБ 67ї ОМБр ДУК  за звітний період не зафіксовано ніяких значущих подій.
        
        2. Засобами аеророзвідки за звітний період  не зафіксовано ніяких значущих подій з причини підготовки обладнання та технічних засобів до виконання бойових завдань.

Спостереження, розвідка з використанням технічних засобів підрозділу триває.

Втрати:
    о/с- 0
    в/т- 0
    а/т- 0

Виконання вогневих завдань- не виконувались. 

Обладнання територій в інженерному та фортифікаційному відношенні - без змін.

Розвідка - 1 сб проводив огляд місцевості (позицій, розвідку) за допомогою технічних засобів відеоспостереження, розрахунків БпЛА та іншого обладнання, пристроїв СПР Око 1го СтрБ 67ї ОМБр ДУК.
Заходи бойової підготовки:
    Проведена роботи по злагодженю та взаємодії між особовим складом підрозділу із бойової підготовки. Також особовий склад провів закріплення правил поведінки в умовах бойових дій в складі підрозділу.
    Проблемні питання - відсутні.
    
Оперативний черговий                                                   Володимир Расько.
солдат                  					                            
                """)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                headers={'Content-Disposition': 'attachment; filename="combat_orders.docx"'},
            )
            text.save(response)
            return response
