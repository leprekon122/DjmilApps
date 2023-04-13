import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import MainOrders, SecondOrdersModel
from .view_logic import CombatLogic, SecondSQLReq, SendSqlReq, SecondOnlineSQLReq, OnlineSQLReq, DownloadOrders, \
    DownloadSecondOrders, DownloadOnlineOrders, DownloadSecondOnlineOrders, BuildCombatOrders
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import permissions
from datetime import datetime
from docx import Document
import docx2txt

'''class for offline sql requests '''


def login_page(request):
    username = request.GET.get('login')
    password = request.GET.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        print('ok')
        login(request, user)
        return redirect('main_page')

    # else:
    #    mes = messages.error(request, "oops wrong login or password!")
    #    data = {'mes': mes}
    #    return render(request, 'main_djmil/login_page.html', data)

    return render(request, 'main_djmil/login_page.html')


class MainPage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        return render(request, "main_djmil/main_page.html")


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
        model = SecondOrdersModel.objects.all().order_by('-dt')[1:20]

        print(os.getenv('db_pass.py'))

        new = request.GET.get('new')
        today = request.GET.get('today')
        old = request.GET.get('old')
        search_by_drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')
        # update_data = request.GET.get('update_data')
        req = SecondOnlineSQLReq()
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
        if new:
            model = req.newest_req
        elif old:
            model = req.oldest_req
        elif search_by_drone_id:
            req = SecondOnlineSQLReq(search_by_drone_id)
            model = req.search_by_drone_id

        # sort_by_date
        if date_search:
            model = SecondOrdersModel.objects.filter(dt__icontains=date_search)

        if today:
            model = SecondOrdersModel.objects.filter(dt__icontains=datetime.today().strftime('%Y-%m-%d'))

        data = {'model': model}

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

        # build docx file and download
        if build_order:
            start_cut = request.GET.get('start_cut')
            end_cut = request.GET.get('end_cup')
            logic = BuildCombatOrders(start_cut, end_cut)
            return logic.build_orders

        # filter by today checkbox
        if today:
            logic = CombatLogic()

            data = {
                'model': logic.today_req,
                'action': 0
            }

            return render(request, 'main_djmil/combat_orders.html', data)

        # filter by date
        if date_search:
            logic = CombatLogic(date_search)

            data = {
                'model': logic.search_by_date,
                'action': 0
            }
            return render(request, 'main_djmil/combat_orders.html', data)

        # personal  detail page
        if open_data:

            serial_no = open_data.split(' ')[0]
            current_year = open_data.split(',')[1].split(' ')[1]
            current_month = open_data.split(' ')[1]
            current_day = open_data.split(' ')[2].split(',')[0]

            if int(current_day) < 10:
                current_day = f'0{current_day}'

            if current_month == 'March':
                model_detail = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-03-{current_day}", serial_no=serial_no).values().order_by(
                    'serial_no')
                model = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-03-{current_day}", serial_no=serial_no).values().order_by(
                    'serial_no')[0]

                data = {
                    'model': model,
                    'model_detail': model_detail,
                    'action': 1
                }

                return render(request, 'main_djmil/combat_orders.html', data)

            elif current_month == "April":

                model_detail = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-04-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')

                model = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-04-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')[0]

                data = {
                    'model': model,
                    'model_detail': model_detail,
                    'action': 1
                }
                return render(request, 'main_djmil/combat_orders.html', data)

            elif current_month == "May":

                model_detail = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-05-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')

                model = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-03-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')[0]

                data = {
                    'model': model,
                    'model_detail': model_detail,
                    'action': 1
                }
                return render(request, 'main_djmil/combat_orders.html', data)

            elif current_year == "July":
                model_detail = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-06-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')

                model = SecondOrdersModel.objects.filter(
                    dt__icontains=f"{current_year}-03-{current_day}", serial_no=serial_no).values().order_by(
                    '-dt')[0]

                data = {
                    'model': model,
                    'model_detail': model_detail,
                    'action': 1
                }
                return render(request, 'main_djmil/combat_orders.html', data)

        return render(request, 'main_djmil/combat_orders.html')
