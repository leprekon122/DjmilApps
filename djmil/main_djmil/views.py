import os
from datetime import datetime
import requests
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import permissions
from .models import MainOrders, SecondOrdersModel
from .view_logic import CombatLogic, SecondOnlineSQLReq, OnlineSQLReq, \
    DownloadOnlineOrders, DownloadSecondOnlineOrders, BuildCombatOrders, \
    BuildStatistics, LogicAnalyze, OpenDataCombatLogicClass, \
    ChoseStatusCombat, AddFlightRecorderData, \
    FilterFlightRecordData, SkySafeLogic, OpenDataSkySafeClass
from .tasks import start_task


load_dotenv()


def login_page(request):
    """function for login on login page"""
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('online_second_orders')

    return render(request, 'main_djmil/login_page.html')


class MainPage(APIView):
    """MainPage logic class"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for het request in main page"""
        start = request.GET.get('start')
        if start:
            start_task.apply_async()
        logic = BuildStatistics(datetime.today().strftime('%y-%m-d')[:7])
        data = {'model': logic.top_rank,
                'action': 0,
                'username': request.user,
                }
        return render(request, "main_djmil/main_page.html", data)


class OnlineOrders(APIView):
    """logic in OnlineOrders page"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for get request in OnlineOrdersPage page"""
        model = MainOrders.objects.all()

        new = request.GET.get('new')
        today = request.GET.get('today')
        old = request.GET.get('old')
        search_by_drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')
        date_search = request.GET.get('date_search')
        req = OnlineSQLReq()

        if download:
            options = request.GET.get('options')
            req_download = DownloadOnlineOrders()
            if options == 'without':
                return req_download.download_order
            if options == 'newest':
                return req_download.download_newest_order
            if options == 'oldest':
                return req_download.download_oldest_order

        if new:
            model = req.newest_req
        elif old:
            model = req.oldest_req
        elif search_by_drone_id:
            req = OnlineSQLReq(search_by_drone_id)
            model = req.search_drone_id

        if date_search:
            model = MainOrders.objects.filter(dt_first__icontains=date_search)

        if today:
            model = MainOrders.objects.filter(dt_first__icontains=datetime.today()
                                              .strftime('%Y-%m-%d'))

        data = {'model': model}

        return render(request, 'main_djmil/online_orders.html', data)


class OnlineSecondOrders(APIView,
                         ):
    """logic in OnlineSecondOrders page"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for het request in OnlineSecondOrders page"""

        model = SecondOrdersModel.objects.all().order_by('-id')
        paginator = Paginator(model, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        today = request.GET.get('today')
        search_by_drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')
        # update_data = request.GET.get('update_data')
        date_search = request.GET.get('date_search')

        # req_update = SecondSQLReq()

        # update order block
        # if update_data:
        # if len(model) == 0:
        #    for el in req_update.make_sql:
        #        SecondOrdersModel(serial_no=el[0], product_type=el[1], longitude=el[2],
        #                          latitude=el[3], height=el[4], altitude=el[5],
        #                          phone_app_latitude=el[6], phone_app_longitude=el[7],
        #                          home_latitude=el[8], home_longitude=el[9], dt=el[10],
        #                          frame_id=el[11]).save()
        # else:
        #    frame_id = SecondOrdersModel.objects.values('frame_id').last()['frame_id']
        # req_update = SecondSQLReq(frame_id)
        #    for el in req_update.update_data:
        #        SecondOrdersModel(serial_no=el[0], product_type=el[1], longitude=el[2],
        #                          latitude=el[3], height=el[4], altitude=el[5],
        #                          phone_app_latitude=el[6], phone_app_longitude=el[7],
        #                          home_latitude=el[8], home_longitude=el[9], dt=el[10],
        #                          frame_id=el[11]).save()

        # download orders block
        if download:
            options = request.GET.get('options')
            req_download = DownloadSecondOnlineOrders()
            if options == 'without':
                return req_download.download_order
            if options == 'newest':
                return req_download.download_newest_order
            if options == 'oldest':
                return req_download.download_oldest_order

        # search by old,new, drone_id

        if search_by_drone_id:
            req = SecondOnlineSQLReq(search_by_drone_id)
            model = req.search_by_drone_id

            data = {'model': model,
                    }
            return render(request, 'main_djmil/online_second_orders.html', data)

        # sort_by_date
        if date_search:
            model = SecondOrdersModel.objects.filter(dt__icontains=date_search).order_by("dt")
            data = {'model': model,
                    }
            return render(request, 'main_djmil/online_second_orders.html', data)

        if today:
            model = SecondOrdersModel.objects.filter(
                dt__icontains=datetime.today().strftime('%Y-%m-%d')).values().order_by('-id')
            data = {'model': model,
                    }
            return render(request, 'main_djmil/online_second_orders.html', data)

        data = {'model': paginator.get_page(page_number).object_list,
                'page_obj': page_obj,
                'current_path': request.get_full_path(),
                }

        return render(request, 'main_djmil/online_second_orders.html', data)


class CombatOrder(APIView):
    """combat_order page view"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for get request in CombatOrder page"""

        date_search = request.GET.get('date_search')

        open_data = request.GET.get('open_data')

        today = request.GET.get('today')

        build_order = request.GET.get('build_order')

        fake_drone = request.GET.get('fakefake')

        get_time = request.GET.get('time')

        # build docx file and download
        if build_order:
            logic = BuildCombatOrders()
            return logic.build_orders

        # filter by date
        if date_search:
            logic = CombatLogic(date_search, fake_drone, get_time)
            data = {
                'model': logic.search_by_date,
                'action': 0
            }
            return render(request, 'main_djmil/combat_orders.html', data)

        # filter by today checkbox
        if today:
            logic = CombatLogic(date_search, fake_drone, get_time)

            data = {
                'model': logic.today_req[0],
                'action': 0,
            }

            return render(request, 'main_djmil/combat_orders.html', data)

        # personal  detail page
        if open_data:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                      f"lat=48.973403&lon=38.142698&" \
                      f"units=metric&appid={os.getenv('WEATHER_API_KEY')}"

            req = requests.get(api_url, timeout=20)

            logic = OpenDataCombatLogicClass(open_data)

            data = {'model': logic.enter_to_detail_data,
                    'weather': req.json(),
                    }
            return render(request, 'main_djmil/combat_orders.html', data)

        return render(request, 'main_djmil/combat_orders.html')

    @staticmethod
    def post(request):
        """function for POST request in CombatOrder page"""
        status = request.POST.get('status').split(' ')
        logic = ChoseStatusCombat(status)
        logic.change_status()

        model = CombatLogic(f"{status[4].split(',')[0]}-{status[2].split(',')[0]}-"
                            f"{status[3].split(',')[0]}",
                            fake_drone=None)

        data = {
            'model': model.today_req[0],
            'action': 0
        }

        return render(request, 'main_djmil/combat_orders.html', data)


class StatisticsPage(APIView):
    """StaticPage logic"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """function for get request in StatisticsPage """
        month = request.GET.get('month')
        today = request.GET.get('today')
        weak = request.GET.get('weak')
        date_1 = request.GET.get('date_1')
        date_2 = request.GET.get('date_2')

        # compare two month data

        if all([date_1, date_2]):
            logic = LogicAnalyze(date_1, date_2)
            data = logic.make_anylyze
            return render(request, 'main_djmil/main_statistics.html', data)

        # chose total result for month
        if month:
            logic = BuildStatistics(month[:7]).total_results_for_chosen_month

            return render(request, 'main_djmil/main_statistics.html', logic)

        # statistics for today
        if today:
            logic = BuildStatistics(datetime.today().strftime("%y-%m-%d")).today_statistics_order
            print(logic)
            return render(request, 'main_djmil/main_statistics.html', {'logic': logic,
                                                                       'count': 'today'
                                                                       })

        # logic for result per weak
        if weak:
            logic = BuildStatistics(datetime.today().strftime("%y-%m-%d")).weak_statistics_order

            data = {'model': logic[0],
                    'date_set': logic[1],
                    'quan_by_date': logic[2],
                    'count': 'week'
                    }
            return render(request, 'main_djmil/main_statistics.html', data)

        return render(request, 'main_djmil/main_statistics.html')


class FlightRecorder(APIView):
    """logic for fly_recorder page"""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """ function for get request in FlightRecorder page """
        date_search = request.GET.get('date_search')
        find_time = request.GET.get('time')
        today = request.GET.get('today')

        if today:
            today_data = datetime.today().strftime('%y-%m-%d')
            logic = FilterFlightRecordData(today_data, find_time, date_search)
            model = logic.find_by_today_filter()
            data = {'logic': model,
                    'count': 1,
                    }
            return render(request, 'main_djmil/flight_recorder.html', data)

        data = {'count': 0}

        return render(request, 'main_djmil/flight_recorder.html', data)

    @staticmethod
    def post(request):
        """ function for POST request in FlightRecorder page """
        add_record = request.POST.get('add_record')
        drona_type = request.POST.get('drona_type')
        drone_id = request.POST.get('drone_id')
        coord_x = request.POST.get('coord_x')
        coord_y = request.POST.get('coord_x')

        if add_record:
            logic = AddFlightRecorderData(drona_type, drone_id, coord_x, coord_y)
            logic.add_data()
        return render(request, 'main_djmil/flight_recorder.html')


class SkySafeOrder(APIView):
    """logic for sky_safe order page"""

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):

        """sky_safe page GET request func """

        date_search = request.GET.get('date_search')

        open_data = request.GET.get('open_data')

        today = request.GET.get('today')

        build_order = request.GET.get('build_order')

        fake_drone = request.GET.get('fakefake')

        get_time = request.GET.get('time')

        # build docx file and download
        if build_order:
            start_cut = request.GET.get('start_cut')
            end_cut = request.GET.get('end_cup')
            logic = BuildCombatOrders(start_cut, end_cut)
            return logic.build_orders

        # filter by date
        if date_search:
            logic = SkySafeLogic(date_search, fake_drone, get_time)
            data = {
                'model': logic.search_by_date,
                'action': 0
            }
            return render(request, 'main_djmil/sky_safe.html', data)

        # filter by today checkbox
        if today:
            logic = SkySafeLogic(date_search, fake_drone, get_time)

            data = {
                'model': logic.today_req[0],
                'action': 0,
            }

            return render(request, 'main_djmil/sky_safe.html', data)

        # personal  detail page
        if open_data:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?" \
                      f"lat=48.973403&lon=38.142698&" \
                      f"units=metric&appid={os.getenv('WEATHER_API_KEY')}"

            req = requests.get(api_url, timeout=20)

            logic = OpenDataSkySafeClass(open_data)

            data = {'model': logic.enter_to_detail_data,

                    'weather': req.json(),
                    }
            return render(request, 'main_djmil/sky_safe.html', data)

        return render(request, 'main_djmil/sky_safe.html')
