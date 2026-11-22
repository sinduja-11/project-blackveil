
# PROJECT BLACKVEIL
## Threat Model

## 1. Introduction

PROJECT BLACKVEIL is an adaptive deception and intelligence defence layer designed to protect permissioned blockchain networks from credential misuse, malicious insider activity and suspicious participant behaviour.

This threat model identifies the assets that require protection, potential adversaries, trust boundaries, security threats, existing safeguards and residual risks.

The purpose is to establish what the prototype is designed to defend against and clearly document its security assumptions and limitations.

---

## 2. Security Objectives

BLACKVEIL aims to achieve the following security objectives:

1. Protect the integrity of the real blockchain ledger.
2. Prevent unauthorised or suspicious transactions from reaching the real blockchain.
3. Identify compromised identities through behavioural analysis.
4. Apply adaptive responses based on continuously calculated risk.
5. Isolate high-risk sessions from the real blockchain.
6. Provide a controlled decoy environment for investigating suspicious activity.
7. Preserve tamper-evident forensic evidence.
8. Prevent failures in individual components from silently bypassing security controls.

---

## 3. Assets Requiring Protection

The following assets are considered security-critical.

| Asset | Description | Security Requirement |
|---|---|---|
| Real blockchain ledger | Actual transactions and blockchain state | Integrity and confidentiality |
| Participant credentials | Private keys and identity information | Confidentiality and protection from misuse |
| Gateway | Entry point for blockchain requests | Availability and integrity |
| Risk assessment engine | Behavioural analysis and risk scoring | Integrity and reliability |
| Risk policies | Thresholds and response rules | Integrity and controlled modification |
| Decoy blockchain | Isolated investigation environment | Isolation and integrity |
| Forensic records | Security events and investigation evidence | Integrity and traceability |
| Threat intelligence | Confirmed indicators and policy updates | Authenticity and integrity |
| Dashboard | Security monitoring interface | Access control and availability |
| Transaction guardian | Independent validation before ledger submission | Integrity and enforcement |

---

## 4. Adversary Profiles

BLACKVEIL considers three primary adversary profiles.

### A1 – Stolen-Credential Outsider

An external attacker obtains a legitimate blockchain participant's credentials.

The attacker may attempt to:
- Access the network using the stolen identity.
- Explore available channels and permitted operations.
- Submit unusual or unauthorised transaction requests.
- Perform reconnaissance while attempting to appear legitimate.
- Exploit the trust associated with the compromised identity.

**Primary defence:**
Identity verification, behavioural risk assessment, transaction validation, adaptive restriction and controlled diversion.

### A2 – Malicious Insider

An authorised participant intentionally misuses their legitimate access.

The insider may attempt to:
- Access information beyond their normal operational requirements.
- Perform unusual transaction sequences.
- Abuse legitimate permissions.
- Manipulate permitted operations for unauthorised purposes.
- Exploit their knowledge of normal network behaviour.

**Primary defence:**
Behavioural baselines, operation-sequence analysis, permission enforcement, transaction invariants and forensic logging.

### A3 – Slow-and-Low Adversary

An attacker deliberately keeps individual actions within normal-looking limits to avoid immediate detection.

The attacker may attempt to:
- Spread suspicious activity across longer periods.
- Gradually change transaction behaviour.
- Avoid sudden increases in request volume.
- Perform low-frequency reconnaissance.
- Remain below individual detection thresholds.

**Primary defence:**
Sliding-window behavioural analysis, cumulative risk scoring, EWMA smoothing and CUSUM drift detection.

---

## 5. Trust Boundaries

Trust boundaries identify where data or requests cross between components with different security responsibilities.

### 5.1 Participant to Gateway

All participant requests must pass through the BLACKVEIL gateway.

The gateway verifies identity and inspects requests before forwarding them.

**Security requirement:** No participant should be able to bypass the gateway and directly access the real blockchain.

### 5.2 Gateway to Real Blockchain

The gateway forwards permitted requests to the real blockchain.

The independent transaction guardian validates transactions before commitment.

**Security requirement:** Suspicious or invalid transactions must not be committed to the real ledger.

### 5.3 Gateway to Decoy Blockchain

The gateway can direct eligible high-risk sessions to the isolated decoy environment.

The decoy uses synthetic data and independently managed credentials.

**Security requirement:** Decoy activity must never modify the real blockchain.

### 5.4 Decoy to Real Blockchain

The decoy must not have a network route or direct communication path to the real blockchain.

**Security requirement:** Strict isolation must prevent an attacker interacting with the decoy from reaching the real ledger through it.

### 5.5 Backend to Database

The application stores risk information, configuration, session history and forensic records.

**Security requirement:** Database access must be restricted according to component responsibilities. Forensic records must not be silently overwritten.

### 5.6 Analyst to Administrative Controls

Analysts may review incidents and approve policy changes.

**Security requirement:** Policy changes must be authenticated, authorised, recorded and versioned.

---

## 6. Threat Scenarios and Mitigations

| ID | Threat | Potential Impact | BLACKVEIL Mitigation |
|---|---|---|---|
| T01 | Stolen participant credentials | Attacker acts under a legitimate identity | Behavioural monitoring and adaptive responses |
| T02 | Replayed requests | Duplicate or unauthorised operations | Nonce and sequence validation |
| T03 | Unusual transaction behaviour | Integrity violations or misuse of permissions | Transaction guardian and risk assessment |
| T04 | Channel reconnaissance | Exposure of network structure and accessible resources | Request inspection, access restrictions and diversion |
| T05 | Slow behavioural changes | Attacker avoids simple threshold detection | EWMA and CUSUM analysis |
| T06 | Direct gateway bypass | Requests avoid BLACKVEIL controls | Network isolation and mandatory gateway routing |
| T07 | Decoy escape attempt | Attacker attempts to reach the real environment | Separate network, independent keys and outbound restrictions |
| T08 | Forensic record tampering | Loss of trustworthy investigation evidence | Hash-chained records and signed evidence batches |
| T09 | Threat intelligence poisoning | Incorrect policies or indicators affect detection | Shadow testing and analyst approval |
| T10 | Gateway failure | Security enforcement becomes unavailable | Fail-closed behaviour |
| T11 | Risk engine failure | Requests cannot receive reliable risk assessments | Protected writes are rejected or restricted |
| T12 | Decoy failure | Investigation environment becomes unavailable | Restrict or quarantine the session |
| T13 | Forensic storage failure | Security evidence cannot be reliably preserved | Bounded protected buffering and restricted operation |
| T14 | Dashboard failure | Analysts temporarily lose visibility | Gateway enforcement continues independently |

---

## 7. Security Controls

### 7.1 Identity and Credential Protection

- Participant identities are verified using enrolled public keys.
- Ed25519 signatures are used to authenticate signed requests.
- Invalid signatures are rejected.
- Nonces or sequence numbers prevent replayed requests.
- Authentication does not automatically grant unrestricted access.

### 7.2 Behavioural Risk Assessment

The gateway evaluates behavioural indicators over a sliding time window.

The prototype considers:

1. Request-rate deviation.
2. Operation-sequence surprise.
3. Number of distinct channels and keys accessed.
4. Transaction-value deviation.
5. Read/write ratio changes.
6. Source and session-context changes.
7. Integrity violations.

The risk engine combines hard security rules, Isolation Forest and CUSUM-based drift analysis.

### 7.3 Adaptive Response

Risk scores determine the response level:

| Risk Score | Response | Purpose |
|---|---|---|
| 0–29 | Observe | Continue normal operation and monitor |
| 30–54 | Challenge | Require additional signed proof and tighter limits |
| 55–74 | Restrict | Limit sensitive operations |
| 75–100 | Divert | Move eligible high-risk sessions to the decoy |

Anti-flapping rules prevent rapid switching between response levels.

### 7.4 Real Blockchain Protection

The transaction guardian independently validates requests before they reach the real ledger.

It checks:
- Participant identity and signature.
- Nonce or sequence validity.
- Channel and operation permissions.
- Transaction endorsement requirements.
- Transaction-value limits.
- Application-specific invariants.

Invalid transactions are rejected.

### 7.5 Decoy Isolation

The decoy blockchain is maintained separately from the real blockchain.

Its safeguards include:
- Synthetic data.
- Independent cryptographic keys.
- Separate network environment.
- No direct route to the real blockchain.
- Restricted outbound communication.
- Per-session state isolation.
- Resource limits.

The decoy must not become a bridge into the real network.

### 7.6 Forensic Integrity

Security events are recorded using canonical JSON and SHA-256 hash chaining.

Gateway-generated evidence batches are digitally signed.

Periodic evidence-chain heads are anchored to the real ledger.

A verification process checks whether records have been altered or removed.

### 7.7 Threat Intelligence Protection

New threat indicators are treated as candidates rather than automatically trusted facts.

Policy updates must undergo:
- Validation against known traces.
- Shadow testing.
- False-positive impact assessment.
- Analyst approval.
- Versioning and rollback support.

---

## 8. Failure and Fail-Safe Behaviour

BLACKVEIL must not silently bypass security controls when a component fails.

| Component Failure | Expected Behaviour |
|---|---|
| Gateway unavailable | Requests are rejected; direct access to the real blockchain is not permitted |
| Risk engine unavailable | Protected writes fail closed or remain restricted |
| Decoy unavailable | Eligible suspicious sessions remain restricted or quarantined |
| Forensic storage unavailable | Evidence is placed in a bounded protected buffer; protected operations are restricted if evidence integrity cannot be maintained |
| Dashboard unavailable | Gateway enforcement and transaction validation continue |
| Threat intelligence unavailable | Last approved policy version remains active |

Fail-closed behaviour prioritises ledger integrity over uninterrupted operation.

---

## 9. Out-of-Scope Threats

The following threats are outside the current prototype's scope:

1. Consensus-level 51% attacks.
2. Smart-contract vulnerabilities and arbitrary contract exploitation.
3. Large-scale network-layer denial-of-service attacks.
4. Physical hardware compromise.
5. Complete compromise of all trusted administrators.
6. Perfect long-term behavioural mimicry.
7. Production-scale protection across hundreds of blockchain nodes.

These areas may be considered in future extensions.

---

## 10. Residual Risks and Limitations

Even with the proposed safeguards, some risks remain.

### 10.1 Pre-Diversion Information Exposure

Information already legitimately served to a session cannot be taken back.

BLACKVEIL therefore limits sensitive information exposure before diversion and uses masked or synthetic data where appropriate.

### 10.2 Decoy Fingerprinting

An experienced attacker may identify inconsistencies between the decoy and the real environment.

Fidelity testing and controlled state synchronisation reduce, but do not eliminate, this possibility.

### 10.3 Gateway as a Critical Component

The gateway is a central enforcement point.

Its failure can interrupt access to the blockchain. The prototype therefore uses fail-closed behaviour rather than allowing direct bypass.

### 10.4 Consensus-Critical Participants

Consensus-critical nodes, such as a sole ordering node, must not be automatically diverted.

If such a participant becomes suspicious, BLACKVEIL restricts its operations and escalates the incident for human review.

This leaves a residual risk that requires careful operational handling.

### 10.5 Behavioural Evasion

An attacker may attempt to imitate legitimate behaviour.

Multiple behavioural signals, cumulative risk scoring and drift analysis help reduce this risk, but cannot guarantee detection of every attack.

---

## 11. Ethical and Operational Boundaries

PROJECT BLACKVEIL is developed as a defensive cybersecurity research prototype.

All experiments must:
- Use an isolated, locally controlled environment.
- Use synthetic blockchain data and test credentials.
- Be performed only on systems owned by the developer or explicitly authorised for testing.
- Avoid accessing real user information.
- Avoid interacting with external blockchain networks without authorisation.
- Preserve evidence for defensive investigation.
- Avoid retaliatory or unauthorised actions against suspected attackers.

---

## 12. Conclusion

This threat model establishes the security assumptions, adversary profiles, protected assets, trust boundaries and defensive controls of PROJECT BLACKVEIL.

The prototype focuses on detecting credential misuse and suspicious participant behaviour while protecting the real blockchain through independent transaction validation, adaptive restrictions, isolated deception and tamper-evident forensic records.

Its security design prioritises real-ledger integrity, controlled information exposure and safe failure behaviour.
