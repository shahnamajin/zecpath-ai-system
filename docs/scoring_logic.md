# ATS Scoring Logic

## Components

The ATS evaluates candidates using four major components:

- Skill Match
- Experience Relevance
- Education Alignment
- Semantic Similarity

## Software Engineer Weights

| Component | Weight |
|---|---:|
| Skill Match | 0.40 |
| Experience Relevance | 0.25 |
| Education Alignment | 0.15 |
| Semantic Similarity | 0.20 |

## Formula

Final Score =

(Skill Match × 0.40)
+
(Experience Relevance × 0.25)
+
(Education Alignment × 0.15)
+
(Semantic Similarity × 0.20)

## Recommendation Rules

| Score | Recommendation |
|---|---|
| 80 or above | Strong Match |
| 60–79 | Moderate Match |
| Below 60 | Weak Match |

## Example

Skill Match = 95

Experience Relevance = 70

Education Alignment = 100

Semantic Similarity = 64.2

Final Score = 83.34

Recommendation = Strong Match