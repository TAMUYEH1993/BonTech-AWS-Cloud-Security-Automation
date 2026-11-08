# Test Evidence and Results

**Final integration test date:** November 8, 2026  
**AWS region:** `us-east-1`

## Test summary

| ID | Validation | Outcome | Evidence type |
|---|---|---|---|
| T01 | Public ALB serves Apache application from private EC2 | Passed | Earlier browser and PowerShell results |
| T02 | Auto Scaling replaces a terminated instance | Passed | AWS console / instance replacement history |
| T03 | Custom EventBridge simulation invokes Lambda | Passed | PutEvents result and CloudWatch Lambda log |
| T04 | Unapproved instance rejected and SNS published | Passed | CloudWatch and earlier email notification |
| T05 | GuardDuty generates sample EC2 finding | Passed | CloudShell `create-sample-findings` returned without error |
| T06 | GuardDuty EventBridge rule invokes target | Passed | `AWS/Events` `Invocations` metric: `Sum=1.0` at `2026-11-08T19:32:00Z` |
| T07 | Lambda handles finding | Passed | CloudWatch log of rejected synthetic instance |
| T08 | SNS delivery to inbox | Passed | Corresponding Gmail message at 2:32 PM ET |
| T09 | Live EC2 quarantine | Not performed | Intentionally excluded from simulation-only scope |

## Final GuardDuty event validation

### Finding generation

```bash
DETECTOR_ID=$(aws guardduty list-detectors --region us-east-1 --query 'DetectorIds[0]' --output text)
aws guardduty create-sample-findings --region us-east-1 --detector-id "$DETECTOR_ID" --finding-types "UnauthorizedAccess:EC2/SSHBruteForce"
```

### EventBridge invocation evidence

An `AWS/Events` `Invocations` CloudWatch query for the GuardDuty findings rule returned a positive sample:

```json
{
  "Timestamp": "2026-11-08T19:32:00+00:00",
  "Sum": 1.0,
  "Unit": "Count"
}
```

### Lambda validation evidence

The CloudWatch Lambda log recorded a rejection for a synthetic instance ID:

```json
{
  "instance_id": "i-99999999",
  "approved": false,
  "dry_run": true,
  "action": "CONTAINMENT_REJECTED",
  "message": "Instance is not on the approved containment list. No changes made."
}
```

The same execution reported an SNS message publication. The matching email was received.

### What this proves

The GuardDuty sample finding was processed by EventBridge and Lambda, and the rejection notification was delivered. This is an **end-to-end sample-finding detection, validation, logging, and alerting test**.

### What this does not prove

It does not establish a real intrusion, successful isolation of a real EC2 instance, production-readiness, or the security impact of an actual quarantine action.

## Screenshot publishing checklist

Before uploading any screenshots to this **public** repository:

- [ ] Remove AWS account numbers, email addresses, personal identifiers, access keys, and session details.
- [ ] Remove SNS subscription / unsubscribe links and any secret URLs.
- [ ] Keep the service name, timestamp, metric name, outcome, and sanitized log message visible.
- [ ] Add a short caption explaining the evidence.
- [ ] Do not publish any sensitive console configuration values or internal organizational details.

Screenshots are **not yet published** to this repository.
