# Day 30 – Screening System Testing & Optimization

## Objective

Validate the Zecpath AI screening pipeline using simulated screening scenarios and optimize its decision behavior.

## Testing Areas

- Simulated candidate responses
- Intent categories
- Screening decision thresholds
- Human-reference comparison
- False rejection detection
- Conversation decision behavior

## Optimization

The system uses configurable thresholds:

- Continue threshold: 70
- Clarification threshold: 45
- Retry threshold: 20

The system avoids immediate rejection when clarification or retry can provide additional information.

## False Rejection Reduction

Potentially relevant responses are protected from immediate rejection.

The system can:

1. Continue relevant responses.
2. Clarify uncertain responses.
3. Retry missing responses.
4. Clarify low-scoring responses before rejecting them.

## Human Judgment Comparison

The test framework supports comparison between AI decisions and a reference human-judgment dataset.

In production, this dataset should be created from multiple reviewers and evaluated for reviewer agreement.

## Outcome

The testing and optimization layer provides a repeatable way to identify decision errors and improve screening behavior.