from GameReviewFetcher import GameReviewFetcher
from GameReview import GameReview
from StorageHelper import StorageHelper
from ConsoleHelper import ConsoleHelper

CHROME_BIN_PATH = R"Chrome-For-Testing\chrome.exe"
CHROME_DRIVER_PATH = R"ChromeDriver\chromedriver.exe"


def main():
    fetcher = GameReviewFetcher(CHROME_BIN_PATH, CHROME_DRIVER_PATH)
    game_reviews = set()
    for item in fetcher.fetch(550):
        game_reviews.add(item)
        if len(game_reviews) >= 1000:
            break
    ConsoleHelper.write_success(f"获取了{len(game_reviews)}条评论")
    StorageHelper.save_to_csv(game_reviews, "data/test.csv")
    StorageHelper.save_to_sqlite(game_reviews, "data/test.db")
    ConsoleHelper.write_success(f"数据已保存")


if __name__ == "__main__":
    main()
