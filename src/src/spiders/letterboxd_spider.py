# imports
import scrapy
import time


# Spider class - crawls the films page of the directed letterboxd user, extracting the titles of their
# watched films, and the rating they gave if any
class LetterboxdSpider(scrapy.Spider):

    # Variable declarations
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]

    # Constructor
    # Arguments:
    #       -user: letterboxd account username to be crawled (Set to my own right now out bc I'm lazy while
    #                testing)
    #       -pagetest: flag to indicate only want to crawl the first page of the users films - intended to
    #                    speed up testing when tests don't depend on crawling all pages (Set to true right now
    #                    for same reason as above)
    # TODO: fix issue of args not being set
    # TODO: clean args before pushing to main
    def __init__(self, user="fruityjames", pagetest=True, **kwargs):
        super().__init__(**kwargs)
        self.page_test = pagetest
        self.user = LetterboxdSpider.sanitize_user(user)
        self.start_urls = ["https://letterboxd.com/" + user + "/films/"]

    # Spiders parse function for retrieving and processing data - outputs dictionary of films, with title and
    # rating keys (rating set to n/a if film not rated by user)
    def parse(self, response):

        for film in response.css("li.poster-container"):
            data = {'Title': film.css("img::attr(alt)").get(), 'Rating': "n/a", 'Liked': "No"}
            # Messy section here due to how ratings are displayed on page - user rating and liked status
            # only present in a span element that may not exist (if user hasn't rated/liked the film) and
            # rating numeric value only present within class attribute of the span element
            rate = film.css("p.poster-viewingdata.-rated-and-liked > span")
            if rate:
                rated = rate.css('[class^="rating"]')
                liked = rate.css('[class^="like"]')
                if rated:
                    data['Rating'] = rated.xpath("@class").get()[-1] + "/10"
                if liked:
                    data['Liked'] = "Yes"
            yield data

        # Obtaining the next page (if it exists) to continue crawling - if page_test is set then skip (to
        # speed up testing that isn't specifically dependent crawling through all pages)
        if not self.page_test:
            next_page = response.css("div.paginate-nextprev > a.next::attr(href)").get()
            if next_page is not None:
                url = response.urljoin(next_page)
                # Sleep for 5sec here to limit crawling speed
                time.sleep(5)
                yield scrapy.Request(url, callback=self.parse)

    @staticmethod
    # TODO: Implement input sanitizing
    def sanitize_user(user):
        return user
