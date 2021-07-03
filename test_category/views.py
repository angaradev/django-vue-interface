from django.shortcuts import render
from django.http import HttpResponse
from test_category.elastic_insert import do_all

# Create your views here.
def elastic_file_create(request):
    try:
        prods = do_all()
        return HttpResponse(f"<h1>Created {prods} Products so far</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Somethin went wrong {e}</h1>")
