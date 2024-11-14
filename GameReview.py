from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameReview:
    author: str
    date_posted: str
    played_hours: float
    helpful_count: int
    is_recommend: bool
    main_content: str

    @staticmethod
    def get_fields() -> Tuple[str, str, str, str, str, str]:
        return ("author", "date_posted", "played_hours",
                "helpful_count", "is_recommend", "main_content")

    def to_tuple(self) -> tuple[str, str, float, int, bool, str]:
        return (self.author,
                self.date_posted,
                self.played_hours,
                self.helpful_count,
                self.is_recommend,
                self.main_content,)

    def __hash__(self) -> int:
        return (hash(self.author)
                ^ hash(self.date_posted)
                ^ hash(self.played_hours)
                ^ hash(self.helpful_count)
                ^ hash(self.is_recommend))
