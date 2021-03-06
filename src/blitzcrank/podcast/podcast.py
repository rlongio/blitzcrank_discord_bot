import datetime
import logging
import re
import typing

from sqlalchemy import Column, DateTime, String

logger: logging.Logger = logging.getLogger(__name__)

from blitzcrank.database.database import BASE, ENGINE, SESSION


class Podcast(BASE):
    """Represents podcast data """

    __tablename__ = "podcast"

    id = Column(String, primary_key=True)
    description = Column(String)
    url = Column(String)
    title = Column(String)
    image = Column(String)
    type = Column(String)
    created_at = Column("created_at", DateTime, nullable=False)

    def __repr__(self) -> str:
        return str(self.__dict__.items())

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} '{self.id}' {self.title}>"

    @staticmethod
    def from_result(results) -> typing.Union["Podcast", None]:
        """Extracts the data from the first result and returns
        as a dict

        Args:
            results (FeedParserDict): parsed results

        Returns:
            dict: select key/value pairs
        """
        IMAGE_URL_PATTERN = r"(src=\")(\S*)(\")"

        if "entries" not in results or len(results["entries"]) < 1:
            return None

        return Podcast(
            id=results["entries"][0]["id"],
            description=results["entries"][0]["subtitle"],
            url=results["entries"][0]["link"],
            title=f"{results['entries'][0]['itunes_title']} ({results['entries'][0]['itunes_episode']})",
            image=re.search(IMAGE_URL_PATTERN, results["entries"][0]["summary"]).group(
                2
            ),
            type="rich",
            created_at=datetime.datetime.utcnow(),
        )
