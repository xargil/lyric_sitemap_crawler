from scrapy import cmdline
import scrapy
from bs4 import BeautifulSoup
from DataHandlers import elastic_handler
from SpidersConfiguration.shironet_config import shironet_config


def removeHTMLCharachters(raw_text):
    return BeautifulSoup(raw_text).text

class ShironetSpider(scrapy.Spider):
    name = "shironet"
    BASE_URL = shironet_config.SHIRONET_BASE_URL
    SPIDER_AGENTS = shironet_config.SHIRONET_AGENT
    SPIDER_COOKIES = shironet_config.SHIRONET_COOKIE
    number_of_scrapped_songs = 0

    def __init__(self):
        self.es_handler = elastic_handler.ElasticSeachHandler()

    def close(self, reason):
        print("\n\nTotal songs scrapped :{0}\n\n".format(self.number_of_scrapped_songs))

    def start_requests(self):
        for curr_artist in shironet_config.ARTISTS_URLS:
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
            song_number = response.url[response.url.index("wrkid") + 6:]
            song_id_raw = artist_name + " " + song_number
            song_id = song_id_raw.replace(" ", "_")

            song = {
                "title": song_name,
                "source": "shironet",
                "album": {
                    "title": album_name,
                    "year": album_year
                },
                "artist": {
                    "unique_name": artist_name
                },
                "lyrics": song_lyrics
            }

            self.es_handler.index_song(song, song_id)
            self.number_of_scrapped_songs += 1

            print("Song {0} was scraped".format(song_id))

cmdline.execute("scrapy runspider shironet_spider.py".split())
