from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from typing import Iterable
from GameReview import GameReview
from ConsoleHelper import ConsoleHelper
from datetime import datetime


class GameReviewFetcher:
    def __init__(self, chrome_bin_path: str, chrome_driver_path) -> None:
        self.__chrome_bin_path = chrome_bin_path
        self.__chrome_driver_path = chrome_driver_path

    def fetch(self, app_id: int) -> Iterable[GameReview]:
        chrome_options = Options()
        chrome_options.binary_location = self.__chrome_bin_path
        service = Service(executable_path=self.__chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        with open("js/FetchGameReviews.js", "r", encoding="utf8") as fp:
            fetch_game_reviews_js_script = GameReviewFetcher.__wrap_async_js_script(fp.read())

        try:
            driver.get(
                f"https://steamcommunity.com/app/{app_id}/reviews?browsefilter=toprated&filterLanguage=schinese")
            total = 0
            page = 1
            while True:
                items = driver.execute_async_script(fetch_game_reviews_js_script, page)
                if len(items) == 0:
                    ConsoleHelper.write_warning("未获取到新数据，已终止")
                    break
                total+=len(items)
                ConsoleHelper.write_success(f"[{datetime.now().strftime("%H:%M:%S")}] <{app_id}> 新获取了{len(items)}条评论(总计{total}条) ")
                for item in items:
                    yield GameReview(
                        author=item["author"],
                        date_posted=item["datePosted"],
                        played_hours=item["playedHours"],
                        helpful_count=item["helpfulCount"],
                        is_recommend=item["isRecommend"],
                        main_content=item["mainContent"]
                    )
                page += 1
        except Exception as e:
            print(f"ERROR: {e.args}")
        finally:
            driver.quit()

    @staticmethod
    def __wrap_async_js_script(js_script: str) -> str:
        return f"""
                const callback = arguments[arguments.length - 1];

                const result = (async () => {{
                    {js_script}
                }})();

                callback(result);
                """
