import time
import vk
import logging

logger = logging.Logger(__name__, level=logging.INFO)

ONE_HOUR_IN_SECONDS = 3600


class VkApi:
    """
        Класс с функциями использующими API Вконтакте
    """

    def __init__(self, access_token, api_version):
        """
            :param access_token: токен приложения
            :type  access_token: str
            :param api_version:  версия api
            :type  api_version:  str
        """
        self.VK_API_VERSION = api_version
        session = vk.Session(access_token=access_token)
        self.vk_api = vk.API(session)

    def get_count_of_hashtag(self, hashtag_text, hours) -> dict:
        """
            Метод считает количество записей по хэштегу за указаное количество часов
            :param hashtag_text: хэштег для поиска
            :type hashtag_text:  str
            :param hours:        число часов за которое необходимо посчитать записи
            :type  hours:        int
            :return:             словарь, где ключ время, а значение количеством записей за час до этого времени,
                                 если количество записей 0, то возвращает пустой словарь
            :rtype:              dict
            :raise:              VkAPIError
        """
        current_time = int(time.time())
        res = {}
        for h in range(hours):
            end_time = current_time - h * ONE_HOUR_IN_SECONDS
            start_time = end_time - ONE_HOUR_IN_SECONDS
            news_feeds = self.vk_api.newsfeed.search(q=hashtag_text,
                                                     start_time=start_time,
                                                     end_time=end_time,
                                                     v=self.VK_API_VERSION)
            res[end_time] = news_feeds['total_count']
        if sum(res.values()) == 0:
            return {}
        return res
