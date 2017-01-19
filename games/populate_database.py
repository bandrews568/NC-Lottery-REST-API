# Script used to populate the database tables
# For the most recent data we will use the information
# off the NC lottery RSS feed
import re
import time
import json
import urllib.request
import urllib.error
import logging
from datetime import datetime

from .models import (Pick3, Pick4, Cash5,
                     PowerBall, MegaMillions,
                     LuckyForLife)

import wget
from termcolor import colored
from bs4 import BeautifulSoup

GAMES = {
        'pick3_day': 'http://www.lotteryusa.com/north-carolina/midday-3/year',
        'pick3_evening': 'http://www.lotteryusa.com/north-carolina/pick-3/year',
        'pick4_day': 'http://www.lotteryusa.com/north-carolina/midday-pick-4/year',
        'pick4_evening': 'http://www.lotteryusa.com/north-carolina/pick-4/year',
        'cash5': 'http://www.lotteryusa.com/north-carolina/cash-5/year',
        'lucky_4_life': 'http://www.lotteryusa.com/north-carolina/lucky-4-life/year'
}

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.ERROR and logging.INFO)

color_attempt = colored('[Attempt] ', 'yellow')
color_error = colored('[Error] ', 'red')
color_success = colored('[Success] ', 'green')


def makesoup(url):
    """
        Request the page and parse the information
        to return a soup object.
    """
    try:
        req = urllib.request.Request(url)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page.read(), 'html.parser')
    except urllib.error.HTTPError as e:
        logger.error(color_error + "{} Response: {}".format(e.code, url))
        return
    except Exception as e:
        logger.error(color_error + "makesoup(): {}".format(e))
        return
    return soup


def format_date(date):
    """
        Change date to a format SQLite accepts.
        From: 'Thu, Nov 03, 2016'
        To: '2016-11-03'
    """
    try:
        og_date = datetime.strptime(date, "%a, %b %d, %Y")
        formatted_date = og_date.strftime('%Y-%m-%d')
        return formatted_date
    except Exception as e:
        logger.error(color_error + "format_date(): {}".format(e))


def pick3(url, time):
    try:
        logger.info(color_attempt + "Pick 3 '{}'".format(time))
        pick3_data = makesoup(url)
        get_date = pick3_data.find_all('td', {'class': 'date'})
        get_numbers = pick3_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Pick 3-{}): {}".format(time, e))
        return

    date_list = [format_date(line.text) for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure: u'\n6\n6\n0\n0\n\n'
        line = re.sub('\n', ',', line.text[1:], 2)
        # This is what we're working with now:
        # u'\n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    if time == 'day':
        pick3_list = zip("D" * len(date_list), date_list, number_list)
    elif time == 'evening':
        pick3_list = zip("E" * len(date_list), date_list, number_list)
    else:
        raise ValueError("Time must be either day or evening, got '{}'"
                         .format(time))

    for time, date, numbers in pick3_list:
        row_data = Pick3()
        row_data.drawing_time = time
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.save()
    # Data formats
    # ('D', u'2016-11-02, u'4,0,4')
    # ('E', u'2016-11-02', u'2,4,5')
    logger.info(color_success + "Pick 3 '{}'".format(time))


def pick4(url, time):
    try:
        logger.info(color_attempt + "Pick 4 '{}'".format(time))
        pick4_data = makesoup(url)
        get_date = pick4_data.find_all('td', {'class': 'date'})
        get_numbers = pick4_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Pick 4-{}): {}".format(time, e))
        return

    date_list = [format_date(line.text) for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure: u'\n6\n6\n0\n0\n\n'
        line = re.sub('\n', ',', line.text[1:], 3)
        # This is what we're working with now:
        # u'\n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    if time == 'day':
        pick4_list = zip("D" * len(date_list), date_list, number_list)
    elif time == 'evening':
        pick4_list = zip("E" * len(date_list), date_list, number_list)
    else:
        raise ValueError("Time must be either day or evening, got '{}'"
                         .format(time))

    for time, date, numbers in pick4_list:
        row_data = Pick4()
        row_data.drawing_time = time
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.save()

    # Data formats
    # ('D', u'2016-11-02', u'0,5,1,0')
    # ('E', u'2016-11-02', u'9,2,6,6')
    logger.info(color_success + "Pick 4 '{}'".format(time))


def cash5(url):
    try:
        logger.info(color_attempt + "Cash 5")
        cash5_data = makesoup(url)
        get_date = cash5_data.find_all('td', {'class': 'date'})
        get_numbers = cash5_data.find_all('td', {'class': 'result'})
        get_jackpot = cash5_data.find_all('td', {'class': 'jackpot'})
    except Exception as e:
        logger.error(color_error + "(Cash 5): {}".format(e))
        return

    date_list = [format_date(line.text) for line in get_date]
    # jackpot_list = [line.text.replace("$", "") for line in get_jackpot]
    jackpot_list = []
    number_list = []

    for line in get_jackpot:
        line = re.sub('\$|,', '', line.text)
        jackpot_list.append(line)

    for line in get_numbers:
        # This is the data structure: u'\n2\n6\n14\n31\n38\n\n'
        line = re.sub('\n', ',', line.text[1:], 4)
        # This is what we're working with now:
        # u'/n2,6,14,31,38\n\n'
        line = re.sub('\n', '', line)
        number_list.append(line)

    cash5_list = zip(date_list, number_list, jackpot_list)

    for date, numbers, jackpot in cash5_list:
        row_data = Cash5()
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.jackpot = jackpot
        row_data.save()
    # Data format
    # (u'2016-11-02', u'2,24,29,33,38', u'100000')
    logger.info(color_success + "Cash 5")


def powerball():
    try:
        logger.info(color_attempt + "Powerball")
        filename = "powerball_{}.txt".format(time.strftime("%m-%d-%Y"))
        url = "http://www.powerball.com/powerball/winnums-text.txt"
        wget.download(url, out=filename)
    except Exception as e:
        logger.error(color_error + "(Powerball): {}".format(e))
        return

    # Make sure we are looking at the current data
    # Example filename: powerball_10-16-2016.txt
    if not filename[10:20] == time.strftime("%m-%d-%Y"):
        raise ValueError("'{}' is not current".format(filename))

    date_list = []
    number_list = []
    powerball_list = []

    try:
        # Data structures:
        # Note: double spaces between all the powerball #'s
        # Without multiplier
        # 06/21/2000  43  01  28  27  24  25 \r\n
        # With
        # 04/19/2006  32  53  34  05  28  10  4 \r\n
        with open(filename, "r") as f:
            for line in f:
                try:
                    date_data = line[0:10]
                    raw_date = datetime.strptime(date_data, "%m/%d/%Y")
                    date = raw_date.strftime('%Y-%m-%d')
                except Exception as e:
                    logger.error(color_error + "(Powerball): {}".format(e))
                    logger.error(color_error + "(Powerball): {}".format(line))
                    continue
                raw_number_data = line[11:].strip().split("  ")
                powerball = raw_number_data.pop(-1)
                number_data = ','.join(raw_number_data)
                date_list.append(date)
                number_list.append(number_data)
                powerball_list.append(powerball)
    except IOError:
        logger.error(color_error + "opening: {}".format(filename))
        return

    powerball_data = zip(date_list, number_list, powerball_list)
    # Deleting: ('Draw Date ', ['WB1 WB2 WB3 WB4 WB5 PB', 'PP'])
    del powerball_list[0]

    for date, numbers, powerball in powerball_data:
        row_data = PowerBall()
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.powerball = powerball
        row_data.save()
    # Data format
    # ('2016-11-02', '18,54,61,13,37,05', '2')
    logger.info(color_success + "Powerball")


def mega_millions():
    """
        Data structure(JSON):
        {
        "draw_date": "2016-10-21T00:00:00.000",
        "mega_ball": "03",
        "multiplier": "04",
        "winning_numbers": "12 43 44 48 66"
        }
    """
    url = 'https://data.ny.gov/resource/h6w8-42p9.json'

    try:
        logger.info(color_attempt + "Mega Millions")
        open_page = urllib.request.urlopen(url).read().decode("utf-8")
        json_data = json.loads(open_page)
    except urllib.error.HTTPError as e:
        logger.error(color_error + "{} Response: {}".format(e.code, url))
        return
    except Exception as e:
        logger.error(color_error + "(Mega Millions): {}".format(e))

    mm_list = []

    for line in json_data:
        date = line['draw_date']
        # Take out the time: 2007-05-11T00:00:00.000
        date = re.sub('T\d\d:\d\d:00\.000', '', date)
        get_numbers = line['winning_numbers']
        numbers = get_numbers.replace(" ", ",")
        megaball = line['mega_ball']
        # Mulitiper isn't in older results so just pass None
        multiplier = line.get('multiplier', None)
        data = (date, numbers, megaball, multiplier)
        mm_list.append(data)

    for date, numbers, megaball, multiplier in mm_list:
        row_data = MegaMillions()
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.megaball = megaball
        row_data.multiplier = multiplier
        row_data.save()
    # Data format
    # (u'2016-11-01', u'19,24,31,39,45', '03', '05')
    logger.info(color_success + "Mega Millions")


def lucky_4_life(url):
    try:
        logger.info(color_attempt + "Lucky For Life")
        lucky_data = makesoup(url)
        get_date = lucky_data.find_all('td', {'class': 'date'})
        get_numbers = lucky_data.find_all('td', {'class': 'result'})
    except Exception as e:
        logger.error(color_error + "(Lucky For Life): {}".format(e))
        return

    date_list = [format_date(line.text) for line in get_date]
    number_list = []

    for line in get_numbers:
        # This is the data structure:
        # '\n6\n23\n33\n44\n45\n9  Lucky Ball\n'
        line = re.sub('\n', ' ', line.text)
        # This is what we're working with now:
        # ' 24 28 30 33 34 18  Lucky Ball '
        line = re.sub('Lucky Ball', '', line).strip()
        # Put commas between the numbers
        line = re.sub(' ', ',', line)
        number_list.append(line)

    lucky_list = zip(date_list, number_list)

    for date, numbers in lucky_list:
        row_data = LuckyForLife()
        row_data.drawing_date = date
        row_data.drawing_numbers = numbers
        row_data.save()
    # Data format
    # (u'2016-11-01', u'3,4,12,32,45,5')
    logger.info(color_success + "Lucky For Life")


def populate_database():
    pick3(GAMES['pick3_day'], 'day')
    pick3(GAMES['pick3_evening'], 'evening')
    pick4(GAMES['pick4_day'], 'day')
    pick4(GAMES['pick4_evening'], 'evening')
    cash5(GAMES['cash5'])
    powerball()
    mega_millions()
    lucky_4_life(GAMES['lucky_4_life'])


# populate_database()
