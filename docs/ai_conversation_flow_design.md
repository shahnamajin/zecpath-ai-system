# Day 29 – AI Conversation Flow Design

## Objective

Define a dynamic AI conversation flow for voice-based candidate screening.

## Conversation States

The system uses the following states:

START
ASKING
WAITING_FOR_RESPONSE
PROCESSING_RESPONSE
CLARIFICATION
RETRY
FALLBACK
NEXT_QUESTION
COMPLETED
FAILED

## Decision Flow

Candidate response is classified into:

1. Valid answer
2. Silence
3. Confusion or vague answer
4. Repeated answer

### Valid Answer

Move to the next question.

### Silence

First occurrence:
Retry the question politely.

Second occurrence:
Use a fallback question.

### Confusion

First occurrence:
Ask the question in a simpler way.

Second occurrence:
Use a fallback question.

### Repeated Answer

First occurrence:
Request additional information.

Second occurrence:
Use a fallback question.

## Error Handling

The conversation uses polite messages for:

- Silence
- Confusion
- Repeated answers
- Temporary failures

The objective is to maintain a natural conversation instead of abruptly terminating the screening.

## State Machine

START
↓
ASKING
↓
WAITING_FOR_RESPONSE
↓
PROCESSING_RESPONSE

Valid Answer → NEXT_QUESTION

Silence → RETRY → FALLBACK

Confusion → CLARIFICATION → FALLBACK

Repeated Answer → CLARIFICATION → FALLBACK

After final question → COMPLETED