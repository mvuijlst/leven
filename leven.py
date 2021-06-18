""" Poging om iets te doen met datums """

import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def convert_date(string_date):
    """ datums converteren """

    return datetime.strptime(string_date, '%Y-%m-%d').date()

def get_name(period):
    """ naam uit studie of werk halen """

    name = ""
    if 'name' in period:
        name += period['name']
    if 'institution' in period:
        name += period['institution']
    if 'location' in period:
        name += ', '
        name += period['location']
    return name

def main():
    " Hoofdding "

    with open('mvuijlst.json') as json_data:
        life = json.load(json_data)
        # print(life)

    birth = convert_date(life['basics']['birth']['date'])
    now = datetime.now()

    css = ''
    legend = '<p><strong>Legende</strong></p><table class="legend">'
    periods = []
    for section in ['education', 'work']:
        for period in life[section]:
            if period['code'] not in periods:
                css = css + '.' + period['code'] + '{background-color:#' + period['colour'] + ';}'
                legend = legend + '<tr><td class="' + period['code'] + '"></td>' + \
                    '<th>' + get_name(period) + '</th></tr><tr><th colspan="3"></th></tr>'
                periods.append(period['code'])
    legend +=  '</table></body></html>'

    thisdate = date(birth.year, 1, 1)
    enddate = date(now.year, now.month, now.day)

    output = '<!DOCTYPE html><html><head><title>Leven</title>'
    output = output + '<link rel="stylesheet" type="text/css" href="normalize.css" />' + \
                '<link rel="stylesheet" type="text/css" href="styles.css" />' + \
                '<style>' + css + '</style></head>' + \
                '<body><table>'
    months = '<tr class="months"><th></th><th>j</th><th>f</th>' + \
                '<th>m</th><th>a</th><th>m</th><th>j</th><th>j</th>' + \
                '<th>a</th><th>s</th><th>o</th><th>n</th><th>d</th></tr>'

    output += months

    while thisdate < enddate:
        ttt = ''

        if thisdate.month == 1:
            output = output + '<tr><th>' + str(thisdate.year) + '</th>'
        style = ''
        for section in ['education', 'work']:
            for period in life[section]:
                if thisdate >= convert_date(period['startDate']) and \
                    thisdate <= convert_date(period['endDate']):
                    style = style + ' tt ' + period['code']
                    ttt = str(thisdate.month) + '/' + str(thisdate.year) + \
                        '<br />' + get_name(period)

        # border rules
        if thisdate.month == 12 \
            or (thisdate.month == now.month and thisdate.year == now.year):
            style = style + ' b_r'
        if (thisdate.month == 1 and thisdate > birth) \
            or (thisdate.month == birth.month and thisdate.year == birth.year):
            style = style + ' b_l'
        if (thisdate.month >= birth.month and thisdate.year == birth.year) \
            or (thisdate.month < birth.month and thisdate.year == birth.year + 1):
            style = style + ' b_t'
        if (thisdate.month <= now.month and thisdate.year == now.year) \
            or (thisdate.month > now.month and thisdate.year == now.year - 1):
            style = style + ' b_b'
        if thisdate.month < birth.month and thisdate.year == birth.year:
            style = style + ' b_0'

        if style != '':
            output = output + '<td class="' + style[1:] + '">'
        else:
            output = output + '<td>'
        if thisdate >= date(birth.year, birth.month, 1):
            output = output + str(thisdate.month)
            if ttt != '':
                output = output + '<b class="ttt">' + ttt + '</b>'
        output = output + '</td>'
        if thisdate.month == 12:
            output = output + '</tr>'

        thisdate = thisdate + relativedelta(months=+1)

    output += months
    output += '</table>'

    output += legend

    with open('leven.html', mode='w') as html:
        html.write(output)

if __name__ == "__main__":
    main()
