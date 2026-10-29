# Day 22 – HR Screening Dataset Creation

## Objective

The objective of Day 22 was to create a structured and AI-ready HR screening question bank for the Zecpath autonomous hiring platform.

The dataset is designed to support automated HR screening conversations.

---

## Question Categories

The dataset contains the following categories:

1. Introduction
2. Education
3. Experience
4. Skills
5. Location
6. Salary
7. Notice Period

---

## Question Metadata

Every question contains:

- Question ID
- Category
- Question text
- Expected answer type
- Mandatory/optional status
- Scoring importance
- Applicable roles
- Difficulty
- Follow-up availability
- Maximum follow-ups

---

## Expected Answer Types

The dataset supports different response types:

- open_text
- yes_no
- education
- experience
- skills
- technical_experience
- project_experience
- motivation
- salary
- salary_range
- duration
- date
- duration_date
- work_preference

These answer types will later help the AI response evaluation engine.

---

## Role-Based Question Selection

Questions can be assigned to:

- All roles
- Python Developer
- Java Developer
- Full Stack Developer
- AI Engineer
- Data Analyst
- Data Scientist

This allows Zecpath to dynamically select appropriate questions.

---

## Scoring Importance

Each question contains a scoring importance between 0 and 1.

Example:

- 1.0 = Critical
- 0.8 = High
- 0.6 = Medium
- 0.4 = Low
- 0.2 = Very Low

This value can later be used by the screening evaluation engine.

---

## Reusable Question Templates

Reusable templates were introduced to reduce duplication.

Example:

"Can you explain your experience with {skill}?"

The `{skill}` variable can dynamically be replaced with:

- Python
- Java
- SQL
- React
- Docker
- AWS

---

## Multilingual Support

The dataset is designed for future multilingual screening.

Supported language identifiers include:

- en – English
- ml – Malayalam
- hi – Hindi
- ta – Tamil
- kn – Kannada

Additional languages can be added without changing the core question schema.

---

## AI Conversation Object

Questions are converted into conversation-ready objects containing:

- Prompt
- Language
- Category
- Expected answer type
- Mandatory status
- Scoring importance
- Follow-up configuration
- Role metadata

---

## Testing

The following components were tested:

- Dataset loading
- Question schema
- Unique question IDs
- Scoring range
- Dataset validation
- Category filtering
- Mandatory question filtering
- Role-based selection
- Python-specific question selection
- Screening sequence
- Conversation object generation

---

## Day 22 Deliverables

Completed deliverables:

- HR screening question dataset
- Question category mapping
- Role-specific question bank
- Expected answer type mapping
- Mandatory/optional classification
- Scoring importance metadata
- Reusable question templates
- Multilingual-ready dataset
- AI conversation-ready objects
- Question loader
- Question selector
- Conversation builder
- Unit tests
- Documentation