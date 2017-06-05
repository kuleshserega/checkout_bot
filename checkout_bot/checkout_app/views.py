# -*- coding: UTF-8 -*-
import csv

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
        qs = super(FilesOfOrdersListView, self).get_queryset()
        return qs


class OrdersListView(LoginRequiredMixin, ListView):
    model = ProductOrder
    template_name = 'orders-list.html'
    context_object_name = 'orders'
    paginate_by = settings.ROWS_ON_PAGE

    def get_queryset(self):
        return ProductOrder.objects.filter(
            search_id=self.kwargs['pk']).order_by('-date_created')


def get_handled_orders(request):
    pass
