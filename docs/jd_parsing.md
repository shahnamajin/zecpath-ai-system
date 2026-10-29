# Job Description Parsing Documentation

## Purpose

The Job Description Parser converts unstructured job descriptions into structured, AI-readable job requirement data.

## Parsing Process

Job Description
        ↓
Text Normalization
        ↓
Role Extraction
        ↓
Skill Extraction
        ↓
Experience Extraction
        ↓
Education Extraction
        ↓
Structured JD Object

## Extracted Information

### 1. Job Role

The parser identifies the job title or role from the job description.

Examples:

- Software Engineer
- Python Developer
- Data Scientist
- Data Analyst
- Machine Learning Engineer

### 2. Required Skills

The parser identifies technical and professional skills mentioned in the job description.

Examples:

- Python
- Django
- SQL
- Docker
- AWS
- Machine Learning

### 3. Experience Requirements

The parser identifies the minimum experience required for the position.

Example:

```json
{
    "minimum_years": 2
}