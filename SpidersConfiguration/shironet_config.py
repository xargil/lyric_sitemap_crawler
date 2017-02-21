from Model.artist_url import artist_url

class shironet_config:
    SHIRONET_BASE_URL = "http://shironet.mako.co.il"
    SHIRONET_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    SHIRONET_COOKIE = {'rbzid': 'WjBhcWcwUXh0VlV1WW1rSHYzdHF2MExVVUh3aHV3S25GeVNIbmo4RHZ3Y1A2NWU1eHlPV2VRY2ZTVUMzaUhaRWNKc0RzWjhGbEJIemNOTUJhQjBBSU1VU2g5OFBlZ3hUWVBXSGZwcnhJR2VNdmZub3YvaDNuaTFJeERlam5pcXlZM3JDS2M5blR1d0QycE9PMFE3a2RoUEpDZHExQzdHc2tXZTdkeUFtNnBiZzVXMGVOTFEyK3BERi93cWxGYW5aTmo3Q1p2K3JwM0hVeUQ4WU1XMzVpZz09QEBAMkBAQC0xNDgxNDgxNDY4MA'}

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
        #artist_url("Mooki", ARTIST_PAGE_PREFIX + '620'),
        #artist_url("Peer Tasi", ARTIST_PAGE_PREFIX + '7747'),
        #artist_url("Eyal Golan", ARTIST_PAGE_PREFIX + '92'),
        #artist_url("Omer Adam", ARTIST_PAGE_PREFIX + '10755'),
        #artist_url("Regev Hod", ARTIST_PAGE_PREFIX + '2570')
        #artist_url("Sarit Hadad", ARTIST_PAGE_PREFIX + '1015')
        #artist_url("Shlomo Artzi", ARTIST_PAGE_PREFIX + '975')
        #artist_url("Shalom Hanoch", ARTIST_PAGE_PREFIX + '960')
        #artist_url("Arik Einstein", ARTIST_PAGE_PREFIX + '166')
        #artist_url("Rita", ARTIST_PAGE_PREFIX + '905')
        #artist_url("Miri Mesika", ARTIST_PAGE_PREFIX + '4226')
        #artist_url("Keren Peles", ARTIST_PAGE_PREFIX + '4314')
        #artist_url("Assaf Amdursky", ARTIST_PAGE_PREFIX + '150')
        #artist_url("Avraham Tal", ARTIST_PAGE_PREFIX + '7335')
        #artist_url("Mashina", ARTIST_PAGE_PREFIX + '686')
        artist_url("Yehoram Gaon", ARTIST_PAGE_PREFIX + '465')

    ]