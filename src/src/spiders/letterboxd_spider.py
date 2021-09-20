"""
Module containing main letterboxd Scrapy spider and associated functions
"""
from time import sleep
from scrapy import Request, Spider
from src.src.utils import sanitize_user


class LetterboxdSpider(Spider):
    """
    Spider class for crawling films watched of directed letterboxd user and extracting relevant data
    available
    """

    name = "letterboxd"
    allowed_domains = ["letterboxd.com"]

    # TODO: Remove page_test param
    def __init__(self, user='', page_test=False, **kwargs):
        """
        Class constructor

        :param user: Letterboxd account username to be crawled
        :param page_test: Flag indicating only the first page of user's watched films should be crawled
            (for debugging purposes only)
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.page_test = page_test
        self.user = sanitize_user(user)
        self.start_urls = ["https://letterboxd.com/" + user + "/films/"]

    def parse(self, response, **kwargs):
        """
        Main parse function for spider to retrieve and process data - yields dictionary of individual
        film data.
        """

        # Loops through each film poster element displayed on user's watched films page
        for film in response.css("li.poster-container"):

            data = {'Title': film.css("img::attr(alt)").get(), 'Rating': "n/a", 'Liked': "No",
                    'Watched': "n/a"}

            # Slightly messy if statements here due to awkward display of user rating/like data on page -
            # info stored only in class attribute of elements that may or may not exist, within a span
            # element that also may or may not exist
            rate = film.css("p.poster-viewingdata.-rated-and-liked > span")
            if rate:
                rated = rate.css('[class^="rating"]')
                liked = rate.css('[class^="like"]')
                if rated:
                    data['Rating'] = rated.xpath("@class").get()[-1] + "/10"
                if liked:
                    data['Liked'] = "Yes"
                # TODO: Get individual film page parsing working
                # url = utils.get_url(self.user + "/film/" + data['Title'].replace(" ", "-"))
                # Date user watched film not available on page, have to crawl individual film page
                # watched = response.follow(url, callback=self.get_watchdate)
                # if watched:
                #     data['Watched'] = watched

            yield data

        if not self.page_test:
            next_page = response.css("div.paginate-nextprev > a.next::attr(href)").get()
            if next_page is not None:
                url = response.urljoin(next_page)
                # Sleep for 5sec here to limit crawling speed
                sleep(5)
                yield Request(url, callback=self.parse)


# TODO: Implement film page parsing
def parse_film(response):
    """
    Parse individual film pages, extracting director and release date data

    :param response: html response
    :return: Dictionary containing film data
    """

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
