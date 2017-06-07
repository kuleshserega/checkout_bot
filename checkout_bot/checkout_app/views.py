# -*- coding: UTF-8 -*-
from openpyxl import load_workbook
from io import BytesIO

from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings

from checkout_app.models import OrdersFileList, ProductOrder


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return super(LoginFormView, self).dispatch(
                request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login")


class FilesOfOrdersListView(LoginRequiredMixin, ListView):
    model = OrdersFileList
    template_name = 'file-list.html'
    context_object_name = 'results'
    paginate_by = settings.ROWS_ON_PAGE

    def get_queryset(self):
        qs = super(FilesOfOrdersListView, self).get_queryset().order_by('-id')
        return qs


class OrdersListView(LoginRequiredMixin, ListView):
    model = ProductOrder
    template_name = 'orders-list.html'
    context_object_name = 'orders'
    paginate_by = settings.ROWS_ON_PAGE

    def get_queryset(self):
        return ProductOrder.objects.filter(
            orders_file_id=self.kwargs['pk']).order_by('-date_created')


def upload_file_with_products(request):
    if request.method == "POST":
        if request.FILES['orders_list']:
            messages.success(request, 'Products from file was added')

            file_name = request.FILES['orders_list'].name
            orders_file_list = OrdersFileList(file_name=file_name)
            orders_file_list.save()

        file_in_memory = request.FILES['orders_list'].read()
        wb = load_workbook(filename=BytesIO(file_in_memory))
        ws = wb.active
        for row in ws.rows:
            order = ProductOrder(
                product_url=row[0].value,
                product_name=row[1].value,
                product_buyer=row[3].value,
                buyer_address=row[4].value,
                buyer_city=row[5].value,
                buyer_state_code=row[6].value,
                buyer_postal_code=row[7].value,
                orders_file=orders_file_list)
            order.save()

    return HttpResponseRedirect('/')


def get_handled_orders(request):
    pass
