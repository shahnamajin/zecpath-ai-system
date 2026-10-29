import re


class IntentClassifier:
    """
    Rule-based intent classifier for Zecpath HR screening.

    The classifier identifies the semantic intent of a candidate's
    response using question context and keyword matching.
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

    def normalize(self, text):
        """
        Normalize input text.
        """

        if text is None:
            return ""

        text = text.lower().strip()

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text

    def keyword_matches(self, text, keyword):
        """
        Safely check whether a keyword or phrase exists.

        Multi-word phrases are searched normally.
        Single words use word boundaries so that words such as
        'day' do not match inside unrelated words.
        """

        keyword = keyword.lower().strip()

        if " " in keyword:
            return keyword in text

        pattern = r"\b" + re.escape(keyword) + r"\b"

        return re.search(pattern, text) is not None

    def classify(self, text, question_category=None):
        """
        Classify a candidate answer.

        Priority:
        1. Missing
        2. Vague
        3. Question-category context
        4. General keyword matching
        5. Short-answer fallback
        6. Off-topic
        """

        normalized = self.normalize(text)

        # --------------------------------------------------
        # 1. Missing answer
        # --------------------------------------------------

        if not normalized:
            return "missing"

        # --------------------------------------------------
        # 2. Vague answer
        # --------------------------------------------------

        if normalized in self.VAGUE_RESPONSES:
            return "vague"

        # --------------------------------------------------
        # 3. Context-aware classification
        # --------------------------------------------------

        if question_category in self.INTENTS:

            category_keywords = self.KEYWORDS.get(
                question_category,
                []
            )

            for keyword in category_keywords:

                if self.keyword_matches(
                    normalized,
                    keyword
                ):
                    return question_category

        # --------------------------------------------------
        # 4. General keyword scoring
        # --------------------------------------------------

        scores = {}

        for intent, keywords in self.KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if self.keyword_matches(
                    normalized,
                    keyword
                ):
                    score += 1

            scores[intent] = score

        best_intent = max(
            scores,
            key=scores.get
        )

        # --------------------------------------------------
        # 5. Known intent found
        # --------------------------------------------------

        if scores[best_intent] > 0:
            return best_intent

        # --------------------------------------------------
        # 6. Short answer without useful information
        # --------------------------------------------------

        if len(normalized.split()) < 4:
            return "vague"

        # --------------------------------------------------
        # 7. Nothing matches
        # --------------------------------------------------

        return "off_topic"