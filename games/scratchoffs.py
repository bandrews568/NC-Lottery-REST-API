from bs4 import BeautifulSoup


all_games_url = "http://www.nc-educationlottery.org/instant.aspx?"

def getGameLinks(url):
    request_page = makesoup(url)
    game_urls = request_page.find_all


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