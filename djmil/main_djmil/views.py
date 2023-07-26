from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from .models import MainOrders, SecondOrdersModel
from .view_logic import CombatLogic, SecondSQLReq, SendSqlReq, SecondOnlineSQLReq, OnlineSQLReq, DownloadOrders, \
    DownloadSecondOrders, DownloadOnlineOrders, DownloadSecondOnlineOrders, BuildCombatOrders, MainPageLogic, \
    BuildStatistics, LogicAnalyze, OpenDataCombatLogicClass, ChoseStatusCombat
from rest_framework.views import APIView
from rest_framework import permissions
from datetime import datetime
from django.db.models import F

'''class for offline sql requests '''


def login_page(request):
    username = request.GET.get('login')
    password = request.GET.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('online_second_orders')

    # else:
    #    mes = messages.error(request, "oops wrong login or password!")
    #    data = {'mes': mes}
    #    return render(request, 'main_djmil/login_page.html', data)

    return render(request, 'main_djmil/login_page.html')


class MainPage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        logic = BuildStatistics(datetime.today().strftime('%y-%m-d')[:7])
        data = {'model': logic.top_rank,
                'action': 0}
        return render(request, "main_djmil/main_page.html", data)


class Orders(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        req = SendSqlReq()

        data = {'res': req.standart_req
                }
        new = request.GET.get('new')
        old = request.GET.get('old')
        search_by_drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')
        if new:
            data = {'res': req.newest_req}
        elif old:
            data = {'res': req.oldest_req}
        elif search_by_drone_id:
            req = SendSqlReq(search_by_drone_id)
            data = {'res': req.search_drone_id}
        elif download:
            options = request.GET.get('options')
            if options == 'without':
                download = DownloadOrders()
                return download.download_order
            elif options == 'newest':
                download = DownloadOrders()
                return download.download_newest_order
            elif options == 'oldest':
                download = DownloadOrders()
                return download.download_oldest_order

        return render(request, "main_djmil/orders.html", data)


class SecondOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        req = SecondSQLReq()
        data = {'res': req.make_sql}

        new = request.GET.get('new')
        old = request.GET.get('old')
        drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')

        if new:
            data = {'res': req.newest_req}
        elif old:
            data = {'res': req.oldest_req}
        elif drone_id:
            req = SecondSQLReq(drone_id)
            data = {'res': req.search_by_drone_id}
        elif download:
            options = request.GET.get('options')

            if options == 'without':
                download = DownloadSecondOrders
                return download.download_order
            elif options == 'newest':
                return download.download_newest_order
            elif options == 'oldest':
                download = DownloadOrders()
                return download.download_oldest_order

        return render(request, 'main_djmil/second_order.html', data)


class OnlineOrders(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
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
            elif options == 'newest':
                return req_download.download_newest_order
            elif options == 'oldest':
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
            model = MainOrders.objects.filter(dt_first__icontains=datetime.today().strftime('%Y-%m-%d'))

        data = {'model': model}

        return render(request, 'main_djmil/online_orders.html', data)


class OnlineSecondOrders(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):

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
            elif options == 'newest':
                return req_download.download_newest_order
            elif options == 'oldest':
                return req_download.download_oldest_order

        # search by old,new, drone_id

        if search_by_drone_id:
            req = SecondOnlineSQLReq(search_by_drone_id)
            model = req.search_by_drone_id

            data = {'model': model
                    }
            return render(request, 'main_djmil/online_second_orders.html', data)

        # sort_by_date
        if date_search:
            model = SecondOrdersModel.objects.filter(dt__icontains=date_search).order_by("dt")
            data = {'model': model}
            return render(request, 'main_djmil/online_second_orders.html', data)

        if today:
            model = SecondOrdersModel.objects.filter(
                dt__icontains=datetime.today().strftime('%Y-%m-%d')).values().order_by('-id')
            data = {'model': model}
            return render(request, 'main_djmil/online_second_orders.html', data)

        data = {'model': paginator.get_page(page_number).object_list,
                'page_obj': page_obj,
                'current_path': request.get_full_path()
                }

        return render(request, 'main_djmil/online_second_orders.html', data)


"""combat_order page view"""


class CombatOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):

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
            logic = OpenDataCombatLogicClass(open_data)
            return render(request, 'main_djmil/combat_orders.html', logic.enter_to_detail_data)

        return render(request, 'main_djmil/combat_orders.html')

    @staticmethod
    def post(request):
        status = request.POST.get('status').split(' ')
        logic = ChoseStatusCombat(status)
        logic.change_status()

        model = CombatLogic(f"{status[4].split(',')[0]}-{status[2].split(',')[0]}-{status[3].split(',')[0]}",
                            fake_drone=None)

        data = {
            'model': model.today_req[0],
            'action': 0
        }

        return render(request, 'main_djmil/combat_orders.html', data)


class StatisticsPage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        month = request.GET.get('month')
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

        # logic = BuildStatistics()
        # data = logic.total_results_for_month

        return render(request, 'main_djmil/main_statistics.html')
