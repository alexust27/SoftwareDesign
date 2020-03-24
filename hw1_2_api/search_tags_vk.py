#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys
import time

from vk.exceptions import VkException
from vk_api import vk_api

logger = logging.Logger(name="search_tags", level=logging.DEBUG)

SUCCESS = 0
API_BAD = 1
ARGS_BAD = 2


class SearchTagsVk:
    """
        Класс для подсчета постов по хэштегу в vk.com
    """

    def __init__(self, token, hash_tag, cnt_hours):
        """
            Конструктор
            :param token:       токен приложения из VK
            :type  token:       str
            :param hash_tag:    хэштег для поиска
            :type  hash_tag:    str
            :param cnt_hours:   количество часов для поиска
            :type  cnt_hours:   int
        """
        self.hours_for_search, self.hash_tag_text = cnt_hours, hash_tag
        self.vk_func = vk_api.VkApi(api_version='5.102', access_token=token)

    @staticmethod
    def parse_args(args) -> (int, str):
        """
            Парсер аргументов для поиска по хэштегу и часам
            :param   args: аргументы для парсера
            :type    args: list
            :rtype:  (int, str)
            :return: число часов и хэштег для поиска
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("search_text", help="название хэштега для поиска", type=str)
        parser.add_argument("hours", help="число часов, за которые необходимо построить диаграмму", type=int)
        ns = parser.parse_args(args)
        h = ns.hours
        t = "#" + ns.search_text
        if not 1 <= h <= 24:
            raise argparse.ArgumentError(None, "число часов должно быть от 1 до 24")
        if len(t) == 1:
            raise argparse.ArgumentError(None, "хэштег не должен быть пустым")
        return h, t

    def run(self) -> int:
        """
            Метод запуска поиска по хэштегу и часам
            :return: возвращает ARGS_BAD, если аргументы не верны,
                     SUCCESS если запрос обработан успешно,
                     API_BAD если проблема с запросом
            :rtype:  int
        """
        if not 1 <= self.hours_for_search <= 24:
            logger.error("число часов %s должно быть от 1 до 24", self.hours_for_search)
            return ARGS_BAD
        if len(self.hash_tag_text) <= 1:
            logger.error("хэштег не должен быть пустым")
            return ARGS_BAD
        try:
            result = self.vk_func.get_count_of_hashtag(self.hash_tag_text, self.hours_for_search)
        except VkException as vk_e:
            logger.error("Не удалось выполнить запрос: %s", vk_e)
            return API_BAD

        self.__print_statistic(result)
        return SUCCESS

    def __print_statistic(self, result):
        """
            Метод вывода полученного результата запроса
            :param result: словарь - время, количество записей за час до этого времени
            :type  result: dict
        """
        if not result:
            print("По хэштегу", self.hash_tag_text, "записей не найдено")
            return

        print("По хэштегу", self.hash_tag_text, "найдено записей:")
        for (end_time, cnt) in sorted(result.items()):
            start_time = end_time - vk_api.ONE_HOUR_IN_SECONDS
            print("с", time.strftime("%d %b %Y %H:%M", time.localtime(start_time)),
                  "по", time.strftime("%d %b %Y %H:%M", time.localtime(end_time)),
                  ":", cnt)


def main():
    hours, tag = SearchTagsVk.parse_args(sys.argv[1:])
    s = SearchTagsVk(token=os.getenv('ACCESS_TOKEN'), cnt_hours=hours, hash_tag=tag)
    s.run()


if __name__ == '__main__':
    main()
