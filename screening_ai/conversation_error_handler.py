class ConversationErrorHandler:

    def silence_retry(self) -> str:

        return (
            "I didn't hear a response. "
            "Please take your time and try again."
        )

    def confusion_retry(self) -> str:

        return (
            "No problem. Let me ask that "
            "in a simpler way."
        )

    def repeated_answer_retry(self) -> str:

        return (
            "Thank you. I already have that information. "
            "Could you provide a little more detail?"
        )

    def final_retry_message(self) -> str:

        return (
            "That's okay. We can move on to the "
            "next question."
        )

    def technical_failure(self) -> str:

        return (
            "I'm sorry, but I encountered a temporary "
            "problem. Let's try that question again."
        )