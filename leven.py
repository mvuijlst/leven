""" Poging om iets te doen met datums """

import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def convert_date(string_date):
    """ datums converteren """

    return datetime.strptime(string_date, '%Y-%m-%d').date()

def main():
    " Hoofdding "

    with open('leven.json') as json_data:
        life = json.load(json_data)
        # print(life)

    birth = convert_date(life['birth'])
    now = datetime.now()

    css = ''
    periods = []
    for period in life['periods']:
        if period['code'] not in periods:
            css = css + '.' + period['code'] + '{background-color:#' + period['colour'] + ';}'
            periods.append(period['code'])

    thisdate = date(birth.year, 1, 1)
    enddate = date(now.year, now.month, now.day)

    output = '<!DOCTYPE html><html><head><title>Leven</title>'
    output = output + '<link rel="stylesheet" type="text/css" href="normalize.css" />'
    output = output + '<link rel="stylesheet" type="text/css" href="styles.css" />'
    output = output + '<style>' + css + '</style>'
    output = output + '<body><table>'
    output = output + '<tr class="months"><th></th><th>j</th><th>f</th>'
    output = output + '<th>m</th><th>a</th><th>m</th><th>j</th><th>j</th>'
    output = output + '<th>a</th><th>s</th><th>o</th><th>n</th><th>d</th></tr>'
    while thisdate < enddate:
        if thisdate.month == 1:
            output = output + '<tr><th>' + str(thisdate.year) + '</th>'
        style = ''
        for period in life['periods']:
            if thisdate >= convert_date(period['start']) and \
                thisdate <= convert_date(period['end']):
                style = style + ' ' + period['code']

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
        output = output + '</td>'
        if thisdate.month == 12:
            output = output + '</tr>'

        thisdate = thisdate + relativedelta(months=+1)
    output = output + '</table></body></html>'

    with open('leven.html', mode='w') as html:
        html.write(output)

if __name__ == "__main__":
    main()
