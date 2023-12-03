import json
import os
import typing

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str | None = os.getenv("API_KEY")

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id
        self.title: str = self.initialize_from_dict()["title"]
        self.description: str = self.initialize_from_dict()["description"]
        self.url: str = self.initialize_from_dict()["url"]
        self.followers: int = int(self.initialize_from_dict()["followers"])
        self.video_count: int = int(self.initialize_from_dict()["video_count"])
        self.views: int = int(self.initialize_from_dict()["views"])

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        dict_to_print = youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        return print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> typing.Any:
        """Возвращает объект для работы с API."""
        return build("youtube", "v3", developerKey=cls.api_key)

    def initialize_from_dict(self) -> dict:
        """Инициализация данных канала."""
        youtube = self.get_service()
        dict_ = youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        title = dict_["items"][0]["snippet"]["title"]
        description = dict_["items"][0]["snippet"]["description"]
        url = "https://www.youtube.com/channel/" + dict_["items"][0]["id"]
        followers = dict_["items"][0]["statistics"]["subscriberCount"]
        video_count = dict_["items"][0]["statistics"]["videoCount"]
        views = dict_["items"][0]["statistics"]["viewCount"]
        return {
            "title": title,
            "description": description,
            "url": url,
            "followers": followers,
            "video_count": video_count,
            "views": views,
        }

    def info_dict(self) -> dict:
        """Возвращает словарь с информацией о канале."""
        return {
            "id канала": self.__channel_id,
            "Название канала": self.title,
            "Описание канала": self.description,
            "Ссылка на канал": self.url,
            "Количество подписчиков": self.followers,
            "Количество видео": self.video_count,
            "Общее количество просмотров": self.views,
        }

    def to_json(self, file_name: str) -> None:
        """Сохранить данные в файл."""
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(self.info_dict(), f, indent=2, ensure_ascii=False)

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        return self.followers + other.followers

    def __sub__(self, other) -> int:
        return self.followers - other.followers

    def __gt__(self, other) -> bool:
        return self.followers > other.followers

    def __ge__(self, other) -> bool:
        return self.followers >= other.followers

    def __lt__(self, other) -> bool:
        return self.followers < other.followers

    def __le__(self, other) -> bool:
        return self.followers <= other.followers

    def __eq__(self, other) -> bool:
        return self.followers == other.followers
