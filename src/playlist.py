import datetime
import os
import typing

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    """
    Класс для получения данных плэйлиста из ютуб-канала
    """

    api_key: str | None = os.getenv("API_KEY")

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @classmethod
    def get_service(cls) -> typing.Any:
        """Возвращает объект для работы с API."""
        return build("youtube", "v3", developerKey=cls.api_key)

    def get_video_ids(self) -> list[str]:
        """Возвращает список video-ids по id плэйлиста для дальнейшей работы"""
        playlist_videos = (
            self.get_service()
            .playlistItems()
            .list(playlistId=self.playlist_id, part="contentDetails", maxResults=50)
            .execute()
        )
        return [video["contentDetails"]["videoId"] for video in playlist_videos["items"]]

    def get_playlist_title(self) -> typing.Any:
        """Возвращает title плэйлиста для инициализации"""
        pl_info = self.get_service().playlists().list(id=self.playlist_id, part="snippet").execute()
        title = pl_info["items"][0]["snippet"]["title"]
        return title

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает длительность всех видео плэйлиста в формате timedelta"""
        video_response = (
            self.get_service()
            .videos()
            .list(part="contentDetails,statistics", id=",".join(self.get_video_ids()))
            .execute()
        )
        td_list = []
        for video in video_response["items"]:
            iso_8601_duration = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_8601_duration)
            td_list.append(duration)
        td_sum = datetime.timedelta(seconds=sum(td.total_seconds() for td in td_list))
        return td_sum

    def show_best_video(self) -> typing.Any:
        """Возвращает ссылку на видео плэйлиста набравшее больше всего лайков"""
        video_ids = self.get_video_ids()
        list_with_video_info = []
        for video_id in video_ids:
            video_info_dict = {}
            video_obj = Video(video_id)  # инициализация через класс Video
            video_info_dict["likes"] = video_obj.like_count
            video_info_dict["url"] = video_obj.video_url
            list_with_video_info.append(video_info_dict)
        sorted_list = sorted(list_with_video_info, key=lambda x: x["likes"], reverse=True)
        return sorted_list[0]["url"]

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"
