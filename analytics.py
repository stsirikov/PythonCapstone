from pandas.core.frame import DataFrame
from matplotlib import pyplot as plt
from logging import info, basicConfig, INFO

basicConfig(
    encoding="utf-8", level=INFO, format="%(asctime)s %(levelname)s %(message)s"
)


def top_articles(articles: DataFrame):
    info("Most recent articles extracted.")
    return articles.sort_values("date", ascending=False).head(5)[["title", "date"]]


def top_authors(authorship: DataFrame, authors: DataFrame):
    info("Authors with the largest number of publications extracted.")
    return (
        authorship.groupby("author_id")
        .count()
        .rename(columns={"article_id": "article_count"})
        .sort_values("article_count", ascending=False)
        .head(5)
        .join(authors.set_index("id"), on="author_id")[["name", "article_count"]]
    )


def top_tags(tagged: DataFrame, tags: DataFrame):
    info("Most popular tags extracted.")
    return (
        tagged.groupby("tag_id")
        .count()
        .rename(columns={"article_id": "article_count"})
        .sort_values("article_count", ascending=False)
        .head(7)
        .join(tags.set_index("id"), on="tag_id")[["name", "article_count"]]
    )


def tags_plot(tags: DataFrame, filename: str):
    info("The plot of most popular tags built.")
    tags.plot.bar(x="name", y="article_count", fontsize=5)
    plt.savefig(filename)
