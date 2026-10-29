\# Zecpath AI - HR Interview Engine Design



\## 1. Overview



The HR Interview Engine is a foundational component of the Zecpath AI hiring platform.



Its purpose is to conduct structured AI-assisted HR interviews based on candidate type, role type, interview category, candidate responses and follow-up eligibility.



The engine is designed to support both fresher and experienced candidates across technical and non-technical roles.



\---



\## 2. Objectives



The HR Interview Engine was designed to:



\- Define structured HR interview categories.

\- Maintain a reusable HR question bank.

\- Generate role-based questions.

\- Support fresher and experienced candidates.

\- Support technical and non-technical roles.

\- Maintain interview state.

\- Capture candidate responses.

\- Track question history.

\- Determine follow-up eligibility.

\- Generate category-specific follow-up questions.

\- Manage interview phases.

\- Complete the interview in a controlled manner.



\---



\## 3. HR Interview Categories



The current question bank contains six major categories.



\### 3.1 Self Introduction



Used to understand the candidate's background, communication and professional summary.



\### 3.2 Career Journey



Used to understand education, projects, previous experience and career progression.



\### 3.3 Strengths and Weaknesses



Used to understand candidate self-awareness, strengths and improvement areas.



\### 3.4 Teamwork and Culture Fit



Used to understand collaboration, communication, conflict handling and workplace behavior.



\### 3.5 Career Goals



Used to understand short-term goals, long-term goals and professional development.



\### 3.6 Availability and Commitment



Used to understand joining availability, relocation and commitment to the role.



\---



\## 4. Question Bank Architecture



The question bank is stored in:



```text

data/hr\_interview/hr\_question\_bank.json

