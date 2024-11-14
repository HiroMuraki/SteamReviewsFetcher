from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re


class ElementExtractor:
    HELPFUL_COUNT_RE = re.compile(r"(?<=有 )\d+(?= 人觉得这篇评测有价值)")
    PLAYED_HOURS_RE = re.compile(r"(?<=总时数 )[\d.]+(?= 小时)")
    IS_RECOMMEND_MAP = {"推荐": True, "不推荐": False}
    CURRENT_YEAR = datetime.now().year

    def __init__(self, driver: Chrome) -> None:
        self.__driver = driver

    def get_author(self, element: WebElement) -> str:
        """
        此评测的发布者
        """
        author_element = element.find_element(By.CLASS_NAME, "apphub_CardContentAuthorName")  # noqa
        author_name = self.__driver.execute_script("return arguments[0].childNodes[1]", author_element)  # noqa

        return author_name.text

    def get_date_posted(self, element: WebElement) -> str:
        """
        此评测的发布日期
        """
        main_content_element = element.find_element(By.CLASS_NAME, "apphub_CardTextContent")  # noqa
        date_posted = main_content_element.find_element(By.CLASS_NAME, "date_posted").text.replace(" ", "").split("：")[1]  # noqa

        if "年" not in date_posted:
            date_posted = f"{ElementExtractor.CURRENT_YEAR}年{date_posted}"
        return date_posted

    def get_helpful_count(self, element: WebElement) -> int:
        """
        觉得此评测有帮助的人数
        """
        found_helpful_element = element.find_element(By.CLASS_NAME, "found_helpful")  # noqa

        if found_helpful_element.text.startswith("尚未有人觉得这篇评测有价值"):
            return 0
        if found_helpful_element.text.startswith("1 人觉得这篇评测有价值"):
            return 1

        found_helpful_count = ElementExtractor.HELPFUL_COUNT_RE.findall(found_helpful_element.text.replace(",", ""))[0]  # noqa
        return int(found_helpful_count)

    def get_is_recommend(self, element: WebElement) -> bool:
        """
        该用户是否推荐该游戏
        """
        is_recommend_element = element.find_element(By.CLASS_NAME, "title")

        return ElementExtractor.IS_RECOMMEND_MAP[is_recommend_element.text]

    def get_played_hours(self, element: WebElement) -> float:
        """
        游玩时长
        """
        played_hours_element = element.find_element(By.CLASS_NAME, "hours")
        played_hours = ElementExtractor.PLAYED_HOURS_RE.findall(played_hours_element.text.replace(",", ""))[0]  # noqa

        return float(played_hours)

    def get_main_content(self, element: WebElement) -> str:
        """
        评测内容
        """
        main_content_element = element.find_element(By.CLASS_NAME, "apphub_CardTextContent")  # noqa
        self.__driver.execute_script(f"""
            const childNodesToRemove = arguments[0].querySelectorAll(".date_posted, .received_compensation");
            childNodesToRemove.forEach(c => c.remove());
            """, main_content_element)

        return main_content_element.text.strip()
