#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from thespian.actors import ActorSystem, ActorExitRequest

from MasterActor import MasterActor


def main():
    asys = ActorSystem()
    try:
        while True:
            print("Type what you want to search:")
            query = input()
            master = asys.createActor(MasterActor, globalName="master")
            res = asys.ask(master, query, timeout=timedelta(seconds=5))
            print(res)
            asys.tell(master, ActorExitRequest())
    finally:
        asys.shutdown()


if __name__ == '__main__':
    main()
