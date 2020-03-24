#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from unittest import TestCase

from thespian.actors import ActorSystem

from ChildActor import ChildActor
from MasterActor import MasterActor
from SearchUtils import SearchRequest, SEARCHERS, DummySearchClient


class TestActors(TestCase):
    def setUp(self) -> None:
        self.asys = ActorSystem()

    def tearDown(self) -> None:
        self.asys.shutdown()

    def test_child_actor(self):
        searcher = SEARCHERS[0]
        child_ac = self.asys.createActor(ChildActor)
        result: dict = self.asys.ask(child_ac, SearchRequest(searcher, "some text for find"))

        self.assertIn(searcher, result.keys())
        self.assertIsNotNone(result[searcher])
        self.assertTrue(len(result[searcher]) > 0)

    def test_master_actor1(self):
        master = self.asys.createActor(MasterActor)

        self.asys.tell(master, timedelta(milliseconds=500))
        DummySearchClient.delay_for_dummy_search = 0.1
        result = self.asys.ask(master, "some text for find")
        s1 = list(SEARCHERS)
        s2 = list(result.keys())
        s1.sort()
        s2.sort()
        self.assertListEqual(s1, s2)
        for s in SEARCHERS:
            self.assertNotEqual(result[s], [])

    def test_master_actor2(self):
        master = self.asys.createActor(MasterActor)

        self.asys.tell(master, timedelta(milliseconds=10))
        DummySearchClient.delay_for_dummy_search = 1
        result = self.asys.ask(master, "some text for find")
        s1 = list(SEARCHERS)
        s2 = list(result.keys())
        s1.sort()
        s2.sort()
        self.assertListEqual(s1, s2)
        for s in SEARCHERS:
            self.assertEqual(result[s], [])
