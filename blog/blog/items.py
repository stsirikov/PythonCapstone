from scrapy import Item, Field


class AuthorItem(Item):
    name = Field()
    job = Field()
    url = Field()


class TagItem(Item):
    name = Field()


class ArticleItem(Item):
    title = Field()
    date = Field()
    text = Field()
    url = Field()


class BlogItem(Item):
    article = Field()
    authors = Field()
    tags = Field()
    