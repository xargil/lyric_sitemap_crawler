from scrapy import cmdline
import scrapy
from bs4 import BeautifulSoup

def removeHTMLCharachters(raw_text):
    return BeautifulSoup(raw_text).text

class ShironetSpider(scrapy.Spider):
    name = "shironet"
    BASE_URL = "http://shironet.mako.co.il"

    def start_requests(self):
        urls = [
            'http://shironet.mako.co.il/artist?lang=1&prfid=4091'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseArtistPage)

    def parseArtistPage(self, response):
        artist_name = str(response.css("h1::text").extract_first())
        self.log("Scraping artist: " + artist_name)
        songsOfArtist = response.css(".artist_player_songlist")
        for song in songsOfArtist:
            song_url = song.css("a::attr(href)").extract_first()
            full_song_url = self.BASE_URL + song_url

            yield scrapy.Request(url=full_song_url, callback=self.parseSongPage)
            break
        self.log("Artist page ended")

    def parseSongPage(self, response):
        artist_name = response.css(".artist_singer_title::text").extract_first()
        album_name = response.css(".artist_more_link::text").extract_first()
        album_year = int(response.css(".artist_color_gray::text").extract_first()[1:5])
        song_lyrics = removeHTMLCharachters(response.css(".artist_lyrics_text").extract_first())

        self.log("a")

cmdline.execute("scrapy runspider shironet_spider.py".split())
