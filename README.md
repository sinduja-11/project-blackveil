
# PROJECT BLACKVEIL

### Adaptive Deception and Intelligence Defence for Permissioned Blockchains

**"It doesn't just defend the blockchain. It turns deception into intelligence, and intelligence into defence."**

---

## 1. Overview

PROJECT BLACKVEIL is a cybersecurity research prototype designed to protect permissioned blockchain networks against compromised credentials, malicious insiders and suspicious participant behaviour.

Traditional authentication verifies whether a participant possesses valid credentials. However, stolen credentials can allow an attacker to appear legitimate.

BLACKVEIL addresses this limitation by continuously analysing participant behaviour, calculating dynamic risk scores and applying adaptive security responses.

When a session reaches a sufficiently high risk level, eligible sessions can be redirected into an isolated decoy blockchain environment for controlled investigation while independent transaction validation protects the real ledger.

---

## 2. Problem Statement

Permissioned blockchain networks restrict participation to authorised identities. However, an authorised identity does not necessarily represent a trustworthy participant.

If an attacker obtains legitimate credentials, the attacker may misuse the associated permissions while passing ordinary authentication checks.

This creates several security challenges:

- Stolen credentials can be used to impersonate legitimate participants.
- Malicious insiders may misuse authorised access.
- Suspicious behaviour may develop gradually and evade simple threshold-based detection.
- Traditional security controls may detect an attack only after suspicious requests have already reached sensitive components.
- Security investigations require reliable and tamper-evident evidence.

PROJECT BLACKVEIL aims to address these challenges through continuous behavioural assessment, adaptive enforcement and isolated deception.

---

## 3. How BLACKVEIL Works

BLACKVEIL operates as a security layer between blockchain participants and the real blockchain.

Its general workflow is:

1. **Identity Verification:** Verify participant identity and signed requests.
2. **Behavioural Monitoring:** Observe request patterns and transaction behaviour.
3. **Risk Assessment:** Calculate a dynamic risk score using security rules, anomaly detection and behavioural drift analysis.
4. **Adaptive Response:** Select an appropriate security response based on the calculated risk.
5. **Decoy Diversion:** Redirect eligible high-risk sessions into an isolated decoy blockchain.
6. **Transaction Protection:** Independently validate transactions before they reach the real ledger.
7. **Forensic Intelligence:** Record security events in a tamper-evident evidence chain.

### Adaptive Response Levels

| Risk Score | Response | Description |
|---|---|---|
| 0–29 | Observe | Continue monitoring normal activity |
| 30–54 | Challenge | Require additional signed proof and tighter controls |
| 55–74 | Restrict | Limit sensitive operations |
| 75–100 | Divert | Redirect eligible sessions to the isolated decoy |

---

## 4. Core Features

### 4.1 Zero-Trust Identity Verification

- Ed25519-based request authentication.
- Participant identity verification.
- Nonce and sequence validation.
- Continuous assessment after authentication.

### 4.2 Behavioural Risk Assessment

The risk engine evaluates multiple behavioural indicators:

- Request-rate deviation.
- Operation-sequence surprise.
- Distinct channels and keys accessed.
- Transaction-value deviation.
- Read/write ratio changes.
- Source and session-context changes.
- Integrity violations.

The proposed assessment combines:

- Hard security rules.
- Isolation Forest anomaly detection.
- CUSUM-based behavioural drift detection.
- EWMA-based risk-score smoothing.

### 4.3 Adaptive Security Response

BLACKVEIL applies different response levels depending on the calculated risk.

It also uses transition controls to prevent unstable switching between response levels.

### 4.4 Isolated Decoy Blockchain

The decoy environment provides a controlled investigation space.

It is designed with:

- Synthetic blockchain data.
- Independent cryptographic keys.
- Per-session state isolation.
- Separate network boundaries.
- No direct route to the real blockchain.
- Controlled response and state continuity.

### 4.5 Independent Transaction Guardian

Transactions are validated before commitment to the real ledger.

Validation includes identity, signature, nonce, permissions, endorsement requirements and application-specific invariants.

### 4.6 Tamper-Evident Forensic Intelligence

Security events are recorded using:

- Canonical JSON event representation.
- SHA-256 hash chaining.
- Ed25519 evidence-batch signatures.
- Periodic evidence-chain anchoring.
- Integrity verification.

### 4.7 Threat Intelligence and Monitoring

Confirmed incidents can produce candidate threat indicators.

Policy updates undergo validation, shadow testing and analyst approval before activation.

---

## 5. Architecture

The main logical components are:

1. Blockchain Participants
2. BLACKVEIL Gateway
3. Identity Verification Module
4. Behavioural Risk Assessment Engine
5. Adaptive Response Controller
6. Real Permissioned Blockchain
7. Transaction Integrity Guardian
8. Isolated Decoy Blockchain
9. Forensic Evidence Service
10. Security Monitoring Dashboard
11. Threat Intelligence and Policy Manager

The risk assessment engine operates within the gateway application process in the initial prototype to avoid unnecessary network communication overhead.

The decoy and real blockchain environments remain isolated.

---

## 6. Threat Model

The prototype focuses on three primary adversary profiles:

| Adversary | Description |
|---|---|
| A1 – Stolen-Credential Outsider | External attacker using compromised legitimate credentials |
| A2 – Malicious Insider | Authorised participant intentionally misusing access |
| A3 – Slow-and-Low Adversary | Attacker gradually changing behaviour to avoid immediate detection |

The prototype also considers replayed requests, reconnaissance, forensic tampering, gateway bypass attempts and component failures.

Consensus-level 51% attacks, smart-contract vulnerabilities and large-scale network denial-of-service attacks are outside the current prototype scope.

---

## 7. Technology Stack

The intended implementation technologies are:

| Area | Technology |
|---|---|
| Backend | Python |
| API Layer | FastAPI |
| Cryptography | Ed25519, SHA-256 |
| Behavioural Analysis | Scikit-learn, Isolation Forest |
| Drift Detection | CUSUM, EWMA |
| Database | PostgreSQL |
| Frontend | React |
| Deployment | Docker Compose |
| Version Control | Git and GitHub |

Technologies and versions may be refined during implementation.

---

## 8. Evaluation Strategy

BLACKVEIL will be evaluated in a controlled local environment with eight simulated blockchain participants.

Four configurations will be compared:

- C0: Baseline blockchain.
- C1: Rule-based detection.
- C2: Rules, anomaly detection and drift detection without diversion.
- C3: Full BLACKVEIL architecture with adaptive response and decoy diversion.

### Initial Evaluation Targets

| Metric | Target |
|---|---|
| Detection Rate | >= 90% |
| False Positive Rate | <= 5% |
| Median Containment Time | < 5 seconds |
| Invalid or Malicious Real-Chain Commits | 0 |
| Gateway p95 Latency | < 15 ms |
| Throughput Loss | < 10% |
| Decoy Distinguishability | <= 10% |

These are evaluation targets, not achieved results. Actual measurements will be documented after implementation and testing.

---

## 9. Project Documentation

Detailed design documents are maintained in the `docs/` directory.

| Document | Purpose |
|---|---|
| `problem_statement.md` | Defines the problem, objectives and scope |
| `requirements.md` | Defines functional and non-functional requirements |
| `architecture.md` | Explains components, workflows and security boundaries |
| `threat_model.md` | Identifies adversaries, threats and mitigations |
| `test_plan.md` | Defines testing scenarios and evaluation criteria |

---

## 10. Development Status

**Current Stage: Phase 0 – Project Foundation**

| Phase | Description | Status |
|---|---|---|
| Phase 0 | Requirements, architecture, threat model and test planning | Documentation in progress |
| Phase 1 | Development environment and project foundation | Pending |
| Phase 2 | Gateway and identity verification | Pending |
| Phase 3 | Behavioural monitoring and risk assessment | Pending |
| Phase 4 | Adaptive response controller | Pending |
| Phase 5 | Real blockchain simulation and transaction guardian | Pending |
| Phase 6 | Isolated decoy blockchain | Pending |
| Phase 7 | Forensic intelligence and dashboard | Pending |
| Phase 8 | Integration, evaluation and demonstration | Pending |

Implementation status will be updated as each component is completed and verified.

---

## 11. Ethical Scope

PROJECT BLACKVEIL is developed as a defensive cybersecurity research prototype.

All experiments will use synthetic data, test credentials and locally controlled environments.

Testing against external systems or networks will only be performed with explicit authorisation.

---

## 12. Project Goal

The goal of PROJECT BLACKVEIL is to demonstrate how continuous trust assessment, adaptive security enforcement, blockchain deception and tamper-evident forensic intelligence can work together to protect permissioned blockchain networks.

**PROJECT BLACKVEIL — Turning suspicious activity into actionable security intelligence.**
