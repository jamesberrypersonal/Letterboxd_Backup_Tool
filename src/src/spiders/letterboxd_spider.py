# imports
import scrapy
import time


# Spider class - crawls the films page of the directed letterboxd user, extracting the titles of their
# watched films, and the rating they gave if any
class LetterboxdSpider(scrapy.Spider):

    # Variable declarations
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]

    # Constructor - optional argument to pass users letterboxd username (defaults to my own for now because I'm
    # lazy and don't want to pass it in every time I test)
    # TODO: clean default user arg
    def __init__(self, user="fruityjames", **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.start_urls = ["https://letterboxd.com/" + user + "/films/"]
        # TODO: sanitize user input

    # Spiders parse function for retrieving and processing data - outputs dictionary of films, with title and
    # rating keys (rating set to n/a if film not rated by user)
    def parse(self, response):

        for film in response.css("li.poster-container"):
            data = {}
            data['Title'] = film.css("img::attr(alt)").get()
            # Messy section here due to how ratings are displayed on page - numeric rating value only present
            # at end of class attribute of a span element that may not exist (if user hasn't rated the film)
            rating = film.css("p.poster-viewingdata.-rated-and-liked > span").xpath("@class").get()
            if rating is not None:
                # TODO: fix bug here stupid (ratings with half stars get processed as '1/2/10')
                data['Rating'] = rating[-1] + "/10"
            else:
                data['Rating'] = "n/a"
            yield data

        # Obtaining the next page (if it exists) to continue crawling
        next_page = response.css("div.paginate-nextprev > a.next::attr(href)").get()
        if next_page is not None:
            url = response.urljoin(next_page)
            # Sleep for 5sec here to limit crawling speed
            time.sleep(5)
            yield scrapy.Request(url, callback=self.parse)
