import os
import typing

from googleapiclient.discovery import build


class Video:
    """Класс для видео из ютуб-канала"""

    api_key: str | None = os.getenv("API_KEY")

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = self.initialize_from_data()["video_title"]
        self.video_url = self.initialize_from_data()["video_url"]
        self.view_count = self.initialize_from_data()["view_count"]
        self.like_count = self.initialize_from_data()["like_count"]

    @classmethod
    def get_service(cls) -> typing.Any:
        """Возвращает объект для работы с API."""
        return build("youtube", "v3", developerKey=cls.api_key)

    def initialize_from_data(self) -> dict:
        """Инициализация данных канала."""
        youtube = self.get_service()
        try:
            video_response = (
                youtube.videos()
                .list(part="snippet,statistics,contentDetails,topicDetails", id=self.video_id)
                .execute()
            )
            title: str = video_response["items"][0]["snippet"]["title"]
            video_url: str = "https://youtu.be/" + self.video_id
            view_count: int = video_response["items"][0]["statistics"]["viewCount"]
            like_count: int = video_response["items"][0]["statistics"]["likeCount"]
            return {
                "video_title": title,
                "view_count": view_count,
                "like_count": like_count,
                "video_url": video_url,
            }
        except IndexError:
            return {
                "video_title": None,
                "view_count": None,
                "like_count": None,
                "video_url": None,
            }

    def __str__(self) -> typing.Any:
        return self.title


class PLVideo(Video):
    """Класс для видео по плейлисту из ютуб-канала"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
