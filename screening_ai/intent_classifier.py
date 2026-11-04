
import re


class IntentClassifier:
    """
    Rule-based intent classifier for Zecpath HR screening.

    Features:
    - Context-aware classification
    - Keyword-based intent scoring
    - Multiple keyword detection
    - Deterministic tie-breaking
    - Missing and vague answer detection
    - Short-answer fallback
    """

    INTENTS = {
        "introduction",
        "education",
        "experience",
        "skills",
        "availability",
        "salary_expectation",
        "location",
        "off_topic",
        "vague",
        "missing",
    }

    KEYWORDS = {
        "introduction": [
            "my name",
            "i am",
            "i'm",
            "myself",
            "introduce",
            "background",
        ],

        "education": [
            "degree",
            "bachelor",
            "master",
            "mca",
            "bca",
            "b.tech",
            "m.tech",
            "education",
            "university",
            "college",
            "graduate",
            "graduated",
        ],

        "experience": [
            "experience",
            "worked",
            "work",
            "internship",
            "intern",
            "project",
            "developed",
            "built",
            "responsibility",
        ],

        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "react",
            "flask",
            "streamlit",
            "docker",
            "git",
            "aws",
            "azure",
            "gcp",
            "machine learning",
            "data analysis",
            "pandas",
            "numpy",
            "html",
            "css",
            "spring",
            "node",
            "node.js",
            "flutter",
            "skills",
            "programming",
            "database",
        ],

        "availability": [
            "available",
            "join",
            "joining",
            "notice period",
            "immediately",
            "immediate",
            "week",
            "weeks",
            "month",
            "months",
            "day",
            "days",
        ],

        "salary_expectation": [
            "salary",
            "expected",
            "compensation",
            "package",
            "lpa",
            "lakhs",
            "lakh",
            "per annum",
            "pay",
        ],

        "location": [
            "location",
            "relocate",
            "relocation",
            "remote",
            "hybrid",
            "onsite",
            "city",
            "work from home",
        ],
    }

    VAGUE_RESPONSES = {
        "yes",
        "yes.",
        "no",
        "no.",
        "maybe",
        "maybe.",
        "okay",
        "okay.",
        "fine",
        "fine.",
        "good",
        "good.",
        "nothing",
        "nothing.",
        "not sure",
        "not sure.",
        "i don't know",
        "i dont know",
        "don't know",
        "dont know",
    }

    # Explicit order used only when two intents have equal scores.
    INTENT_PRIORITY = [
        "introduction",
        "education",
        "experience",
        "skills",
        "availability",
        "salary_expectation",
        "location",
    ]

    def normalize(self, text):
        """Normalize candidate response text."""

        if text is None:
            return ""

        if not isinstance(text, str):
            raise ValueError("Candidate response must be a string.")

        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)

        return text

    def keyword_matches(self, text, keyword):
        """
        Match complete words or phrases.

        Word boundaries prevent matches such as 'day'
        inside unrelated words.
        """

        keyword = keyword.lower().strip()

        if not keyword:
            return False

        if " " in keyword:
            pattern = (
                r"(?<!\w)"
                + re.escape(keyword)
                + r"(?!\w)"
            )
        else:
            pattern = r"\b" + re.escape(keyword) + r"\b"

        return re.search(pattern, text) is not None

    def calculate_intent_scores(self, normalized):
        """
        Calculate keyword match scores for every supported
        question-answer category.

        Each matched keyword contributes one point.
        """

        scores = {}

        for intent, keywords in self.KEYWORDS.items():

            matched_keywords = []

            for keyword in keywords:

                if self.keyword_matches(normalized, keyword):
                    matched_keywords.append(keyword)

            scores[intent] = {
                "score": len(matched_keywords),
                "matched_keywords": matched_keywords,
            }

        return scores

    def classify(self, text, question_category=None):
        """
        Classify a candidate answer.

        Priority:
        1. Missing answer
        2. Vague answer
        3. Question-category context
        4. General keyword scoring
        5. Short-answer fallback
        6. Off-topic
        """

        normalized = self.normalize(text)

        # 1. Missing answer
        if not normalized:
            return "missing"

        # 2. Vague answer
        if normalized in self.VAGUE_RESPONSES:
            return "vague"

        # 3. Calculate all intent scores
        intent_scores = self.calculate_intent_scores(normalized)

        # 4. Question-category context
        if question_category in self.KEYWORDS:

            context_score = intent_scores[question_category]["score"]

            # Give priority to the requested question category
            # when the answer contains evidence for that category.
            if context_score > 0:
                return question_category

        # 5. General keyword scoring
        best_score = max(
            item["score"]
            for item in intent_scores.values()
        )

        if best_score > 0:

            # Resolve ties using an explicit priority order.
            for intent in self.INTENT_PRIORITY:

                if intent_scores[intent]["score"] == best_score:
                    return intent

        # 6. Short answer without useful information
        if len(normalized.split()) < 4:
            return "vague"

        # 7. No matching intent
        return "off_topic"
