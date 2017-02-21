from scrapy import cmdline
import scrapy
from bs4 import BeautifulSoup
from DataHandlers import elastic_handler
import time
import Model.artist_url
from Model.artist_url import artist_url


def removeHTMLCharachters(raw_text):
    return BeautifulSoup(raw_text).text

class ShironetSpider(scrapy.Spider):
    name = "shironet"
    BASE_URL = "http://shironet.mako.co.il"
    SPIDER_AGENTS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    SPIDER_COOKIES = {'rbzid': 'a21VNy8wdmdRT2ZPTWU5TVRyeXAyQWRoaWEwWHVvdVJWNXdjeGVGbXZyaVFIV0NOTVNWaEtHWEhNUVJrZitsWkpjZ2VZMHVsejB3d0NkTWFZUU5jaEdzaHBxVmJRUVI0elVqZ0xBTFhjOUFaOVNORGZmbStpZmlZQWxJdHBuK1l1UlJCSnBaMFJmQXErT0hWYjVkdmJRM1lXMnBEMm9KR1FFMEp2NVNKdXNESng5ekYyQ2Z4K3JxVExPcDRlR2lWSjdYcVBzWEVNOXB5L2dlVzBjUXhDZz09QEBAMEBAQC0xNDgxNDgxNDY4MA'}

    def __init__(self):
        self.es_handler = elastic_handler.ElasticSeachHandler()

    def start_requests(self):
        artist_urls = [
            artist_url("Dor Daniel",'http://shironet.mako.co.il/artist?type=works&lang=1&prfid=1333')
        ]

        for curr_artist in artist_urls:
            yield scrapy.Request(url=curr_artist.url,
                                 meta={"artist_name": curr_artist.english_name},
                                 headers=self.SPIDER_AGENTS,
                                 cookies=self.SPIDER_COOKIES,
                                 callback=self.parseArtistPage)

    def parseArtistPage(self, response):
        # check if request was successfuly
        if len(response.css(".menu")) == 0:
            print("\nNeed to replace cookie!")
            print("Url " + response.url)
        else:
            artist_name = str(response.css("h1::text").extract_first())
            self.log("Scraping artist: " + artist_name)
            songsOfArtist = response.css(".artist_player_songlist")
            for song in songsOfArtist:
                song_url = song.css("a::attr(href)").extract_first()
                full_song_url = self.BASE_URL + song_url

                yield scrapy.Request(url=full_song_url,
                                     meta={"artist_name": response.meta["artist_name"]},
                                     headers=self.SPIDER_AGENTS,
                                     cookies=self.SPIDER_COOKIES,
                                     callback=self.parseSongPage)

            # check if there is anoother page
            nav_bar_len = len(response.css(".artist_nav_bar")) - 1
            last_nav_bar_text = str(response.css(".artist_nav_bar::text")[nav_bar_len].extract())
            last_nav_bar_href = self.BASE_URL + str(response.css(".artist_nav_bar::attr(href)")[nav_bar_len].extract())
            if "הבא" in str(last_nav_bar_text):
                yield scrapy.Request(url=last_nav_bar_href,
                                     meta={"artist_name": response.meta["artist_name"]},
                                     headers=self.SPIDER_AGENTS,
                                     cookies=self.SPIDER_COOKIES,
                                     callback=self.parseArtistPage)

        self.log("Artist {0} all pages ended".format(response.meta["artist_name"]))

    def parseSongPage(self, response):
        # check if request was successfuly
        if len(response.css(".menu")) == 0:
            print("\nNeed to replace cookie!")
            print("Url " + response.url)
        else:
            artist_name = response.meta["artist_name"]
            album_name = response.css(".artist_more_link::text").extract_first()
            album_year_text = response.css(".artist_color_gray::text").extract_first()
            if album_year_text != None:
                album_year = int(album_year_text[1:5])
            else:
                album_year = 1
            song_name = response.css(".artist_song_name_txt > h1::text").extract_first()
            song_lyrics = removeHTMLCharachters(response.css(".artist_lyrics_text").extract_first())

            song = {
                "title": song_name,
                "album": {
                    "title": album_name,
                    "year": album_year
                },
                "artist": {
                    "unique_name": artist_name
                },
                "lyrics": song_lyrics
            }

            self.es_handler.index_song(song)

            print("Song {0} of {1} was scraped".format(song_name, artist_name))

cmdline.execute("scrapy runspider shironet_spider.py".split())
