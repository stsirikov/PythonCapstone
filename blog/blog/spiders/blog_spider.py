from datetime import datetime
from scrapy import Spider, Request

from blog.items import ArticleItem, AuthorItem, TagItem, BlogItem


class BlogSpider(Spider):
    name = "blog"
    start_urls = ["http://blog.griddynamics.com/"]

    def __init__(self, last_date=None, *args, **kwargs):
        if last_date == None:
            self.last_date = datetime.min
        else:
            self.last_date = datetime.strptime(last_date, "%Y-%m-%d")
        super(BlogSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """Parse main page for links to articles by domain."""
        for domain in response.xpath(
            '//section[contains(@class, "domainblock")]/div/h2/a/@href'
        ).getall():
            domain_page = response.urljoin(domain)
            yield Request(domain_page, callback=self.domain_parse)

    def domain_parse(self, response):
        """Parse all articles from a single domain."""
        for article in response.xpath(
            '//a[contains(@class, "card cardtocheck")]/@href'
        ).getall():
            article_page = response.urljoin(article)
            yield Request(article_page, callback=self.article_parse)

    def article_parse(self, response):
        """Parse article page."""
        container = "section[id=hero] div[id=wrap]"
        date = datetime.strptime(
            response.css(f"{container} div[class=sdate]::text")[0]
            .get()
            .strip("\n\t •"),
            "%b %d, %Y",
        )
        if date < self.last_date:
            return
        title = response.css(f"{container} h1[class=mb30]::text")[0].get()
        authors_links = response.css(
            f"{container} div[class=sauthor] span[itemprop=author] a[class=goauthor]::attr(href)"
        ).getall()
        authors_names = list(
            filter(
                lambda x: x != "",
                map(
                    lambda x: x.strip(' "\n\t'),
                    response.css(f"{container} span[class=name]::text").getall(),
                ),
            )
        )
        tags_names = response.xpath('//meta[@property="article:tag"]/@content').getall()
        yield from map(lambda x: TagItem(name=x), tags_names)
        text = "\n".join(response.xpath("//p/text()").getall())[:160]
        for author in authors_links:
            author_page = response.urljoin(author)
            yield Request(author_page, callback=self.author_parse)
        yield ArticleItem(title=title, date=date, text=text, url=response.url)
        yield BlogItem(article=title, authors=authors_names, tags=tags_names)

    def author_parse(self, response):
        """Parse author page."""
        card = '//div[@class="modalbg"]/div[@class="authorcard popup"]'
        name = response.xpath(f'{card}//div[@class="titlewrp"]/h3/text()')[0].get()
        job_container = response.xpath(
            f'{card}//div[@class="titlewrp"]/p[@class="jobtitle"]/text()'
        )
        if len(job_container) != 0:
            job = job_container[0].get()
        else:
            job = None
        links = response.xpath(f'{card}//a[contains(@class, "linkedin")]/@href')
        if len(links) != 0:
            link = links[0].get()
        else:
            link = None
        yield AuthorItem(name=name, job=job, url=link)
