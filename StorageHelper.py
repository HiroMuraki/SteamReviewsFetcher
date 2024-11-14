from typing import List
from GameReview import GameReview
import csv
import os
import sqlite3
from ConsoleHelper import ConsoleHelper


class StorageHelper:
    @staticmethod
    def save_to_csv(game_reviews: List[GameReview], file_path: str) -> None:
        with open(file_path, mode='w+', encoding='utf8', newline='\n') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(GameReview.get_fields())  # noqa
            csv_writer.writerows([i.to_tuple() for i in game_reviews])

        ConsoleHelper.write_success(f"Saved to csv ({file_path})")

    @staticmethod
    def save_to_sqlite(game_reviews: List[GameReview], file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)

        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `game_review`
            (
                `id` INTEGER NOT NULL,
                `author` TEXT NOT NULL,
                `date_posted` TEXT NOT NULL,
                `played_hours` REAL NOT NULL,
                `helpful_count` INTEGER NOT NULL,
                `is_recommend` INTEGER NOT NULL,
                `main_content` TEXT NOT NULL,
                PRIMARY KEY(`id` AUTOINCREMENT)
            )
            """)

        cursor.executemany(
            f"""
            INSERT INTO `game_review` ({",".join([f"`{x}`" for x in GameReview.get_fields()])})
            VALUES (?, ?, ?, ?, ?, ?)""", [x.to_tuple() for x in game_reviews])

        conn.commit()
        conn.close()

        ConsoleHelper.write_success(f"Saved to sqlite ({file_path})")
