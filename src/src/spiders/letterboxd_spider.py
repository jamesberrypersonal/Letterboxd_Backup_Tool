# imports
import scrapy
import time


# Spider class - crawls the films page of the directed letterboxd user, extracting the basic data of
# their watched films, as well as user generated data (likes, ratings, watched date) if available
class LetterboxdSpider(scrapy.Spider):

    # Variable declarations
    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]

    # Constructor
    # Arguments:
    #       -user: letterboxd account username to be crawled (Set to my own right now out bc I'm lazy while
    #                testing)
    #       -page_test: flag to indicate only want to crawl the first page of the users films - intended to
    #                    speed up testing when tests don't depend on crawling all pages (Set to true right now
    #                    for same reason as above)
    # TODO: fix issue of args not being set
    # TODO: clean args before pushing to main
    def __init__(self, user="fruityjames", page_test=True, **kwargs):
        super().__init__(**kwargs)
        self.page_test = page_test
        self.user = LetterboxdSpider.sanitize_user(user)
        self.start_urls = ["https://letterboxd.com/" + user + "/films/"]

    # Spiders parse function for retrieving and processing data - outputs dictionaries of film data for the
    # individual films in user's watched films
    # TODO: Clean up commenting
    def parse(self, response):

        # Loops through each film poster element displayed on user's watched films page
        for film in response.css("li.poster-container"):

            # Output dictionary of film data
            data = {'Title': film.css("img::attr(alt)").get(), 'Rating': "n/a", 'Liked': "No",
                    'Watched': "n/a"}

            # Other than title, have to crawl individual film page to obtain data on each film
            url = self.get_url("/film/" + data['Title'].replace(" ", "-"))
            film_info = response.follow(url, callback=self.parse_film)
            data['Director'] = film_info['Director']
            data['Released'] = film_info['Released']

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
                url = self.get_url(self.user + "/film/" + data['Title'].replace(" ", "-"))
                # Date user watched film not available on page, have to crawl individual film page
                watched = response.follow(url, callback=self.get_watchdate)
                if watched:
                    data['Watched'] = watched

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

    # TODO: Implement film page parsing
    # Function to parse individual film pages and extract the directors and release date
    def parse_film(self, response):

        film_info = {'Director': "n/a", 'Released': "n/a"}

        attrs = response.css("section.film-header-lockup > p")
        rel = attrs.css('a[href^="/films/"]::text').get()
        dirs = attrs.css('a[href^="/director/"] span::text').getall()
        if rel:
            film_info['Released'] = rel
        if dirs:
            s = ", "
            film_info['Director'] = s.join(dirs)
        yield film_info

    # TODO: Make sure yield stuff is working
    # Function to extract date user watched film, if available
    def get_watchdate(self, response):

        if not response.css('[class^="error"]'):
            watchdate = response.css('p[class^="view-date"] a::text').getall()
            if not watchdate:
                yield 0
            else:
                s = " "
                yield s.join(watchdate)
        else:
            yield 0

    # Helper function to generate url strings
    @staticmethod
    def get_url(url_string):
        url = "https://letterboxd.com/" + url_string
        return url

    # Helper function to sanitize initial user input (ensure corresponds to an actually existing
    # letterboxd user
    # TODO: Implement user input sanitizing
    @staticmethod
    def sanitize_user(user):
        return user
