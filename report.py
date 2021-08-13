from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import max
from subprocess import run
from pandas import read_sql_table

from analytics import top_articles, top_authors, top_tags, tags_plot
from blog.blog.database import engine, Article


def main():
    """Entry point for the program, crawls data and builds a report."""
    Session = sessionmaker(bind=engine)
    s = Session()
    last_date = s.query(max(Article.date)).first()[0]
    s.close()
    if (last_date is not None):
        run(f"cd blog; scrapy crawl blog -a last_date={last_date}", shell=True)
    else:
        run(f"cd blog; scrapy crawl blog", shell=True)
    cnx = engine.connect()
    author = read_sql_table("author", cnx)
    article = read_sql_table("article", cnx, parse_dates=["date"])
    authorship = read_sql_table("authorship", cnx)
    tag = read_sql_table("tag", cnx)
    tagged = read_sql_table("tagged", cnx)
    cnx.close()

    print(top_articles(article))
    print(top_authors(authorship, author))
    tags = top_tags(tagged, tag)
    print(tags)
    tags_plot(tags, "report.png")


if __name__ == "__main__":
        main()
