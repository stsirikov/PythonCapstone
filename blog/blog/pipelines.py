from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_

from blog.items import ArticleItem, AuthorItem, BlogItem, TagItem
from blog.database import engine, Article, Author, Authorship, Tag, Tagged

Session = sessionmaker(bind=engine)


class BlogPipeline:
    def open_spider(self, spider):
        self.session = Session()

    def process_item(self, item, spider):
        if isinstance(item, TagItem):
            name = item["name"]
            if not self.session.query(
                self.session.query(Tag).filter(Tag.name == name).exists()
            ).scalar():
                self.session.add(Tag(name=name))
            self.session.commit()
        elif isinstance(item, AuthorItem):
            name = item["name"]
            job = item["job"]
            url = item["url"]
            if not self.session.query(
                self.session.query(Author).filter(Author.name == name).exists()
            ).scalar():
                self.session.add(Author(name=name, job=job, linkedin=url))
            else:
                self.session.query(Author).filter(Author.name == name).update(
                    {Author.job: job, Author.linkedin: url}, synchronize_session=False
                )
            self.session.commit()
        elif isinstance(item, ArticleItem):
            title = item["title"]
            date = item["date"]
            text = item["text"]
            url = item["url"]
            if not self.session.query(
                self.session.query(Article).filter(Article.title == title).exists()
            ).scalar():
                self.session.add(Article(title=title, date=date, text=text, url=url))
            else:
                self.session.query(Article).filter(Article.title == title).update(
                    {Article.date: date, Article.text: text, Article.url: url},
                    synchronize_session=False,
                )
            self.session.commit()
        if isinstance(item, BlogItem):
            article = item["article"]
            authors = item["authors"]
            tags = item["tags"]
            if not self.session.query(
                self.session.query(Article).filter(Article.title == article).exists()
            ).scalar():
                self.session.add(Article(title=article))
            art_id = (
                self.session.query(Article).filter(Article.title == article).one().id
            )
            for aut in authors:
                if not self.session.query(
                    self.session.query(Author).filter(Author.name == aut).exists()
                ).scalar():
                    self.session.add(Author(name=aut))
                aut_id = self.session.query(Author).filter(Author.name == aut).one().id
                if not self.session.query(
                    self.session.query(Authorship)
                    .filter(
                        and_(
                            Authorship.article_id == art_id,
                            Authorship.author_id == aut_id,
                        )
                    )
                    .exists()
                ).scalar():
                    self.session.add(Authorship(article_id=art_id, author_id=aut_id))
            for tag in tags:
                if not self.session.query(
                    self.session.query(Tag).filter(Tag.name == tag).exists()
                ).scalar():
                    self.session.add(Tag(name=tag))
                tag_id = self.session.query(Tag).filter(Tag.name == tag).one().id
                if not self.session.query(
                    self.session.query(Tagged)
                    .filter(and_(Tagged.article_id == art_id, Tagged.tag_id == tag_id))
                    .exists()
                ).scalar():
                    self.session.add(Tagged(article_id=art_id, tag_id=tag_id))
            self.session.commit()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
