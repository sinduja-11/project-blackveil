
# PROJECT BLACKVEIL
## Test Plan

## 1. Introduction

This document defines the testing strategy, test scenarios, evaluation metrics and acceptance criteria for PROJECT BLACKVEIL.

The objective is to verify whether the prototype can identify suspicious blockchain participant behaviour, apply adaptive security responses, isolate high-risk sessions and preserve trustworthy forensic evidence.

Testing will be conducted in a controlled local environment using simulated blockchain participants and synthetic data.

The test plan defines expected results and evaluation targets. It does not represent achieved results.

---

## 2. Testing Objectives

The testing process aims to verify the following:

1. Identity verification correctly accepts valid participants and rejects invalid credentials.
2. Behavioural monitoring identifies deviations from normal participant activity.
3. Risk assessment produces meaningful risk scores.
4. Adaptive response levels are applied correctly.
5. Suspicious sessions are isolated from the real blockchain.
6. The decoy blockchain provides a controlled investigation environment.
7. Invalid transactions are prevented from reaching the real ledger.
8. Forensic records remain tamper-evident.
9. System failures do not silently bypass security controls.
10. The prototype operates within acceptable performance limits.

---

## 3. Test Environment

The prototype will initially be evaluated on a single development machine.

### 3.1 Environment Configuration

| Component | Configuration |
|---|---|
| Deployment | Local environment using Docker Compose |
| Simulated participants | 8 blockchain nodes |
| Real blockchain | Local permissioned blockchain simulation |
| Decoy blockchain | Separate isolated simulation |
| Gateway | Python-based application |
| Risk assessment | Rules, Isolation Forest and CUSUM |
| Cryptography | Ed25519 and SHA-256 |
| Database | PostgreSQL |
| Dashboard | Web-based monitoring interface |
| Test data | Synthetic transactions and participant activity |

### 3.2 Repeatability

- Each experiment will use a predefined random seed.
- Each configuration will be tested across 10 independent runs.
- The same workload and attack scenarios will be used for comparable configurations.
- Test results will be recorded for later analysis.

This helps ensure that differences in results are caused by the tested security features rather than inconsistent test conditions.

---

## 4. Testing Levels

### 4.1 Unit Testing

Individual components will be tested independently.

Examples:
- Signature verification.
- Nonce validation.
- Risk-score calculation.
- Behavioural feature extraction.
- Hash-chain generation.
- Forensic verification.
- Transaction invariant validation.

### 4.2 Integration Testing

Multiple components will be tested together.

Examples:
- Gateway to identity verification.
- Gateway to risk assessment.
- Risk engine to adaptive response controller.
- Gateway to real blockchain.
- Gateway to decoy blockchain.
- Forensic service to database.

### 4.3 System Testing

The complete BLACKVEIL prototype will be tested using simulated participants and controlled attack scenarios.

The objective is to evaluate the complete request lifecycle, from authentication to transaction validation, response selection and forensic recording.

### 4.4 Failure Testing

Individual components will be deliberately made unavailable in the isolated test environment.

The objective is to verify that component failures do not create unrestricted access to the real blockchain.

---

## 5. Test Configurations

Four configurations will be used to compare the contribution of different security mechanisms.

| Configuration | Enabled Features | Purpose |
|---|---|---|
| C0 | Baseline blockchain without BLACKVEIL behavioural defence | Establish baseline performance |
| C1 | Rule-based detection | Evaluate hard rules and threshold-based detection |
| C2 | Rules + behavioural model + drift detection, with restriction but no diversion | Evaluate detection without deception |
| C3 | Full BLACKVEIL system with adaptive response and decoy diversion | Evaluate the complete architecture |

This comparison helps identify the contribution of behavioural analysis, adaptive response and deception.

---

## 6. Functional Test Scenarios

### TS-01: Valid Participant Authentication

**Objective:** Verify that legitimate participants can authenticate.

**Test procedure:**
1. Register a simulated participant.
2. Generate a valid Ed25519 key pair.
3. Submit a correctly signed request.
4. Verify the participant identity.

**Expected result:** The valid participant is authenticated and permitted to continue through normal security checks.

### TS-02: Invalid Credential Rejection

**Objective:** Verify that invalid credentials are rejected.

**Test procedure:**
1. Submit a request with an invalid signature.
2. Observe the gateway response.
3. Check the forensic event record.

**Expected result:** The request is rejected and the security event is recorded.

### TS-03: Stolen-Credential Behaviour Simulation

**Objective:** Evaluate detection of suspicious activity performed under an otherwise valid identity.

**Test procedure:**
1. Establish a normal activity baseline for a simulated participant.
2. Use the same test identity in a controlled suspicious-activity simulation.
3. Generate activity that deviates from its established baseline.
4. Observe behavioural features and risk-score changes.
5. Verify the selected response.

**Expected result:** BLACKVEIL identifies the behavioural deviation and applies an appropriate adaptive response.

### TS-04: Suspicious Operation Sequence

**Objective:** Verify operation-sequence analysis.

**Test procedure:**
1. Generate a normal sequence of permitted operations.
2. Introduce a different sequence in the simulation.
3. Compare the sequence-surprise feature.
4. Observe its contribution to the risk score.

**Expected result:** Unusual operation sequences contribute to increased risk assessment.

### TS-05: Slow-and-Low Behaviour

**Objective:** Evaluate the ability to identify gradual behavioural changes.

**Test procedure:**
1. Generate normal activity over multiple observation windows.
2. Gradually change the simulated activity pattern.
3. Observe EWMA and CUSUM behaviour.
4. Compare the resulting risk score with the baseline.

**Expected result:** Cumulative behavioural drift is identified even when individual activity windows do not contain obvious spikes.

### TS-06: Risk-Level Transition

**Objective:** Verify adaptive response selection.

**Test procedure:**
1. Generate simulated activity associated with different risk levels.
2. Observe risk-score calculations.
3. Verify the selected response level.
4. Evaluate anti-flapping behaviour during score fluctuations.

**Expected result:** BLACKVEIL applies Observe, Challenge, Restrict and Divert according to the configured thresholds and transition rules.

### TS-07: Decoy Diversion

**Objective:** Verify that eligible high-risk sessions are redirected to the decoy.

**Test procedure:**
1. Generate a controlled high-risk session.
2. Allow the risk engine to evaluate the session.
3. Verify the diversion decision.
4. Confirm that the session interacts with the decoy environment.
5. Verify that decoy activity does not modify the real ledger.

**Expected result:** The eligible session is directed to the isolated decoy, and the real blockchain remains protected.

### TS-08: Transaction Guardian Validation

**Objective:** Verify independent transaction validation.

**Test procedure:**
1. Submit a valid transaction in the simulation.
2. Submit a transaction with an invalid signature or replayed nonce.
3. Submit a transaction that violates a configured application invariant.
4. Observe transaction guardian decisions.

**Expected result:** Valid transactions satisfying all configured checks may proceed. Invalid transactions are rejected.

### TS-09: Forensic Integrity Verification

**Objective:** Verify the integrity of security evidence.

**Test procedure:**
1. Generate multiple security events.
2. Store them in the forensic event chain.
3. Verify the hash chain and signatures.
4. In an isolated test copy, modify a stored event.
5. Run the forensic verification process.

**Expected result:** The original evidence passes verification, while the modified evidence produces an integrity failure.

### TS-10: Threat Intelligence Policy Update

**Objective:** Verify controlled policy improvement.

**Test procedure:**
1. Introduce a candidate threat indicator into the test environment.
2. Evaluate it against known benign and suspicious traces.
3. Perform shadow testing.
4. Review its false-positive impact.
5. Simulate analyst approval and policy versioning.

**Expected result:** Candidate indicators do not become active policies without the required validation and approval.

---

## 7. Security and Failure Test Scenarios

### TS-11: Gateway Failure

**Objective:** Verify that gateway failure does not create a security bypass.

**Expected result:** Requests cannot directly access the real blockchain when the gateway is unavailable.

### TS-12: Risk Engine Failure

**Objective:** Verify safe behaviour when risk assessment is unavailable.

**Expected result:** Protected write operations fail closed or remain restricted.

### TS-13: Decoy Failure

**Objective:** Verify behaviour when the decoy becomes unavailable.

**Expected result:** Suspicious sessions remain restricted or quarantined. They are not automatically returned to the real blockchain.

### TS-14: Forensic Storage Failure

**Objective:** Verify that evidence is not silently discarded.

**Expected result:** Events are placed in a bounded protected buffer, and protected operations are restricted if evidence integrity cannot be maintained.

### TS-15: Dashboard Failure

**Objective:** Verify that security enforcement does not depend on dashboard availability.

**Expected result:** Gateway enforcement and transaction validation continue even if the dashboard is unavailable.

### TS-16: Consensus-Critical Participant

**Objective:** Verify the special handling of consensus-critical participants.

**Expected result:** Consensus-critical participants are never automatically diverted. Suspicious activity results in restriction and human escalation.

---

## 8. Performance Evaluation

The following metrics will be measured.

| Metric | Description | Target |
|---|---|---|
| Detection Rate | Percentage of simulated malicious sessions correctly identified | >= 90% |
| False Positive Rate | Percentage of benign sessions incorrectly classified as suspicious | <= 5% |
| Median Containment Time | Time between detection and effective restriction or diversion | < 5 seconds |
| Invalid Real-Chain Commits | Invalid or malicious transactions committed to the real ledger | 0 |
| Gateway p95 Latency | 95th-percentile gateway processing latency | < 15 ms |
| Throughput Loss | Throughput reduction compared with the baseline | < 10% |
| Decoy Distinguishability | Percentage of defined fidelity probes that distinguish the decoy from the reference environment | <= 10% |

These are prototype evaluation targets, not guaranteed production performance figures.

---

## 9. Evaluation Methodology

### 9.1 Detection Rate

Detection rate measures how many simulated malicious sessions BLACKVEIL correctly identifies.

Detection Rate = (True Positives / Total Actual Malicious Sessions) × 100

### 9.2 False Positive Rate

False positive rate measures how many legitimate sessions are incorrectly flagged.

False Positive Rate = (False Positives / Total Actual Benign Sessions) × 100

### 9.3 Containment Time

Containment time measures the elapsed time between identifying a suspicious session and successfully applying the required restriction or diversion.

### 9.4 Gateway Latency

Gateway latency measures the time taken to process a request through the gateway's security checks.

The 95th percentile is used to understand the experience of slower requests rather than relying only on average latency.

### 9.5 Throughput Loss

Throughput loss compares the number of requests processed per second with and without BLACKVEIL.

### 9.6 Decoy Distinguishability

A predefined set of fidelity probes will compare observable properties of the decoy and reference environment.

The evaluation will consider:
- Block-time regularity.
- Hash linkage.
- Response latency.
- Balance representation.
- Error-message consistency.

The target is to keep the percentage of probes that distinguish the decoy at or below 10%.

---

## 10. Result Recording

Each experiment will record:

- Test scenario ID.
- Configuration ID.
- Random seed.
- Number of benign sessions.
- Number of simulated malicious sessions.
- Detection results.
- False positives.
- Risk-score history.
- Response transitions.
- Containment time.
- Gateway latency.
- Throughput.
- Real-ledger integrity results.
- Forensic verification results.
- Decoy fidelity results.

Results will be stored in a structured format for comparison and analysis.

Each configuration will be evaluated across 10 runs using fixed, documented random seeds.

Where appropriate, results will include confidence intervals and a discussion of failures or unexpected outcomes.

---

## 11. Acceptance Criteria

The prototype will be considered to have met its core testing objectives when:

1. Valid and invalid identities are handled correctly.
2. The risk engine identifies the defined suspicious behaviour scenarios.
3. Adaptive response levels operate according to the configured rules.
4. Eligible high-risk sessions can be redirected to the isolated decoy.
5. The decoy cannot modify or directly access the real blockchain.
6. The transaction guardian rejects invalid transactions.
7. Forensic verification identifies modified evidence.
8. Component failures do not silently bypass security enforcement.
9. Evaluation results are reproducible and documented.
10. Performance and detection targets are measured and reported honestly.

Failure to meet a numerical target will be documented and investigated rather than hidden.

---

## 12. Limitations of Testing

The evaluation uses a local simulated environment.

Therefore:
- Results do not prove production-scale performance.
- Eight simulated participants do not represent hundreds of distributed nodes.
- Synthetic attack scenarios cannot represent every real attacker behaviour.
- Decoy fidelity tests cannot guarantee that an experienced attacker will never identify the decoy.
- Performance results depend on the development machine and test configuration.

Further evaluation would be required before deployment in a real permissioned blockchain network.

---

## 13. Conclusion

This test plan establishes a repeatable method for evaluating PROJECT BLACKVEIL.

It covers authentication, behavioural detection, adaptive response, decoy isolation, transaction integrity, forensic verification, failure handling and performance.

The evaluation will determine whether the prototype can demonstrate its central objective:

Protecting the real blockchain by identifying suspicious behaviour, applying adaptive defence and using isolated deception without compromising ledger integrity.
