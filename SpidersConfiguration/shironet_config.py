from Model.artist_url import artist_url

class shironet_config:
    SHIRONET_BASE_URL = "http://shironet.mako.co.il"
    SHIRONET_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    SHIRONET_COOKIE = {'rbzid': 'Y2ZYVmtJRnhaRUR4TVdZNjZ6TVpEcUliaTFFa1hWUk51eXBrUldVcXNtMzhqdmp0RkRCZE4wb04zYXh1QlRzWnJiM0dkNGZiTW1tVUtoNENtOVVEb1Q0N2hoZm9HM1AxcjhjajE4UGM4VXZEQ0ZDUy9EZ2c5bjBYcnphcmxFdUlxOCszTXJlWHprc2QzenRGSy84VS9EeUp6d1I5dWNZdmJiQmxsellqcysxaW9JbXpoVVc1K0MzdjFBWXQxWm8raW1oeHVyUGtQTERPYnNrUTh6bjBPUT09QEBAMUBAQC0xNDgxNDgxNDY4MA'}

    ARTIST_PAGE_PREFIX = "http://shironet.mako.co.il/artist?type=works&lang=1&prfid="
    ARTISTS_URLS = [
        #artist_url("Idan Raichel",  ARTIST_PAGE_PREFIX + '1428'),
        #artist_url("Eviatar Banai", ARTIST_PAGE_PREFIX + '41'),
        #artist_url("Moshe Peretz", ARTIST_PAGE_PREFIX + '3787'),
        #artist_url("Dudu Aharon", ARTIST_PAGE_PREFIX + '4592'),
        #artist_url("Kobi Peretz", ARTIST_PAGE_PREFIX + '1202'),
        #artist_url("Meir Ariel", ARTIST_PAGE_PREFIX + '605'),
        #artist_url("Hadag Nahash", ARTIST_PAGE_PREFIX + '333'),
        #artist_url("Lior Narkis", ARTIST_PAGE_PREFIX + '594'),
        artist_url("Mooki", ARTIST_PAGE_PREFIX + '620')
    ]