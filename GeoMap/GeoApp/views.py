from django.shortcuts import render, redirect
from . import map_editor, Server_connector
from .forms import GetPoezd, GetUno
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.


def main(request):
    return render(request, 'GeoApp/main.html', {})


def home(request):
    form = GetPoezd()
    return render(request, 'GeoApp/index.html', {'form': form})


def map(request):
    month_form = ''
    poezd_form = ''
    form = ''
    if request.method == 'POST':
        form = GetPoezd(request.POST)
        if form.is_valid():
            month_form = form.cleaned_data['month'].replace("-", "")
            poezd_form = form.cleaned_data['poezd']

    map, error, no_coord, numbering, start_end_meta = map_editor.getMap(month_form, poezd_form)

    context = {'my_map': map,
               'no_coord': no_coord}
    if error:
        messages.error(request, 'Нет данных')
        return render(request, 'GeoApp/index.html', {'form': form})
        # return render(request, 'GeoApp/no_data.html', context)
    else:
        return render(request, 'GeoApp/home.html', context)


def map_two(request):
    form = GetPoezd()
    return render(request, 'GeoApp/map_two.html', {'form': form})


def map_uno(request):
    form = GetUno()
    return render(request, 'GeoApp/map_uno.html', {'form': form})


def map_uno_ajax(request):
    month = ''
    uno = ''
    iddos = ''
    form = GetUno(request.POST)
    if form.is_valid():
        month = form.cleaned_data['month'].replace("-", "")
        uno = form.cleaned_data['uno']
        uno = str(uno).zfill(12)
        iddos = form.cleaned_data['iddos']
        iddos = str(iddos).zfill(10)

    ajax_map, error, no_coord, start_end_meta, numbering, uno_list = map_editor.getMapUno(month, uno, iddos)

    response = {'ajax_map': ajax_map,
                'no_coord': no_coord,
                'start_end_meta': start_end_meta,
                'numbering': numbering,
                'uno_list': uno_list}
    return JsonResponse(response)


def map_ajax(request):
    poezd = ''
    month = ''
    form = GetPoezd(request.POST)
    st_text = False
    if form.is_valid():
        month = form.cleaned_data['month'].replace("-", "")
        poezd = form.cleaned_data['poezd']
        poezd = str(poezd).zfill(16)
        st_text = form.cleaned_data['st_text']

    ajax_map, error, no_coord, numbering, start_end_meta = map_editor.getMap(month, poezd, icon_text=st_text)
    response = {'ajax_map': ajax_map,
                'no_coord': no_coord,
                'numbering': numbering,
                'start_end_meta': start_end_meta}

    return JsonResponse(response)


def poezd_suggest(request):
    pattern = request.GET.get('search_keyword')
    pattern = '%' + pattern + '%'
    filter = '?poezd=' + pattern
    poezd_json = Server_connector.get_set('PoezdSuggest', filter)
    response = {'trains_code': poezd_json}
    return JsonResponse(response)
