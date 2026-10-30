"""Bounded difficulty progression based on explicit answer evaluation evidence."""


class TechnicalDifficultyController:
    LEVELS = ["easy", "medium", "hard", "expert"]

    def __init__(self, baseline="easy", maximum="expert", minimum="easy"):
        if baseline not in self.LEVELS or maximum not in self.LEVELS or minimum not in self.LEVELS:
            raise ValueError("Difficulty must be one of: easy, medium, hard, expert")
        self.minimum = self.LEVELS.index(minimum)
        self.maximum = self.LEVELS.index(maximum)
        self.current = self.LEVELS.index(baseline)
        if not self.minimum <= self.current <= self.maximum:
            raise ValueError("Baseline difficulty must be within configured bounds")

    @property
    def difficulty(self):
        return self.LEVELS[self.current]

    def update(self, evaluation_status, performance=None):
        """Accept evaluator evidence: strong, partial, weak, or insufficient."""
        if evaluation_status == "strong":
            self.current = min(self.current + 1, self.maximum)
        elif evaluation_status == "weak":
            self.current = max(self.current - 1, self.minimum)
        elif evaluation_status in {"partial", "insufficient"}:
            pass
        else:
            raise ValueError("evaluation_status must be strong, partial, weak, or insufficient")
        return self.difficulty
