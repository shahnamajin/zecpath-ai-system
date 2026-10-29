# Day 34 – Dynamic Follow-Up Logic

## 1. Objective

Enable adaptive questioning based on candidate responses.

## 2. Features

- Incomplete and vague response detection
- Clarification triggers
- Deepening questions
- Example-based prompts
- Scenario-based questions
- Response-driven difficulty adaptation
- Question repetition prevention
- Follow-up count limits
- Conversation-aware decision output

## 3. Decision Logic

```text
Candidate Response
       |
       v
Response Quality Analysis
       |
       +-- Empty / Very Short / Uncertain --> Clarification
       |
       +-- General Claim -----------------> Example-Based
       |
       +-- Short / Vague ------------------> Deepening
       |
       +-- Detailed + Confident ----------> Scenario-Based
       |
       v
Check Question History
       |
       +-- Repeated --> Block / Regenerate
       |
       +-- New ------> Return Follow-Up
```

## 4. Difficulty Adaptation

| Trigger | Difficulty |
|---|---|
| Clarification | Simple |
| Deepening | Medium |
| Example-based | Medium |
| Scenario-based | Advanced |

## 5. Repetition Prevention

Every generated follow-up is normalized and compared with the existing question history. An exact normalized match is blocked.

## 6. Safety Limits

The engine limits follow-ups to two per question by default. Once the limit is reached, the interview continues instead of repeatedly probing the candidate.

## 7. Implementation

- `response_quality_analyzer.py`
- `question_repetition_checker.py`
- `dynamic_follow_up_engine.py`
- `adaptive_question_engine.py`
- `demo_dynamic_follow_up.py`
- `test_dynamic_follow_up.py`

## 8. Validation

The Day 34 test suite validates:
- Empty responses
- Short responses
- Vague responses
- General claims
- Detailed confident responses
- Repetition prevention
- Follow-up limits
- Follow-up eligibility
- Difficulty adaptation
- Response-analysis output


## 9. Conversation State Tracking

`dynamic_follow_up_state.py` tracks:

- Candidate ID
- Session ID
- Current question ID
- Response count
- Follow-up count
- Trigger history
- Follow-up question history
- Current difficulty

The state prevents uncontrolled follow-up loops and provides context for the next adaptive decision.
