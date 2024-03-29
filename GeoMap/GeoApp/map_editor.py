import folium
# import pandas as pd
from branca.element import Template, MacroElement
from . import Sap_connector, Server_connector, SOAPConnetor

from folium import plugins
from folium.features import DivIcon

ICONS_EXIST = 700


def getMap(month, poezd, icon_text=False):
    filter = '$filter=MONTH%20eq%20%27' + month + '%27%20and%20poezd%20eq%20%27' + poezd + '%27'
    stantions = Sap_connector.get_oData_set('InvestigationSet', filter)
    # filter = '?MONTH=' + month + '&poezd=' + poezd
    # stantions = Server_connector.get_set('InvestigationSet', filter)

    if not stantions:
        return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), 'no_data', [], [], []

    start_element = 0
    for row in stantions:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp = folium.Map(location=[stantions[start_element]['LAT'], stantions[start_element]['LON']], zoom_start=8,
                      control_scale=True)
    fs = plugins.Fullscreen()
    mapp.add_child(fs)

    # # путь
    # train_path = Sap_connector.get_oData_set('TrainPathSet', filter)
    # line = []
    # if train_path:
    #     for row in train_path:
    #         folium.Marker(location=[float(row['LAT']), float(row['LON'])], popup=row['NAME'],
    #                       icon=folium.Icon(color='orange')).add_to(mapp)
    #         line.append((float(row['LAT']), float(row['LON'])))
    #
    #     folium.PolyLine(line, color='red', weight=3, opacity=0.8).add_to(mapp)

    # наносим станции
    no_coord = []
    for row in stantions:
        # if row['LAT'] and row['LON']:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord.append(row)
        else:
            if icon_text:
                div_icon = DivIcon(
                    icon_size=(120, 100),
                    icon_anchor=(60, 100),
                    html=f'<div style="font-size: 15px; color: white; background: rgba(0, 0, 0, 0.4); '
                         f'border: 2px solid white; padding: 2px; border-radius: 10px;">'
                         f'{row["STANTION"]} <br> {row["NAME"]}</div>')
                folium.Marker(location=[float(row['LAT']), float(row['LON'])],
                              icon=div_icon).add_to(mapp)

            mapp = add_icon_number_from_map(row, mapp)

    # добавляем станции начала и конца
    start_end = Sap_connector.get_oData_set('InvestigationSFSet', filter)
    # start_end = Server_connector.get_set('InvestigationSFSet', filter)
    mapp, start_end_meta, no_coord = add_start_end_st(mapp, start_end, len(stantions), no_coord)

    # данные для таблицы проследования
    numbering = Sap_connector.get_oData_set('StNumberingSet', filter)
    # numbering = Server_connector.get_set('StNumberingSet', filter)

    # mapp = make_legend(mapp, title, uno)

    return mapp._repr_html_(), '', no_coord, numbering, start_end_meta


# getMap(month='202204', poezd='61922174005006')
def add_icon_number_from_map(row, mapp):
    if row['TYPEST'] == 'H':
        icon_color = 'white'
    elif row['TYPEST'] == 'T':
        icon_color = 'red'
    else:
        icon_color = 'orange'

    folium.Marker(location=[float(row['LAT']), float(row['LON'])],
                  popup=(str(row['STANTION']) + '\n' + row['NAME']),
                  icon=folium.Icon(color=icon_color, icon='')).add_to(mapp)  # icon='globe'

    patch = './static/icons/default.png'
    if int(row['NUMBER']) <= ICONS_EXIST:
        patch = './static/icons/' + str(int(row['NUMBER'])) + '.png'
    icon = folium.features.CustomIcon(patch, icon_size=(40, 40),
                                      icon_anchor=(20, 40), popup_anchor=(0, -40))
    folium.Marker(location=[float(row['LAT']), float(row['LON'])],
                  popup=(str(row['STANTION']) + '\n' + row['NAME']),
                  # icon=folium.Icon(color='blue', icon=globe)).add_to(mapp)
                  icon=icon).add_to(mapp)
    return mapp


def getMapUno(month, uno, iddos):
    filter = '$filter=MONTH%20eq%20%27' + month + '%27%20and%20UNO%20eq%20%27' + uno + '%27%20and%20IDDOS%20eq%20%27' + iddos + '%27'
    #print(filter)
    stantions = Sap_connector.get_oData_set('UnoStantionsSet', filter)
    #stantions = Sap_connector.get_oData_set('UnoStantionsCutSet', filter)

    if not stantions:
        return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), 'no_data', [], [], [], []

    start_element = 0
    for row in stantions:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp = folium.Map(location=[stantions[start_element]['LAT'], stantions[start_element]['LON']], zoom_start=8,
                      control_scale=True)
    fs = plugins.Fullscreen()
    mapp.add_child(fs)

    # наносим станции
    no_coord = []
    for row in stantions:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord.append(row)
        else:
            mapp = add_icon_number_from_map(row, mapp)
    # помечаем станции начала и конца
    start_end_st = Sap_connector.get_oData_set('UnoStantionsSFSet', filter)
    mapp, start_end_meta, no_coord = add_start_end_st(mapp, start_end_st, len(stantions), no_coord)

    numbering = Sap_connector.get_oData_set('UnoNumberingSet', filter)

    uno_list = Sap_connector.get_oData_set('UnoListSet', filter)

    # return mapp._repr_html_(), '', no_coord, numbering, start_end_meta
    return mapp._repr_html_(), '', no_coord, start_end_meta, numbering, uno_list
    # return 0


def getMapUnoCut(month, uno, iddos): # карта только со станциями начала и конца
    filter = '$filter=MONTH%20eq%20%27' + month + '%27%20and%20UNO%20eq%20%27' + uno + '%27%20and%20IDDOS%20eq%20%27' + iddos + '%27'
    #print(filter)
    stantions = Sap_connector.get_oData_set('UnoStantionsCutSet', filter)

    if not stantions:
        return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), []

    start_element = 0
    for row in stantions:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp = folium.Map(location=[stantions[start_element]['LAT'], stantions[start_element]['LON']], zoom_start=8,
                      control_scale=True)
    fs = plugins.Fullscreen()
    mapp.add_child(fs)

    # наносим станции
    no_coord = []
    for row in stantions:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord.append(row)
        else:
            mapp = add_icon_number_from_map(row, mapp)
    # помечаем станции начала и конца
    start_end_st = Sap_connector.get_oData_set('UnoStantionsSFSet', filter)
    mapp, start_end_meta, no_coord = add_start_end_st(mapp, start_end_st, len(stantions), no_coord)
    return mapp._repr_html_(), no_coord


def add_start_end_st(mapp, start_end_st, len_stantions, no_coord, month='', poezd=''):
    start_end_meta = []

    if start_end_st[0]['LAT_START'] or start_end_st[0]['LON_START']:
        icon = folium.features.CustomIcon('./static/icons/1.png', icon_size=(40, 40),
                                          icon_anchor=(20, 40), popup_anchor=(0, -40))
        # фон
        folium.Marker(location=[float(start_end_st[0]['LAT_START']), float(start_end_st[0]['LON_START'])],
                      popup=('Начало' + '\n' + str(start_end_st[0]['STANTION_START']) +
                             '\n' + str(start_end_st[0]['NAME_START'])),
                      icon=folium.Icon(color='green', icon='')).add_to(mapp)

        folium.Marker(location=[float(start_end_st[0]['LAT_START']), float(start_end_st[0]['LON_START'])],
                      popup=('Начало' + '\n' + str(start_end_st[0]['STANTION_START']) + '\n' +
                             str(start_end_st[0]['NAME_START'])),
                      icon=icon).add_to(mapp)
    else:
        cord_line = {'poezd': start_end_st[0]['poezd'],
                     'MONTH': start_end_st[0]['MONTH'],
                     'STANTION': start_end_st[0]['STANTION_START'],
                     'NAME': start_end_st[0]['NAME_START'],
                     'NUMBER': 0}
        no_coord.append(cord_line)

    if start_end_st[0]['LAT_FINISH'] or start_end_st[0]['LON_FINISH']:
        patch = './static/icons/default.png'
        if len_stantions < ICONS_EXIST:
            patch = './static/icons/' + str(len_stantions) + '.png'
        icon = folium.features.CustomIcon(patch, icon_size=(40, 40), icon_anchor=(20, 40), popup_anchor=(0, -40))

        folium.Marker(location=[float(start_end_st[0]['LAT_FINISH']), float(start_end_st[0]['LON_FINISH'])],
                      popup=('Конец' + '\n' + str(start_end_st[0]['STANTION_FINISH']) +
                             '\n' + str(start_end_st[0]['NAME_FINISH'])),
                      icon=folium.Icon(color='blue', icon='')).add_to(mapp)
        folium.Marker(location=[float(start_end_st[0]['LAT_FINISH']), float(start_end_st[0]['LON_FINISH'])],
                      popup=('Конец' + '\n' + str(start_end_st[0]['STANTION_FINISH']) +
                             '\n' + str(start_end_st[0]['NAME_FINISH'])),
                      # icon=folium.Icon(color='blue', icon=globe)).add_to(mapp)
                      icon=icon).add_to(mapp)
    else:
        cord_line = {'poezd': poezd,
                     'MONTH': month,
                     'STANTION': start_end_st[0]['STANTION_FINISH'],
                     'NAME': start_end_st[0]['NAME_FINISH'],
                     'NUMBER': 0}
        no_coord.append(cord_line)

    start_end_meta.append({'stantion_start': start_end_st[0]['STANTION_START'],
                           'stantion_start_name': start_end_st[0]['NAME_START'],
                           'stantion_finish': start_end_st[0]['STANTION_FINISH'],
                           'stantion_finish_name': start_end_st[0]['NAME_FINISH']})

    return mapp, start_end_meta, no_coord


def make_legend(mapp, title, uno):
    template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>
     
<div class='legend-title'>""" + title + """ <br>Уно - """ + uno + """</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:orange;opacity:0.7;'></span>Станции переработки</li>
    <li><span style='background:gray;opacity:0.7;'></span>Станции поезда</li>
    <li><span style='background:red;opacity:0.7;'></span>Станция отправления/назначения отправки</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)
    mapp.get_root().add_child(macro)
    return mapp


def getMapSOAP(month, poezd, icon_text=False):

    numbering, stantions, start_end = SOAPConnetor.getPoezdData(month, poezd)

    if not stantions:
        return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), 'no_data', [], [], []

    start_element = 0
    for row in stantions:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp = folium.Map(location=[stantions[start_element]['LAT'], stantions[start_element]['LON']], zoom_start=8,
                      control_scale=True)
    fs = plugins.Fullscreen()
    mapp.add_child(fs)

    # наносим станции
    no_coord = []
    for row in stantions:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord.append(row)
        else:
            if icon_text:
                div_icon = DivIcon(
                    icon_size=(120, 100),
                    icon_anchor=(60, 100),
                    html=f'<div style="font-size: 15px; color: white; background: rgba(0, 0, 0, 0.4); '
                         f'border: 2px solid white; padding: 2px; border-radius: 10px;">'
                         f'{row["STANTION"]} <br> {row["NAME"]}</div>')
                folium.Marker(location=[float(row['LAT']), float(row['LON'])],
                              icon=div_icon).add_to(mapp)

            mapp = add_icon_number_from_map(row, mapp)

    mapp, start_end_meta, no_coord = add_start_end_st(mapp, start_end, len(stantions), no_coord, poezd)

    return mapp._repr_html_(), '', no_coord, numbering, start_end_meta


def getMapUnoSOAP(month, uno, iddos):
    stantions, start_end_st, numbering, uno_list, stantions_cut = SOAPConnetor.getUnoData(month, uno, iddos)

    if not stantions:
        return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), 'no_data', [], [], [], [], folium.Map(zoom_start=5, control_scale=True)._repr_html_(), []

    start_element = 0
    for row in stantions:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp = folium.Map(location=[stantions[start_element]['LAT'], stantions[start_element]['LON']], zoom_start=8,
                      control_scale=True)
    fs = plugins.Fullscreen()
    mapp.add_child(fs)

    # наносим станции
    no_coord = []
    for row in stantions:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord.append(row)
        else:
            mapp = add_icon_number_from_map(row, mapp)
    # помечаем станции начала и конца
    mapp, start_end_meta, no_coord = add_start_end_st(mapp, start_end_st, len(stantions), no_coord)

##################################################
    # if not stantions_cut:
    #     return folium.Map(zoom_start=5, control_scale=True)._repr_html_(), []

    start_element = 0
    for row in stantions_cut:
        if row['LAT'] != '0':
            break
        start_element += 1
    mapp_uno = folium.Map(location=[stantions_cut[start_element]['LAT'], stantions_cut[start_element]['LON']],
                          zoom_start=8, control_scale=True)
    fs = plugins.Fullscreen()
    mapp_uno.add_child(fs)

    # наносим станции
    no_coord_uno = []
    for row in stantions_cut:
        if row['LAT'] == '0' or row['LON'] == '0' or row['LAT'] is None or row['LON'] is None:
            no_coord_uno.append(row)
        else:
            mapp_uno = add_icon_number_from_map(row, mapp_uno)
    # помечаем станции начала и конца
    mapp_uno, start_end_meta_uno, no_coord_uno = add_start_end_st(mapp_uno, start_end_st, len(stantions_cut), no_coord_uno)
    # return mapp_uno._repr_html_(), no_coord_uno

##################################################
    return mapp._repr_html_(), '', no_coord, start_end_meta, numbering, uno_list, mapp_uno._repr_html_(), no_coord_uno