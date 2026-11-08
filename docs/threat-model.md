# Threat Model — BonTech Project 3

## Purpose and boundaries

This threat model evaluates the **hands-on lab architecture**, not a production-certified system. The public ALB is the entry point for application traffic; private EC2 instances serve the application. GuardDuty, EventBridge, Lambda, CloudWatch and SNS form the security-event workflow.

## Assets and trust boundaries

| Asset | Trust boundary | Security objective |
|---|---|---|
| Public ALB | Internet to AWS VPC | Accept only intended application traffic |
| Private EC2 instances | ALB to private application subnets | Prevent direct internet-originated access |
| EC2 IAM role / Systems Manager | AWS identity and management plane | Limit administrative access |
| GuardDuty findings | AWS security service to EventBridge | Preserve event origin and integrity |
| EventBridge rule | Detection plane to Lambda | Invoke only the intended automation |
| Lambda function | Untrusted event fields to AWS API access | Reject unauthorized actions |
| SNS topic and email | AWS account to external notification channel | Avoid leakage and alert abuse |
| CloudWatch logs | Runtime to audit/observability plane | Retain useful incident evidence |

## Threat scenarios (STRIDE-inspired)

| Threat | Impact | Existing lab mitigation | Residual gap / future control |
|---|---|---|---|
| Spoofed or malformed event fields | Unwanted automated action | Lambda allowlist and simulation-only behavior | Validate AWS event source, account, region, finding ID, age, severity, and resource tags before any action |
| Internet-originated direct access to EC2 | Workload compromise | Private subnets, no public IPs, application SG sourced from ALB SG | Periodic security group drift review and least-privilege egress |
| Overprivileged Lambda execution role | Escalation after Lambda compromise | Scoped SNS publishing; read-only EC2 inspection in tested code | Formal IAM review and access analysis |
| Application denial of service | Availability loss | ALB and multi-AZ ASG | Load testing, WAF policy validation, rate limiting, alarms, capacity review |
| ASG replacement during quarantine | Evidence loss | No live quarantine in this lab | Incident evidence snapshots, lifecycle strategy, explicit human approval |
| Missing or delayed event delivery | Missed response | EventBridge invocation metric and Lambda logs | DLQ/retry strategy, failure alarms, periodic end-to-end tests |
| Alert fatigue or malicious notification flood | Missed critical incidents | Explicit rejected-event notification | Severity thresholds, deduplication, rate limits, incident routing |
| Secrets or sensitive IDs published in GitHub | Information disclosure | Documentation excludes sensitive values | Review every commit and redact screenshots before publishing |

## Abuse-case walkthrough: synthetic GuardDuty finding

1. GuardDuty produces a **sample** EC2 SSH brute-force finding.
2. EventBridge matches the `aws.guardduty` source, `GuardDuty Finding` detail type, and EC2 `Instance` resource type.
3. Lambda extracts the synthetic instance ID `i-99999999`.
4. The ID is not approved, so Lambda returns `CONTAINMENT_REJECTED`.
5. Lambda writes a CloudWatch log and publishes an SNS email notification.
6. No EC2 security group is modified.

**Validated:** detection-to-notification with a synthetic sample.  
**Not validated:** live threat eradication, automated isolation of a real instance, or production attack resistance.

## Risk priorities for a future production design

1. **High:** Validate event provenance and target identity before allowing any EC2 mutation.
2. **High:** Prevent ASG lifecycle actions from destroying incident evidence.
3. **Medium:** Add failure alarms, retry handling, and a dead-letter queue for asynchronous delivery.
4. **Medium:** Establish log retention, immutable evidence handling, and incident ticket tracking.
5. **Medium:** Add web-layer protection and verify HTTPS/TLS configuration before production exposure.
