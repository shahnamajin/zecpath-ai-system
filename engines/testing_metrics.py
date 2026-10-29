class TestingMetrics:

    def accuracy(self, results):

        if not results:
            return 0

        correct = sum(
            1
            for result in results
            if result["ai_decision"]
            == result["manual_decision"]
        )

        return round(
            (correct / len(results)) * 100,
            2
        )

    def precision(self, results):

        tp = 0
        fp = 0

        for result in results:

            ai = result["ai_decision"]
            manual = result["manual_decision"]

            if ai == "Shortlist" and manual == "Shortlist":
                tp += 1

            elif ai == "Shortlist" and manual != "Shortlist":
                fp += 1

        if tp + fp == 0:
            return 0

        return round(
            tp / (tp + fp) * 100,
            2
        )

    def recall(self, results):

        tp = 0
        fn = 0

        for result in results:

            ai = result["ai_decision"]
            manual = result["manual_decision"]

            if ai == "Shortlist" and manual == "Shortlist":
                tp += 1

            elif ai != "Shortlist" and manual == "Shortlist":
                fn += 1

        if tp + fn == 0:
            return 0

        return round(
            tp / (tp + fn) * 100,
            2
        )