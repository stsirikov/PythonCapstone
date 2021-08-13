from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:////tmp/blog.db", echo=True)
Model = declarative_base()


class Article(Model):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    text = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f"<Article # {self.id}>"


class Author(Model):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    job = Column(String)
    linkedin = Column(String)

    def __repr__(self):
        return f"<Author # {self.id}>"


class Authorship(Model):
    __tablename__ = "authorship"

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"<Article # {self.article_id} by Author # {self.author_id}>"


class Tag(Model):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Tag # {self.id}>"


class Tagged(Model):
    __tablename__ = "tagged"

    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"<Article # {self.article_id} with Tag # {self.tag_id}>"


if __name__ == "__main__":
    Model.metadata.create_all(engine)
