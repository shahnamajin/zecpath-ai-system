from typing import Dict, Any, Optional

from .conversation_state import (
    ConversationState,
    ConversationContext,
)

from .fallback_handler import (
    FallbackHandler,
)

from .conversation_error_handler import (
    ConversationErrorHandler,
)


class ConversationFlow:

    def __init__(
        self,
        context: ConversationContext,
    ):

        self.context = context

        self.fallback_handler = (
            FallbackHandler()
        )

        self.error_handler = (
            ConversationErrorHandler()
        )

    def start_question(
        self,
        question_id: str,
        question: str,
        category: str = "general",
    ) -> Dict[str, Any]:

        self.context.state = (
            ConversationState.ASKING
        )

        self.context.current_question_id = (
            question_id
        )

        self.context.current_question = (
            question
        )

        self.context.current_category = (
            category
        )

        self.context.retry_count = 0
        self.context.clarification_count = 0
        self.context.repeat_count = 0

        return self._result(
            action="ask_question",
            message=question,
        )

    def process_response(
        self,
        response: Optional[str],
        intent: str = "unknown",
        is_repeated: bool = False,
    ) -> Dict[str, Any]:

        self.context.state = (
            ConversationState.PROCESSING_RESPONSE
        )

        response = (
            response.strip()
            if response
            else ""
        )

        # 1. Silence
        if not response:

            return self._handle_silence()

        # 2. Repeated answer
        if is_repeated:

            return self._handle_repeated_answer(
                response
            )

        # 3. Confusion / vague answer
        if intent in {
            "vague",
            "confused",
            "missing",
        }:

            return self._handle_confusion()

        # 4. Valid answer
        self.context.previous_answer = response

        self.context.state = (
            ConversationState.NEXT_QUESTION
        )

        return self._result(
            action="next_question",
            message="Thank you. Let's continue.",
            response=response,
        )

    def _handle_silence(self):

        if self.context.retry_count < 1:

            self.context.retry_count += 1

            self.context.state = (
                ConversationState.RETRY
            )

            return self._result(
                action="retry",
                message=self.error_handler.silence_retry(),
            )

        self.context.state = (
            ConversationState.FALLBACK
        )

        self.context.retry_count += 1

        fallback = (
            self.fallback_handler.get_question(
                self.context.current_category,
                self.context.retry_count - 1,
            )
        )

        return self._result(
            action="fallback",
            message=fallback,
        )

    def _handle_confusion(self):

        if self.context.clarification_count < 1:

            self.context.clarification_count += 1

            self.context.state = (
                ConversationState.CLARIFICATION
            )

            return self._result(
                action="clarify",
                message=self.error_handler.confusion_retry(),
            )

        self.context.state = (
            ConversationState.FALLBACK
        )

        fallback = (
            self.fallback_handler.get_question(
                self.context.current_category,
                self.context.clarification_count,
            )
        )

        return self._result(
            action="fallback",
            message=fallback,
        )

    def _handle_repeated_answer(
        self,
        response: str,
    ):

        self.context.repeat_count += 1

        if self.context.repeat_count <= 1:

            self.context.state = (
                ConversationState.CLARIFICATION
            )

            return self._result(
                action="clarify",
                message=(
                    self.error_handler
                    .repeated_answer_retry()
                ),
            )

        self.context.state = (
            ConversationState.FALLBACK
        )

        fallback = (
            self.fallback_handler.get_question(
                self.context.current_category,
                self.context.repeat_count - 1,
            )
        )

        return self._result(
            action="fallback",
            message=fallback,
        )

    def complete(self):

        self.context.state = (
            ConversationState.COMPLETED
        )

        return self._result(
            action="complete",
            message=(
                "Thank you. The screening "
                "conversation is complete."
            ),
        )

    def _result(
        self,
        action: str,
        message: str,
        response: Optional[str] = None,
    ):

        result = {
            "state": self.context.state.value,
            "action": action,
            "message": message,
        }

        if response is not None:
            result["response"] = response

        return result