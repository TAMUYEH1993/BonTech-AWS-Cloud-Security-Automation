# Incident Response Runbook

**Workflow:** GuardDuty → EventBridge → Lambda → CloudWatch → SNS  
**Scope:** Lab validation and safe investigation. No automatic EC2 isolation is enabled.

## Trigger

A GuardDuty finding for an EC2 `Instance` resource matches the EventBridge rule. A Lambda invocation may reject the target if its instance ID is not allowlisted.

## Triage procedure

### 1. Confirm the alert

Record the notification time, finding type, severity, resource type, instance ID, account and region (in a **private incident record**, not a public GitHub issue). Determine whether the event is a GuardDuty **sample** or a genuine finding.

### 2. Confirm event delivery

Use CloudWatch EventBridge metrics and Lambda logs. A positive `Invocations` metric indicates an invocation attempt, not necessarily successful downstream handling.

```bash
aws logs tail \
  "/aws/lambda/BonTech_Project3_Security_Containment" \
  --since 30m \
  --region us-east-1 \
  --format short
```

For historical evidence, use the appropriate timestamps and ensure the query window includes the incident.

### 3. Validate resource identity

Before any real action, independently verify the EC2 instance exists, belongs to the expected AWS account and VPC, and is owned by the relevant application team. Check finding provenance, age, type and severity. Synthetic IDs such as `i-99999999` must **never** be treated as real compromised hosts.

### 4. Preserve evidence

For a real suspected compromise, follow organizational incident procedures. Preserve relevant CloudTrail, VPC Flow Logs, GuardDuty findings, system logs, and disk evidence where configured. Coordinate snapshot and memory acquisition with responders; do not assume these logs or collection mechanisms are already enabled in the lab.

### 5. Assess Auto Scaling impact

An ASG-managed instance can be replaced if isolation breaks ALB health checks. Coordinate with the application owner before any health-check or lifecycle change. Avoid terminating or quarantining the instance until evidence-preservation steps are approved.

### 6. Decide response

| Finding | Lab response | Future production consideration |
|---|---|---|
| Sample finding / synthetic ID | Log, reject, notify | No containment |
| Missing or malformed ID | Log parsing failure, investigate | Reject and alert with safe error handling |
| Unapproved real instance | Reject and notify | Require human review |
| Approved instance with matching VPC | Validate in dry run | Additional provenance and incident authorization required |
| VPC mismatch | Block | Investigate configuration or targeting error |

### 7. Communicate and close

Document incident timeline, observed impact, finding validity, decisions, evidence locations, notification delivery, remediation owner, and follow-up actions. Never paste raw credentials, private logs, or personal email details into the public repository.

## Lab completion evidence

On November 8, 2026, the GuardDuty sample-finding workflow invoked Lambda, rejected synthetic instance `i-99999999` with `dry_run: true`, published SNS, and delivered an email. This proves the **sample detection-to-alert** workflow, not live quarantine.

## Escalation and rollback

No live EC2 mutation is part of this project, so there is no quarantine rollback to execute. A future live-response runbook must define approval, evidence preservation, safe SG restoration, health-check recovery, and validation of application availability **before** any containment capability is enabled.
