from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
import psycopg2
import csv

'''class for sql requests '''


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
                print('ok')
                res = req.standart_req
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
                )
                writer = csv.writer(response)
                writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
                for el in res:
                    writer.writerow(el)
                return response
            elif options == 'newest':
                res = req.newest_req
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
                )
                writer = csv.writer(response)
                writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
                for el in res:
                    writer.writerow(el)
                return response
            elif options == 'oldest':
                res = req.oldest_req
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
                )
                writer = csv.writer(response)
                writer.writerow(['serial_no', 'product_type', 'dt_first', 'dt_last', 'id'])
                for el in res:
                    writer.writerow(el)
                return response
        return render(request, "main_djmil/orders.html", data)
