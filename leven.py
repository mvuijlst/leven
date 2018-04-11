""" Poging om iets te doen met datums """

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def main():
    " hoofdding "

    birth = date(1970, 7, 27)
    now = datetime.now()

    thisdate = date(birth.year, 1, 1)
    enddate = date(now.year, now.month, now.day)

    print('<html><head><title>Leven</title>')
    print('<body>')
    print('<table>')
    while thisdate < enddate:
        if thisdate.month == 1:
            print('<tr><td>', str(thisdate.year)[2:], '</td>', sep='', end='')
        print('<td>', thisdate.month, '</td>', sep='', end='')
        if thisdate.month == 12:
            print('</tr>')

        thisdate = thisdate + relativedelta(months=+1)
    print('</table>')
    print('</body>')
    print('</html>')

if __name__ == "__main__":
    main()
