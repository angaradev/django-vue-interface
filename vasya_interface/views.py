from django.shortcuts import render
from django.views.generic import ListView
from .models import Rows


class RowsView(ListView):
    model = Rows
