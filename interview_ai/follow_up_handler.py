from typing import Dict, Optional


class HRFollowUpHandler:
    """
    Handles follow-up questions during an HR interview.

    Follow-ups are generated based on:
    - Question category
    - Candidate response
    - Follow-up eligibility
    - Response quality
    """

    FOLLOW_UP_TEMPLATES = {
        "self_introduction": [
            "Can you tell me a little more about that?",
            "Which part of your background is most relevant to this role?"
        ],
        "career_journey": [
            "What was your biggest learning from that experience?",
            "What challenges did you face during that journey?"
        ],
        "strengths_weaknesses": [
            "Can you give me an example that demonstrates that?",
            "How are you working to improve in this area?"
        ],
        "teamwork_culture": [
            "What was your specific responsibility in that situation?",
            "How did you handle any challenges within the team?"
        ],
        "career_goals": [
            "What steps are you taking to achieve that goal?",
            "Why is that career direction important to you?"
        ],
        "availability_commitment": [
            "Is there anything that could affect your availability?",
            "Are you comfortable with the commitment required for this role?"
        ]
    }

    def __init__(self):
        self.follow_up_count = 0

    def needs_follow_up(
        self,
        response: str,
        follow_up_eligible: bool
    ) -> bool:
        """
        Determine whether a follow-up should be asked.

        A follow-up is considered when:
        - The question allows follow-up.
        - The response is very short or lacks detail.
        """

        if not follow_up_eligible:
            return False

        if not response or not response.strip():
            return True

        words = response.strip().split()

        # Very short answers need clarification.
        if len(words) < 8:
            return True

        return False

    def generate_follow_up(
        self,
        category: str,
        response: str
    ) -> Optional[str]:
        """
        Generate a category-specific follow-up question.
        """

        templates = self.FOLLOW_UP_TEMPLATES.get(category)

        if not templates:
            return None

        # Alternate between available templates.
        index = self.follow_up_count % len(templates)

        self.follow_up_count += 1

        return templates[index]

    def process_response(
        self,
        category: str,
        response: str,
        follow_up_eligible: bool
    ) -> Dict:
        """
        Process a candidate response and determine
        whether a follow-up is required.
        """

        should_follow_up = self.needs_follow_up(
            response=response,
            follow_up_eligible=follow_up_eligible
        )

        if should_follow_up:
            follow_up_question = self.generate_follow_up(
                category=category,
                response=response
            )

            return {
                "follow_up_required": True,
                "follow_up_question": follow_up_question,
                "reason": "response_needs_more_detail"
            }

        return {
            "follow_up_required": False,
            "follow_up_question": None,
            "reason": "response_sufficient"
        }