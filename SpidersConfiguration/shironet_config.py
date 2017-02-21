from Model.artist_url import artist_url

class shironet_config:
    SHIRONET_BASE_URL = "http://shironet.mako.co.il"
    SHIRONET_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    SHIRONET_COOKIE = {'rbzid': 'U3BEbTBJWk5nNGRIT29leDdESmdHMVVFTkFuUkVwTStBam9KSWgrSWlZT1NRd3BHNVpPNXovTWo3NzFPblBEeS9mZWI3WDgrUGxQZEJvOXFVV3ZBRlU0UXFCVDVnU28raU9nNlN4Qnhaakw0c2MrNkp0Wno2dFpadWlWS3JTYUZJaFBaelR3UUZZaVg3azBUdjFRYVdwYnBEM2tnU0FsUzFIOG9wdHhkSGxGM0p2OHlmVWVya0hGd3dyRklNNW1Qb1pXL3A5T2FndmVMcHp5TU5YK3pNZz09QEBAMUBAQC0xNDgxNDgxNDY4MA'}

    ARTIST_PAGE_PREFIX = "http://shironet.mako.co.il/artist?type=works&lang=1&prfid="
    ARTISTS_URLS = [
        #artist_url("Idan Raichel",  ARTIST_PAGE_PREFIX + '1333'),
        #artist_url("Eviatar Banai", ARTIST_PAGE_PREFIX + '41')
        artist_url("Moshe Peretz", ARTIST_PAGE_PREFIX + '3787')
    ]