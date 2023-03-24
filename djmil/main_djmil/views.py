from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import MainOrders
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
import psycopg2

import csv

'''class for offline sql requests '''


class SendSqlReq:

    def __init__(self, *args):
        self.conn = psycopg2.connect("dbname=vidma_db user=user017a password=AxqwKNn4")
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
            f"SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones WHERE serial_no='{self.drone_id[0]}'")
        res = self.curs.fetchall()
        return res


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


'''download orders on production'''


class DownloadOnlineOrders:

    def __init__(self, ):
        self.conn = psycopg2.connect("dbname=vidma_db user=user017a password=AxqwKNn4")
        self.curs = self.conn.cursor()

    @property
    def download_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones")
        res = self.curs.fetchall()

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="orders.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last'])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_newest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY dt_last DESC")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="newest_data_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
        for el in res:
            writer.writerow(el)
        return response

    @property
    def download_oldest_order(self):
        self.curs.execute(
            "SELECT serial_no, product_type, dt_first, dt_last, id FROM vidma.vidma_drones ORDER BY dt_first")
        res = self.curs.fetchall()
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="oldest_date_order.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last'])
        for el in res:
            writer.writerow(el)
        return response


def login_page(request):
    username = request.GET.get('login')
    password = request.GET.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
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
        log_out = request.GET.get('exit')

        if log_out:
            print('ok')
            logout(request)
            redirect('login')
        return render(request, "main_djmil/main_page.html")


class Orders(APIView):

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


class OnlineOrders(APIView):
    @staticmethod
    def get(request):
        model = MainOrders.objects.all()

        new = request.GET.get('new')
        old = request.GET.get('old')
        search_by_drone_id = request.GET.get('drone_id')
        download = request.GET.get('download')
        req = OnlineSQLReq()
        if new:
            model = req.newest_req
        elif old:
            model = req.oldest_req
        elif search_by_drone_id:
            req = OnlineSQLReq(search_by_drone_id)
            model = req.search_drone_id
        if download:
            options = request.GET.get('options')
            if options == 'without':
                req = DownloadOnlineOrders()
                return req.download_order
            elif options == 'newest':
                req = DownloadOnlineOrders()
                return req.download_newest_order
            elif options == 'oldest':
                req = DownloadOnlineOrders()
                return req.download_oldest_order

        data = {'model': model}

        return render(request, 'main_djmil/online_orders.html', data)
