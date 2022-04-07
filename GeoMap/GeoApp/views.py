from django.shortcuts import render, redirect
from . import map_editor, Server_connector
from .forms import getPoezd
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.


def home(request):
    form = getPoezd()
    return render(request, 'GeoApp/index.html', {'form': form})


def map(request):
    month_form = ''
    poezd_form = ''
    form = ''
    if request.method == 'POST':
        form = getPoezd(request.POST)
        if form.is_valid():
            month_form = form.cleaned_data['month'].replace("-", "")
            poezd_form = form.cleaned_data['poezd']

    map, error, no_coord, numbering = map_editor.getMap(month_form, poezd_form)

    context = {'my_map': map,
               'no_coord': no_coord}
    if error:
        messages.error(request, 'Нет данных')
        return render(request, 'GeoApp/index.html', {'form': form})
        # return render(request, 'GeoApp/no_data.html', context)
    else:
        return render(request, 'GeoApp/home.html', context)


def map_two(request):
    form = getPoezd()
    return render(request, 'GeoApp/map_two.html', {'form': form})


def map_ajax(request):
    poezd = ''
    month = ''
    form = getPoezd(request.POST)
    if form.is_valid():
        month = form.cleaned_data['month'].replace("-", "")
        poezd = form.cleaned_data['poezd']
        poezd = str(poezd).zfill(16)

    ajax_map, error, no_coord, numbering = map_editor.getMap(month, poezd)
    response = {'ajax_map': ajax_map,
                'no_coord': no_coord,
                'numbering': numbering}
    return JsonResponse(response)


def poezd_suggest(request):
    pattern = request.GET.get('search_keyword')
    pattern = '%' + pattern + '%'
    filter = '?poezd=' + pattern
    poezd_json = Server_connector.get_set('PoezdSuggest', filter)
    response = {'trains_code': poezd_json}
    return JsonResponse(response)
