# Used to retrieve the most current lottery data daily

import re
from time import strptime
from datetime import datetime

# from .populate_database import (cash5, powerball,
#                                 mega_millions, GAMES)
from .models import (Pick3, Pick4, Cash5,
                     PowerBall, MegaMillions,
                     LuckyForLife)

import feedparser


def trim_spaces(data):
    return data.replace(' ', '')


def format_data(summary, title):
    """
    Used to format the number and date data for each game.
    Example summary: 21-22-29-38-40
    Example title: Powerball Winning Numbers on Wednesday, January 18, 2017
    """
    numbers = summary.replace('-', ',')

    if 'PB' or 'MB' in numbers:
        numbers = re.sub('PB|PP|MB|MP', '', numbers)
        numbers = trim_spaces(numbers).replace(',,', ',')

    if ',' in title:
        raw_date = title.split(',')
        date_year = raw_date[2]
        # Change ' Nov' to a numerical number(note space before)
        date_month = strptime(raw_date[1][0:4].lstrip(), '%b').tm_mon
        date_day = re.findall(' \d.*$', raw_date[1])
        date_day = trim_spaces(date_day[0])

        if len(date_day) == 1:
            date_day = '0' + date_day[0]
            date_day = trim_spaces(date_day)

        date = date_year + '-' + str(date_month) + '-' + date_day
        date = trim_spaces(date)
    else:
        # Lucky for Life is formatted differently than the rest
        # title: 'Lucky For Life Winning Numbers on 10/31/2016'
        raw_date = re.findall('\d*./\d*./\d*.$', title)
        raw_date = raw_date[0]
        raw_date = datetime.strptime(raw_date, '%m/%d/%Y')
        date = raw_date.strftime('%Y-%m-%d')
    return date, numbers


def write_to_database(date, numbers, model, **kwargs):
    time = kwargs.get('time', None)
    jackpot = kwargs.get('jackpot', None)
    _powerball = kwargs.get('powerball', None)
    powerplay = kwargs.get('powerplay', None)
    megaball = kwargs.get('megaball', None)
    multiplier = kwargs.get('multiplier', None)

    row_data = model()

    if time and model == Pick3 or model == Pick4:
        row_data.drawing_time = time

    if jackpot and model == Cash5:
        row_data.jackpot = jackpot

    if _powerball and model == PowerBall:
        row_data.powerplay = powerplay
        row_data.powerball = _powerball

    if megaball and multiplier and model == MegaMillions:
        row_data.megaball = megaball
        row_data.multiplier = multiplier

    row_data.drawing_date = date
    row_data.drawing_numbers = numbers
    row_data.save()


def scrape_rss():
    """
    Used to scrape data for Pick3, Pick4, and Lucky for Life.
    Date is in the title tag except for the Carolina
    Pick 3 evening drawing.
    'title': 'Carolina Pick 3 Evening Winning Numbers',
    'summary': '4-4-8',
    """
    url = 'http://www.nc-educationlottery.org/rss_winning_numbers.aspx'
    rss_data = feedparser.parse(url)

    for i in range(len(rss_data['entries'])):
        entry = rss_data['entries'][i]
        summary = entry['summary']  # number data
        title = entry['title']  # game name and date

        if 'Carolina Pick 3 Daytime' in title:
            data = format_data(summary, title)
            write_to_database(data[0], data[1], Pick3, time="D")

        elif 'Carolina Pick 3 Evening' in title:
            # Date is in 'published' instead of title.
            # 'published': u'Monday, October 31, 2016'
            data = format_data(summary, entry['published'])
            write_to_database(data[0], data[1], Pick3, time="E")

        elif 'Carolina Pick 4 Daytime' in title:
            data = format_data(summary, title)
            write_to_database(data[0], data[1], Pick4, time="D")

        elif 'Carolina Pick 4 Evening' in title:
            data = format_data(summary, title)
            write_to_database(data[0], data[1], Pick4, time="E")

        elif 'Lucky For Life Winning Numbers' in title:
            data = format_data(summary, title)
            write_to_database(data[0], data[1], LuckyForLife)

# scrape_rss()
# cash5(GAMES['cash5'])
# powerball()
# mega_millions()
