import csv
from datetime import datetime
import psycopg2

from django.http import HttpResponse
from docx import Document

from django.db.models import Count

from .models import SecondOrdersModel, MainOrders, StatisticDataSet


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
    def search_by_drone_id(self):
        return SecondOrdersModel.objects.filter(serial_no=self.drone_id[0]).order_by('-dt')


'''sql req on production'''


class OnlineSQLReq:
    def __init__(self, *args):
        self.drone_id = args

    @property
    def standart_req(self):
        return MainOrders.objects.all()

    @property
    def newest_req(self):
        return MainOrders.objects.all().order_by('-dt_last')

    @property
    def oldest_req(self):
        return MainOrders.objects.all().order_by('dt_first')

    @property
    def search_drone_id(self):
        return MainOrders.objects.filter(serial_no=self.drone_id[0])


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
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY dt_last ASC")
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
        if len([*args]) is not None == 0:
            self.date_search = []
        else:
            if len([*args]) > 1:
                self.date_search = args[0]
                self.fake_drone = args[1]
            else:
                self.date_search = args
                self.fake_drone = None

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
        if self.fake_drone is not None:
            model_set = SecondOrdersModel.objects.filter(dt__icontains=self.date_search).values().exclude(
                serial_no=self.fake_drone).order_by('serial_no')
        else:
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


'''OpenData get request in combat logic'''


class OpenDataCombatLogicClass:
    def __init__(self, *args):
        self.input_data = args[0]

        self.serial_no = self.input_data.split(' ')[0]
        self.current_year = self.input_data.split(',')[1].split(' ')[1]
        self.current_month = self.input_data.split(' ')[1]
        self.current_day = self.input_data.split(' ')[2].split(',')[0]

    @property
    def enter_to_detail_data(self):
        if int(self.current_day) < 10:
            self.current_day = f'0{self.current_day}'

        if self.current_month == 'March':
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-03-{self.current_day}", serial_no=self.serial_no).values().order_by(
                'serial_no')
            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-03-{self.current_day}", serial_no=self.serial_no).values().order_by(
                'serial_no')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,

            }

            return data

        elif self.current_month == "April":

            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-04-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-04-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,

            }
            return data

        elif self.current_month == "May":

            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-05-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-05-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,

            }
            return data

        elif self.current_month == "June":

            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-06-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-06-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_year == "July":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-07-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-07-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_month == "August":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-08-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-08-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_month == "September":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-09-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-09-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_month == "October":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-10-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-10-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_month == "November":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-11-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-11-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data

        elif self.current_month == "December":
            model_detail = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-12-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')

            model = SecondOrdersModel.objects.filter(
                dt__icontains=f"{self.current_year}-12-{self.current_day}", serial_no=self.serial_no).values().order_by(
                '-dt')[0]

            data = {
                'model': model,
                'model_detail': model_detail,
                'action': 1,
            }
            return data


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


class MainPageLogic:

    def __init__(self):
        pass

    @property
    def total_month_result(self):
        total_value = SecondOrdersModel.objects.filter(
            dt__icontains=datetime.today().strftime('%y-%m')).aggregate(
            Count('serial_no'))

        return total_value


class BuildStatistics:

    def __init__(self, *args):
        self.logic = CombatLogic(datetime.today().strftime('%y-%m'))
        self.data_set = {}
        self.model = []
        self.open_data = args

    @property
    def total_results_for_chosen_month(self):
        mavic3 = []
        m300rtk = []
        mini_2 = []
        air_2s = []
        m30 = []
        mavic2enterprise = []
        mini_se = []
        data_set = CombatLogic(self.open_data[0]).search_by_date
        for el in data_set:

            if el['product_type'] == 68:
                mavic3.append(el['product_type'])
            elif el['product_type'] == 60:
                m300rtk.append(el['product_type'])
            elif el['product_type'] == 63:
                mini_2.append(el['product_type'])
            elif el['product_type'] == 66:
                air_2s.append(el['product_type'])
            elif el['product_type'] == 67:
                m30.append(el['product_type'])
            elif el['product_type'] == 69:
                mavic2enterprise.append(el['product_type'])
            elif el['product_type'] == 70:
                mini_se.append(el['product_type'])
            else:
                mavic3.append(el['product_type'])

        data = {'total_value': len(CombatLogic(self.open_data[0]).search_by_date),
                'dirty_total_value': len(
                    SecondOrdersModel.objects.filter(dt__icontains=self.open_data[0])),
                'mavic3': len(mavic3),
                'M300RTK': len(m300rtk),
                'mini_2': len(mini_2),
                'air_2s': len(air_2s),
                'm30': len(m30),
                'mavic2Enterprise': len(mavic2enterprise),
                'mini_se': len(mini_se),
                }
        return data

    """Rate function"""

    @property
    def top_rank(self):
        logic = self.logic.search_by_date
        if len(logic) == 1:
            self.data_set = {'serial_no': logic[0]['serial_no'],
                             'quantity': logic[0]['quantity']
                             }
            self.model.append(self.data_set)

        elif len(logic) == 0:
            self.model.append('no data')
        else:
            for el in range(len(logic)):
                if el < len(logic) - 1:
                    if logic[el]['quantity'] > logic[el + 1]['quantity']:
                        self.data_set = {'serial_no': logic[el]['serial_no'],
                                         'quantity': logic[el]['quantity']
                                         }
                        self.model.append(self.data_set)
                else:
                    if logic[el]['quantity'] > logic[el - 1]['quantity']:
                        self.data_set = {'serial_no': logic[el]['serial_no'],
                                         'quantity': logic[el]['quantity']
                                         }
                    self.model.append(self.data_set)

        return self.model

    @property
    def open_data_main_page(self):
        model_detail = SecondOrdersModel.objects.filter(dt__icontains=datetime.today().strftime('%y-%m'),
                                                        serial_no=self.open_data[0]).values()

        data = {'model_detail': model_detail,
                'model': SecondOrdersModel.objects.filter(serial_no=self.open_data[0]).values()[0],
                'action': 1
                }

        return data


class LogicAnalyze:

    def __init__(self, data_1, data_2):
        self.date_1 = data_1
        self.date_2 = data_2
        self.data_set_1 = BuildStatistics(self.date_1[:7])
        self.data_set_2 = BuildStatistics(self.date_2[:7])
        self.data = {}

    @property
    def make_anylyze(self):

        try:
            total_value = (self.data_set_1.total_results_for_chosen_month['total_value'] /
                           self.data_set_2.total_results_for_chosen_month['total_value']) * 100
            self.data['total_value'] = f"{round(total_value, 2)} %"
        except Exception:
            self.data['total_value'] = 'none'

        try:
            dirty_total_value = (self.data_set_1.total_results_for_chosen_month['dirty_total_value'] /
                                 self.data_set_2.total_results_for_chosen_month['dirty_total_value']) * 100
            self.data['dirty_total_value'] = f"{round(dirty_total_value, 2)} %"

        except Exception:
            self.data['dirty_total_value'] = 'none'

        try:
            mavic3 = (self.data_set_1.total_results_for_chosen_month['mavic3'] /
                      self.data_set_2.total_results_for_chosen_month['mavic3']) * 100

            self.data['mavic3'] = f"{round(mavic3, 2)} %"
        except Exception:
            self.data['mavic3'] = 'none'

        try:
            M300RTK = (self.data_set_1.total_results_for_chosen_month['M300RTK'] /
                       self.data_set_2.total_results_for_chosen_month['M300RTK']) * 100

            self.data['M300RTK'] = f"{round(M300RTK, 2)} %"
        except Exception:
            self.data['M300RTK'] = 'none'

        try:
            mini_2 = (self.data_set_1.total_results_for_chosen_month['mini_2'] /
                      self.data_set_2.total_results_for_chosen_month['mini_2']) * 100

            self.data['mini_2'] = f"{round(mini_2, 2)} %"
        except Exception:
            self.data['mini_2'] = 'none'

        try:
            air_2s = (self.data_set_1.total_results_for_chosen_month['air_2s'] /
                      self.data_set_2.total_results_for_chosen_month['air_2s']) * 100

            self.data['air_2s'] = f"{round(air_2s, 2)} %"

        except Exception:
            self.data['air_2s'] = 'none'

        try:
            m30 = (self.data_set_1.total_results_for_chosen_month['m30'] /
                   self.data_set_2.total_results_for_chosen_month['m30']) * 100

            self.data['m30'] = f"{round(m30, 2)} %"
        except Exception:
            self.data['m30'] = 'none'

        try:
            mavic2Enterprise = (self.data_set_1.total_results_for_chosen_month['mavic2Enterprise'] /
                                self.data_set_2.total_results_for_chosen_month['mavic2Enterprise']) * 100

            self.data['mavic2Enterprise'] = f"{round(mavic2Enterprise, 2)} %"

        except Exception:
            self.data['mavic2Enterprise'] = 'none'

        try:
            mini_se = (self.data_set_1.total_results_for_chosen_month['mini_se'] /
                       self.data_set_2.total_results_for_chosen_month['mini_se']) * 100

            self.data['mini_se'] = f"{round(mini_se, 2)} %"
        except Exception:
            self.data['mini_se'] = 'none'

        return self.data
