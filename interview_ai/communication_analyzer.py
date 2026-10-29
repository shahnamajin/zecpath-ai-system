"""Communication skill feature extraction for ZECPath AI."""

import re
from collections import Counter


class CommunicationAnalyzer:
    """Extract transparent communication signals from a text response."""

    FILLERS = {
        "um", "uh", "erm", "hmm", "mmm", "like", "actually",
        "basically", "you know", "sort of", "kind of"
    }

    STRUCTURE_MARKERS = {
        "first", "second", "third", "then", "finally", "because",
        "therefore", "for example", "however", "in conclusion",
        "overall", "my role", "the result", "as a result"
    }

    def tokenize_words(self, text: str) -> list[str]:
        return re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", (text or "").lower())

    def sentences(self, text: str) -> list[str]:
        return [s.strip() for s in re.split(r"[.!?]+", text or "") if s.strip()]

    def detect_fillers(self, text: str) -> dict:
        lowered = (text or "").lower()
        tokens = self.tokenize_words(lowered)
        count = 0
        found = []

        # Multi-word fillers
        for phrase in ("you know", "sort of", "kind of"):
            matches = re.findall(r"\b" + re.escape(phrase) + r"\b", lowered)
            if matches:
                count += len(matches)
                found.extend([phrase] * len(matches))

        # Single-word fillers
        single_tokens = set(self.FILLERS) - {"you know", "sort of", "kind of"}
        for token in tokens:
            if token in single_tokens:
                count += 1
                found.append(token)

        word_count = len(tokens)
        rate = (count / word_count * 100) if word_count else 0.0
        return {
            "count": count,
            "rate_per_100_words": round(rate, 2),
            "words": found,
        }

    def fluency_score(self, text: str) -> float:
        sents = self.sentences(text)
        words = self.tokenize_words(text)
        if not words:
            return 0.0
        if not sents:
            return 0.0
        avg_len = len(words) / len(sents)
        # Moderate sentence length receives the highest score.
        if 8 <= avg_len <= 22:
            base = 90
        elif 5 <= avg_len < 8 or 22 < avg_len <= 30:
            base = 78
        elif 3 <= avg_len < 5 or 30 < avg_len <= 38:
            base = 65
        else:
            base = 50
        filler_penalty = min(self.detect_fillers(text)["rate_per_100_words"] * 2, 25)
        return round(max(0, min(100, base - filler_penalty)), 2)

    def grammar_score(self, text: str) -> float:
        sents = self.sentences(text)
        words = self.tokenize_words(text)
        if not words:
            return 0.0

        issues = 0
        for sentence in sents:
            sw = self.tokenize_words(sentence)
            if len(sw) >= 4:
                if sentence[0].islower():
                    issues += 1
                if len(sw) >= 4 and len(set(sw)) == 1:
                    issues += 1

        # Common informal fragments / obvious patterns, kept deliberately conservative.
        lowered = (text or "").lower()
        issues += len(re.findall(r"\b(i are|he are|she are|they is|we is)\b", lowered))
        issues += len(re.findall(r"\b(a experience|an project)\b", lowered))

        sentence_count = max(1, len(sents))
        issue_rate = issues / sentence_count
        score = 92 - min(issue_rate * 25, 45)
        if len(words) < 8:
            score -= 8
        return round(max(0, min(100, score)), 2)

    def vocabulary_score(self, text: str) -> float:
        words = self.tokenize_words(text)
        if not words:
            return 0.0
        unique = len(set(words))
        ttr = unique / len(words)

        # Length-normalized range estimate to reduce the advantage/disadvantage
        # caused by very short or very long answers.
        if len(words) < 8:
            return round(max(0, min(100, 55 + (ttr - 0.5) * 60)), 2)

        score = 45 + min(ttr * 55, 55)
        return round(max(0, min(100, score)), 2)

    def clarity_score(self, text: str) -> float:
        words = self.tokenize_words(text)
        sents = self.sentences(text)
        if not words:
            return 0.0
        avg_len = len(words) / max(1, len(sents))
        if 7 <= avg_len <= 24:
            score = 90
        elif 5 <= avg_len < 7 or 24 < avg_len <= 32:
            score = 78
        else:
            score = 62

        filler_rate = self.detect_fillers(text)["rate_per_100_words"]
        score -= min(filler_rate * 1.5, 20)
        return round(max(0, min(100, score)), 2)

    def structure_score(self, text: str) -> float:
        words = self.tokenize_words(text)
        if not words:
            return 0.0

        lowered = (text or "").lower()
        marker_count = sum(
            1 for marker in self.STRUCTURE_MARKERS
            if re.search(r"\b" + re.escape(marker) + r"\b", lowered)
        )
        sentence_count = len(self.sentences(text))

        if sentence_count >= 3 and marker_count >= 1:
            score = 92
        elif sentence_count >= 3:
            score = 82
        elif sentence_count == 2:
            score = 72
        else:
            score = 55

        if marker_count >= 2:
            score += 4
        return round(min(100, score), 2)

    def filler_control_score(self, text: str) -> float:
        rate = self.detect_fillers(text)["rate_per_100_words"]
        if rate == 0:
            return 100.0
        if rate <= 2:
            return 90.0
        if rate <= 5:
            return 75.0
        if rate <= 10:
            return 55.0
        return 35.0

    def analyze(self, text: str) -> dict:
        words = self.tokenize_words(text)
        sents = self.sentences(text)
        fillers = self.detect_fillers(text)
        return {
            "word_count": len(words),
            "sentence_count": len(sents),
            "fluency": self.fluency_score(text),
            "grammar_quality": self.grammar_score(text),
            "vocabulary_range": self.vocabulary_score(text),
            "clarity": self.clarity_score(text),
            "answer_structure": self.structure_score(text),
            "filler_control": self.filler_control_score(text),
            "filler_details": fillers,
        }
