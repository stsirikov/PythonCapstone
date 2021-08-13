from datetime import datetime
from sqlalchemy.orm import sessionmaker
from os import path, remove
import unittest as ut
import pandas as pd

from blog.blog.database import engine, Article
from analytics import top_articles, top_authors, tags_plot


class TestBD(ut.TestCase):
    def setUp(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_insert_article(self):
        self.session.add(Article(title="fake"))
        self.assertTrue(
            self.session.query(
                self.session.query(Article).filter(Article.title == "fake").exists()
            ).scalar()
        )
        self.session.query(Article).filter(Article.title == "fake").delete()


class TestAnalytics(ut.TestCase):
    def test_analyse_articles(self):
        dates = map(
            lambda x: datetime.strptime(x, "%b %d %Y"),
            (f"Jan {i} 1980" for i in range(1, 7)),
        )
        articles = pd.DataFrame.from_dict({"date": dates, "title": map(lambda x: str(x), range(1, 7))})
        res = top_articles(articles)
        self.assertTrue(res["title"].size == 5)
        self.assertTrue(res["title"].apply(lambda x: x != "1").all())

    def test_analyse_authors(self):
        authors = pd.DataFrame.from_dict({"id": range(1, 7), "name": map(lambda x: str(x), range(1, 7))})
        authorship = pd.DataFrame.from_dict(
            {"author_id": [1] + (list(range(2, 7)) * 2), "article_id": range(1, 12)}
        )
        res = top_authors(authorship, authors)
        self.assertTrue(res["article_count"].size == 5)
        self.assertTrue(res["article_count"].apply(lambda x: x == 2).all())

    def test_plot(self):
        tags = pd.DataFrame.from_dict(
            {"name": ["a", "b", "c"], "article_count": [1, 2, 3]}
        )
        tags_plot(tags, "test.png")
        self.assertTrue(path.exists("test.png"))
        remove("test.png")


if __name__ == "__main__":
    ut.main()
