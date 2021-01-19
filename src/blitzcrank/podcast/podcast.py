import datetime
import logging
import re

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()


class Podcast(Base):
    """Represents podcast data """

    __tablename__ = "podcast"

    id = Column(String, primary_key=True)
    description = Column(String)
    url = Column(String)
    title = Column(String)
    image = Column(String)
    type = Column(String)
    created_at = Column("created_at", DateTime, nullable=False)

    @staticmethod
    def _from_results(results):
        IMAGE_URL_PATTERN = r"(src=\")(\S*)(\")"

        return {
            "id": results["entries"][0]["id"],
            "description": results["entries"][0]["subtitle"],
            "url": results["entries"][0]["link"],
            "title": f"{results['entries'][0]['itunes_title']} ({results['entries'][0]['itunes_episode']})",
            "image": re.search(
                IMAGE_URL_PATTERN, results["entries"][0]["summary"]
            ).group(2),
            "type": "rich",
            "created_at": datetime.datetime.utcnow(),
        }