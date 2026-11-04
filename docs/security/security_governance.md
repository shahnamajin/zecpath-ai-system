# ZECPath AI – Security and Governance Framework

## 1. Overview

This document describes the initial security and AI governance framework
implemented for the ZECPath AI hiring platform.

The framework covers:
- Audit logging
- Role-based access control
- Candidate consent management
- Data retention evaluation
- Encryption of stored files and data

This is an engineering implementation document, not a legal compliance
certification.

## 2. Audit Logging

Module: security/audit_logger.py

Audit events are stored in SQLite.

Recorded fields:
- Actor ID
- Actor role
- Action
- Resource type
- Resource ID
- Outcome
- UTC timestamp
- Sanitized metadata

Sensitive metadata fields such as passwords, tokens, transcript content,
resume text, email addresses and phone numbers are excluded.

Limitation:
SQLite audit records are not tamper-proof. Production deployment should
include restricted write access, integrity monitoring and secure backups.

## 3. Role-Based Access Control

Module: security/access_control.py

Supported roles:
- Admin
- Recruiter
- Company
- Candidate

Permissions are configured in config/security_policy.json.

The AccessControl module supports permission checks and raises
PermissionError for unauthorized operations.

Limitation:
Permission checks must be integrated into actual API endpoints and
processing entry points. Authentication and user identity verification
are not implemented by this module.

## 4. Consent Management

Module: security/consent_manager.py

Consent events are stored in a dedicated SQLite database.

Supported operations:
- Grant consent
- Withdraw consent
- Check current consent
- Retrieve consent history

Withdrawal is recorded as a new event, preserving previous consent history.

Limitation:
Consent management is not yet integrated into all AI processing
entry points. Recording consent does not automatically prevent
screening or interview processing.

## 5. Data Retention

Module: security/retention_manager.py

The retention manager evaluates records against configured retention
periods.

Supported capabilities:
- Expiration evaluation
- Retained and expired record counts
- Dry-run deletion evaluation
- Protection against deletion when automatic deletion is disabled

Retention periods remain unset pending privacy/legal review.

Limitation:
The module does not yet delete actual records or files. Integration
with the relevant storage backends is required before deletion can
be enabled.

## 6. Secure Storage

Module: security/secure_storage.py

Fernet authenticated encryption is used to:
- Encrypt byte data
- Decrypt encrypted byte data
- Encrypt files
- Decrypt files

The encryption key is read from the ZECPATH_ENCRYPTION_KEY environment
variable.

Security requirements:
- Never commit encryption keys to source control.
- Restrict access to encryption keys.
- Maintain secure backups.
- Establish a key rotation procedure.
- Protect temporary decrypted files.

Limitation:
Existing resumes, transcripts and reports are not automatically
encrypted. Their storage workflows must be integrated with SecureStorage.

## 7. Data Privacy Principles

ZECPath should follow these engineering principles:

- Collect only data required for hiring purposes.
- Provide clear candidate notices.
- Obtain and record applicable consent.
- Restrict candidate data access by role.
- Avoid storing sensitive content in audit metadata.
- Define and enforce approved retention periods.
- Support appropriate human review of AI recommendations.
- Protect stored candidate information.

## 8. Security Test Results

Focused security test modules:

- tests/security/test_security_core.py
- tests/security/test_consent_manager.py
- tests/security/test_retention_manager.py
- tests/security/test_secure_storage.py

Latest reported result:

24 tests passed.

This verifies the tested module behavior, not complete application-wide
security or legal compliance.

## 9. Production Readiness Checklist

[ ] Integrate authentication and authorization into API endpoints.
[ ] Enforce consent before relevant AI processing.
[ ] Approve retention periods with responsible reviewers.
[ ] Integrate deletion with actual storage backends.
[ ] Encrypt existing sensitive data at rest.
[ ] Establish encryption key rotation and recovery.
[ ] Restrict and monitor audit database access.
[ ] Review backup retention and deletion.
[ ] Conduct security testing and privacy review.
[ ] Verify applicable legal and regulatory requirements.

## 10. Compliance Status

Status: Engineering foundation implemented; production readiness pending.

The current implementation provides initial security components and
focused automated tests. It does not establish complete regulatory
compliance or guarantee secure operation of the entire platform.
