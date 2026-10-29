# Zecpath AI ATS API Specification

## 1. Overview

The Zecpath AI ATS API provides REST endpoints for resume upload, resume parsing, candidate scoring, candidate shortlisting, and asynchronous resume processing.

Base URL:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

---

# 2. Resume Upload API

## Endpoint

POST /api/resume/upload

## Purpose

Uploads a candidate resume and generates a unique candidate ID.

## Request

Content-Type:

multipart/form-data

Parameter:

file – Resume PDF file

## Example

Resume:

Shahna_Maji_Resume.pdf

## Successful Response

HTTP 200

```json
{
    "success": true,
    "candidate_id": "CAND-2B83E96C",
    "filename": "Shahna_Maji_Resume.pdf",
    "status": "uploaded"
}