import time

SEARCHERS = ["Google", "Yandex", "Bing"]


class SearchRequest:

    def __init__(self, search_system: str, query: str):
        self.__search_system = search_system
        self.__query = query

    def get_search_system(self) -> str:
        return self.__search_system

    def get_query(self) -> str:
        return self.__query


class DummySearchClient:
    delay_for_dummy_search = 0.3

    def search_for(self, request: SearchRequest) -> dict:
        result = []
        for i in range(5):
            result.append({
                f"http://res_of_searh/{request.get_query()}/{i}",
                f"Answer for {request.get_query()} #{i}"
            })
        time.sleep(self.delay_for_dummy_search)
        return {request.get_search_system(): result}
