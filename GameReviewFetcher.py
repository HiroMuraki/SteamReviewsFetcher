from __future__ import annotations
from typing import List
from typing import Set
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from ElementExtractor import ElementExtractor
from GameReview import GameReview
from AsyncHelper import AsyncHelper
from ConsoleHelper import ConsoleHelper
import time
import threading


class GameReviewFetcher:
    class SharedData:
        def __init__(self):
            self.__game_reviews: Set[GameReview] = set()
            self.__stop_signal = False
            self.__stop_signal_lock = threading.Lock()
            self.__current_page_num = 1
            self.__current_page_num_lock = threading.Lock()
            self.__next_page_num = 1
            self.__next_page_num_lock = threading.Lock()

        @property
        def stop_signal(self) -> bool:
            with self.__stop_signal_lock:
                return self.__stop_signal

        def call_stop(self) -> None:
            with self.__stop_signal_lock:
                self.__stop_signal = True

        @property
        def game_reviews(self) -> Set[GameReview]:
            return self.__game_reviews

        @property
        def current_page_num(self) -> int:
            with self.__current_page_num_lock:
                return self.__current_page_num

        def inc_current_page_num(self) -> None:
            with self.__current_page_num_lock:
                self.__current_page_num += 1

        @property
        def next_page_num(self) -> int:
            with self.__next_page_num_lock:
                return self.__next_page_num

        def inc_next_page_num(self) -> None:
            with self.__next_page_num_lock:
                self.__next_page_num += 1

    def __init__(self, chrome_path: str, chrome_driver_path: str) -> None:
        chrome_options = Options()
        chrome_options.binary_location = chrome_path
        service = Service(chrome_driver_path)
        self.__driver = Chrome(service=service, options=chrome_options)
        self.__element_extractor = ElementExtractor(self.__driver)

    async def fetch(self, url: str, count: int) -> List[GameReview]:
        shared_data = GameReviewFetcher.SharedData()

        # Helper functions
        def wait_until(by: str, value: str, timeout: int) -> bool:
            try:
                WebDriverWait(self.__driver, timeout).until(expected_conditions.presence_of_element_located((by, value)))  # noqa
                return True
            except TimeoutException:
                return False

        def try_skip_content_warning_page() -> None:
            try:
                self.__driver.find_element(By.CLASS_NAME, "contentcheck_btns_ctn").find_elements(By.CLASS_NAME, "btn_blue_steamui.btn_medium")[0].click()  # noqa
                wait_until(By.ID, "NoMoreContent", 10)
            except NoSuchElementException:
                pass

        def load_next_page_worker() -> None:
            retry_times = 0
            retry_times_threshold = 10

            while True:
                if shared_data.stop_signal:
                    break

                if shared_data.next_page_num - shared_data.current_page_num > 5:
                    ConsoleHelper.write("Waiting: Fetching tasks")
                    time.sleep(1)
                    continue

                shared_data.inc_next_page_num()

                current_scroll_y = self.__driver.execute_script("return window.scrollY;")  # noqa
                self.__driver.execute_script(f"window.scrollBy(0, document.body.scrollHeight);")  # noqa
                new_scroll_y = self.__driver.execute_script("return window.scrollY;")  # noqa

                if int(current_scroll_y) == int(new_scroll_y):
                    ConsoleHelper.write_warning("No more pages")
                    return

                while True:
                    if wait_until(By.ID, f"page{shared_data.next_page_num}", 1):
                        retry_times = 0
                        break
                    else:
                        retry_times += 1
                        if retry_times > retry_times_threshold:
                            ConsoleHelper.write_warning("Network error detected")  # noqa
                            return

        def get_reviews_worker() -> None:
            def helper():
                retry_times = 0
                retry_times_threshold = 10

                while True:
                    ConsoleHelper.write(f"Fetching from page: {shared_data.current_page_num}")  # noqa

                    if wait_until(By.ID, f"page{shared_data.current_page_num}", 1):  # noqa
                        retry_times = 0
                    else:
                        retry_times += 1
                        if retry_times > retry_times_threshold:
                            ConsoleHelper.write_warning("[Warning] Not enough reviews or network error; fetching stopped")  # noqa
                            break
                        continue

                    page = self.__driver.find_element(By.ID, f"page{shared_data.current_page_num}")  # noqa
                    review_cards = page.find_elements(By.CLASS_NAME, "apphub_Card.modalContentLink.interactable")  # noqa

                    for card in review_cards:
                        game_review = GameReview(
                            author=self.__element_extractor.get_author(card),  # noqa
                            date_posted=self.__element_extractor.get_date_posted(card),  # noqa
                            played_hours=self.__element_extractor.get_played_hours(card),  # noqa
                            is_recommend=self.__element_extractor.get_is_recommend(card),  # noqa
                            helpful_count=self.__element_extractor.get_helpful_count(card),  # noqa
                            main_content=self.__element_extractor.get_main_content(card),  # noqa
                        )

                        shared_data.game_reviews.add(game_review)
                        if len(shared_data.game_reviews) >= count:
                            break

                    ConsoleHelper.write(f"Fetched: ({len(shared_data.game_reviews)} / {count})")  # noqa
                    if len(shared_data.game_reviews) >= count:
                        ConsoleHelper.write_success("Done")
                        break

                    shared_data.inc_current_page_num()

            try:
                helper()
            finally:
                shared_data.call_stop()

        # Function body starts here
        self.__driver.get(url)

        try_skip_content_warning_page()

        await AsyncHelper.run(load_next_page_worker, get_reviews_worker)  # noqa

        return list(shared_data.game_reviews)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__driver.quit()
        return False
