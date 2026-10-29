# Zecpath Confidence & Sentiment Signal Analysis

## Overview

The Confidence & Sentiment Signal Analysis module evaluates observable communication signals from candidate screening responses.

The module does not make psychological or personality judgments. It analyzes measurable textual and speech-related indicators.

## Signals

- Hesitation
- Response length
- Response pace
- Sentiment
- Uncertainty
- Contradictions
- Communication strength

## Hesitation

The system detects markers such as:

- um
- uh
- erm
- hmm
- mmm
- ...
- --

## Response Length

Responses are categorized as:

- empty
- very_short
- short
- medium
- long

## Response Pace

When response duration is available, words per minute are calculated.

## Sentiment

Responses are classified as:

- positive
- neutral
- negative

## Uncertainty

The system identifies phrases such as:

- I think
- maybe
- probably
- perhaps
- not sure
- I guess
- possibly
- I don't know

## Contradiction Detection

The module compares current structured candidate information with previous context.

Examples include differences in:

- Experience duration
- Previously mentioned skills

## Communication Strength

An observable communication-strength indicator is generated using hesitation, uncertainty, response length and pace signals.

The score is normalized between 0 and 100.

## Output

The behavioral report contains:

- Communication signals
- Sentiment
- Uncertainty
- Hesitation
- Response length
- Response pace
- Contradiction indicators
- Communication strength