from Model.artist_url import artist_url

class shironet_config:
    SHIRONET_BASE_URL = "http://shironet.mako.co.il"
    SHIRONET_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    SHIRONET_COOKIE = {'rbzid': 'eFlIbjVMWGRDZHY4QUtaS09KbXdyTGZRSGhkazB6ZVowT0s4bzhGQWpPZ2F4aWplVkdTQUFVZDZtTGZZK09PZkdtcXdTMVV6Si9GaytDdmM1Vkh0SFF0QW12YldMQ0R4eXpCTzJXNld3UXU4QWxub2F1N21uT2ppa3ZxajMzSDQvSHhySUJramp6Tng4R3QxZVE3SEc2QXprOXhjcXpGcVFwZDJzU21pd3luRUIxQlZjTWQwK3daZlkrNDduZmZ2aU9SZFFoVW5tc0MxV09vaGdNbTlEQT09QEBAMEBAQC0xNDgxNDgxNDY4MA'}

    ARTIST_PAGE_PREFIX = "http://shironet.mako.co.il/artist?type=works&lang=1&prfid="
    ARTISTS_URLS = [
        artist_url("Idan Raichel",  ARTIST_PAGE_PREFIX + '1428'),
        artist_url("Eviatar Banai", ARTIST_PAGE_PREFIX + '41'),
        artist_url("Moshe Peretz", ARTIST_PAGE_PREFIX + '3787'),
        artist_url("Dudu Aharon", ARTIST_PAGE_PREFIX + '4592'),
        artist_url("Kobi Peretz", ARTIST_PAGE_PREFIX + '1202'),
        artist_url("Meir Ariel", ARTIST_PAGE_PREFIX + '605'),
        artist_url("Hadag Nahash", ARTIST_PAGE_PREFIX + '333'),
        artist_url("Lior Narkis", ARTIST_PAGE_PREFIX + '594'),
        artist_url("Mooki", ARTIST_PAGE_PREFIX + '620'),
        artist_url("Peer Tasi", ARTIST_PAGE_PREFIX + '7747'),
        artist_url("Eyal Golan", ARTIST_PAGE_PREFIX + '92'),
        artist_url("Omer Adam", ARTIST_PAGE_PREFIX + '10755'),
        artist_url("Regev Hod", ARTIST_PAGE_PREFIX + '2570'),
        artist_url("Sarit Hadad", ARTIST_PAGE_PREFIX + '1015'),
        artist_url("Shlomo Artzi", ARTIST_PAGE_PREFIX + '975'),
        artist_url("Shalom Hanoch", ARTIST_PAGE_PREFIX + '960'),
        artist_url("Arik Einstein", ARTIST_PAGE_PREFIX + '166'),
        artist_url("Rita", ARTIST_PAGE_PREFIX + '905'),
        artist_url("Miri Mesika", ARTIST_PAGE_PREFIX + '4226'),
        artist_url("Keren Peles", ARTIST_PAGE_PREFIX + '4314'),
        artist_url("Assaf Amdursky", ARTIST_PAGE_PREFIX + '150'),
        artist_url("Avraham Tal", ARTIST_PAGE_PREFIX + '7335'),
        artist_url("Mashina", ARTIST_PAGE_PREFIX + '686'),
        artist_url("Yehoram Gaon", ARTIST_PAGE_PREFIX + '465'),
        artist_url("Yishi Levi", ARTIST_PAGE_PREFIX + '559'),
        artist_url("Avi Biter", ARTIST_PAGE_PREFIX + '1145'),
        artist_url("Shlomi Shabat", ARTIST_PAGE_PREFIX + '966'),
        artist_url("Zehava Ben", ARTIST_PAGE_PREFIX + '372'),
        artist_url("Zohar Argov", ARTIST_PAGE_PREFIX + '373'),
        artist_url("Lior Farhi", ARTIST_PAGE_PREFIX + '596'),
        artist_url("Shimi Tavori", ARTIST_PAGE_PREFIX + '955'),
        artist_url("Ofer Levi", ARTIST_PAGE_PREFIX + '783'),
        artist_url("Moshik Afia", ARTIST_PAGE_PREFIX + '623'),
        artist_url("Zehava Ben", ARTIST_PAGE_PREFIX + '372'),
        artist_url("Idan Yaniv", ARTIST_PAGE_PREFIX + '4858'),
        artist_url("Margalit Tzanani", ARTIST_PAGE_PREFIX + '666'),
        artist_url("Boaz Sharabi", ARTIST_PAGE_PREFIX + '183')
    ]