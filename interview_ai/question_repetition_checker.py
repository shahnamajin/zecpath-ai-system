"""Prevent repetitive follow-up questions."""

import re


class QuestionRepetitionChecker:
    def normalize(self, question: str) -> str:
        text = (question or "").lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def is_repeated(self, question: str, history: list[str]) -> bool:
        normalized = self.normalize(question)
        return any(normalized == self.normalize(old) for old in (history or []))

    def filter_new(self, questions: list[str], history: list[str]) -> list[str]:
        return [q for q in questions if not self.is_repeated(q, history)]
