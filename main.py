from __future__ import annotations
from StorageHelper import StorageHelper
from GameReviewFetcher import GameReviewFetcher
import asyncio
import time
import os

# 设置要爬取的游戏，元素1是游戏名，元素2是游戏的AppID
GAMES = [
    ("CS2", 730),
    ("求生之路2", 550),
    # ("黑神话悟空", 2358720),
    # ("怪物猎人世界", 582010),
    # ("女神异闻录3R", 2161700),
    # ("最后生还者1", 1888930)
]

# 游戏评论URL模板，此处为“简体中文 + 最有价值（发布至今）”
GAME_REVIEWS_URL_TEMPLATE = "https://steamcommunity.com/app/{0}/reviews/?filterLanguage=schinese&browsefilter=toprated"

# Chrome路径
CHROME_PATH = "Chrome\\chrome-win64\\chrome.exe"

# Chrome Driver路径
CHROME_DRIVER_PATH = "Chrome\\chromedriver-win64\\chromedriver.exe"

# 爬取结果保存路径的根目录
SAVE_TO_ROOT = "data"

# 爬取结果保存路径的模板
SAVE_TO_TEMPLATE = f"{SAVE_TO_ROOT}\\{{0}}"

# 每个游戏需要爬取的评论数量
DESIRED_COUNT = 50


def init():
    if not os.path.exists(SAVE_TO_ROOT):
        os.makedirs(SAVE_TO_ROOT)

    if not os.path.exists(CHROME_PATH):
        print(f"[Error] CHROME_PATH ({CHROME_PATH}) not found")

    if not os.path.exists(CHROME_DRIVER_PATH):
        print(f"[Error] CHROME_DRIVER_PATH ({CHROME_DRIVER_PATH}) not found")


def wait(task_name: str, timeout: int) -> None:
    for remaining in range(timeout, 0, -1):
        print(f"Task '{task_name}' will start in {remaining} second(s)")  # noqa
        time.sleep(1)  # Wait for 1 second


async def main():
    init()

    for game_name, game_appid in GAMES:
        wait(f"Fetching reviews for {game_name}", 3)

        with GameReviewFetcher(CHROME_PATH, CHROME_DRIVER_PATH) as fetcher:
            game_reviews = await fetcher.fetch(GAME_REVIEWS_URL_TEMPLATE.format(game_appid), DESIRED_COUNT)  # noqa
            StorageHelper.save_to_csv(game_reviews, SAVE_TO_TEMPLATE.format(f"{game_name} - {game_appid}.csv"))  # noqa
            StorageHelper.save_to_sqlite(game_reviews, SAVE_TO_TEMPLATE.format(f"{game_name} - {game_appid}.db"))  # noqa

asyncio.run(main())
