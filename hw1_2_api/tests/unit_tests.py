import os
import time
from unittest import TestCase
from unittest.mock import patch

import search_tags_vk as search
from argparse import ArgumentError

from vk_api.vk_api import ONE_HOUR_IN_SECONDS

GOOD_TOKEN = os.getenv('ACCESS_TOKEN')


class TestArgParser(TestCase):

    def test_parser_ok1(self):
        try:
            hours, text = search.SearchTagsVk.parse_args(["зенит", "1"])
        except ArgumentError as ae:
            self.fail(ae)

        self.assertEqual(hours, 1)
        self.assertEqual(text, "#зенит")

    def test_parser_ok2(self):
        try:
            hours, text = search.SearchTagsVk.parse_args(["з", "24"])
        except ArgumentError as ae:
            self.fail(ae)

        self.assertEqual(hours, 24)
        self.assertEqual(text, "#з")

    def test_parser_fail1(self):
        try:
            search.SearchTagsVk.parse_args(["", "1"])
        except ArgumentError as ae:
            self.assertEqual(ae.args[1], "хэштег не должен быть пустым")

    def test_parser_fail2(self):
        try:
            search.SearchTagsVk.parse_args(["зенит", "0"])
        except ArgumentError as ae:
            self.assertEqual(ae.args[1], "число часов должно быть от 1 до 24")


class TestSearchTagsVk(TestCase):
    def setUp(self):
        self.cur_time = time.time()

    def test_bad_args1(self):
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=0, hash_tag="#зенит")
        self.assertEqual(s.run(), search.ARGS_BAD)

    def test_bad_args2(self):
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=1, hash_tag="#")
        self.assertEqual(s.run(), search.ARGS_BAD)

    def test_bad_token(self):
        s = search.SearchTagsVk(token="bad_token", cnt_hours=1, hash_tag="#зенит")
        self.assertEqual(s.run(), search.API_BAD)

    @patch("vk_api.vk_api.VkApi.get_count_of_hashtag")
    def test_search_ok(self, mock_get_count):
        mock_get_count.return_value = {time.time(): 1}
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=1, hash_tag="#зенит")
        self.assertEqual(s.run(), search.SUCCESS)

    @patch("vk_api.vk_api.VkApi.get_count_of_hashtag")
    def test_search_ok2(self, mock_get_count):
        mock_get_count.return_value = {self.cur_time - ONE_HOUR_IN_SECONDS: 1,
                                       self.cur_time: 11}
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=1, hash_tag="#зенит")
        self.assertEqual(s.run(), search.SUCCESS)

    @patch("vk_api.vk_api.VkApi.get_count_of_hashtag")
    def test_search_max(self, mock_get_count):
        ret_val = {}
        for h in range(24):
            ret_val[self.cur_time - h * ONE_HOUR_IN_SECONDS] = h
        mock_get_count.return_value = ret_val
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=24, hash_tag="#зенит")
        self.assertEqual(s.run(), search.SUCCESS)

    @patch("vk_api.vk_api.VkApi.get_count_of_hashtag")
    def test_search_empty(self, mock_get_count):
        mock_get_count.return_value = {self.cur_time - ONE_HOUR_IN_SECONDS: 0,
                                       self.cur_time: 0}
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=1, hash_tag="#зенит")
        self.assertEqual(s.run(), search.SUCCESS)

    @patch("vk_api.vk_api.VkApi.get_count_of_hashtag")
    def test_search_empty2(self, mock_get_count):
        mock_get_count.return_value = {}
        s = search.SearchTagsVk(token=GOOD_TOKEN, cnt_hours=1, hash_tag="#зенит")
        self.assertEqual(s.run(), search.SUCCESS)
