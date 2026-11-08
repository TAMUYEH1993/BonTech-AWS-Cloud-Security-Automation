# Validation Matrix

The table distinguishes **observed lab results** from **planned production controls**.

| Area | Test method | Observed result | Status |
|---|---|---|---|
| VPC segmentation | Console inspection of public/private subnets and routes | Segmented multi-AZ VPC | Verified |
| Application traffic | Browser/PowerShell requests to ALB | Apache response | Verified |
| Private compute | EC2 networking inspection | ASG-managed instances in private subnets | Verified |
| Recovery | Controlled instance termination | ASG launched replacement | Verified |
| Lambda permissions | IAM and resource-policy inspection | SNS publish scoped; EventBridge invoke permitted | Verified for tested scope |
| Custom EventBridge event | `aws events put-events` | Successful submission and Lambda execution | Verified |
| Allowlist rejection | Unapproved instance test | `CONTAINMENT_REJECTED` | Verified |
| GuardDuty sample event | `aws guardduty create-sample-findings` | Sample finding generated | Verified |
| GuardDuty rule invocation | CloudWatch `AWS/Events` `Invocations` | `Sum=1` at 19:32 UTC on Nov 8, 2026 | Verified |
| Lambda GuardDuty handling | CloudWatch execution logs | Synthetic instance rejected safely | Verified |
| SNS alert delivery | Email inbox | Notification received | Verified |
| Live quarantine | None | Not enabled | Not in lab scope |
| Real-world attack response | None | Not evaluated | Not in lab scope |
| Failure alarm / DLQ | None | Not demonstrated | Future enhancement |
| Infrastructure as Code | None in this project | AWS Console/CLI implementation | Future enhancement |
| Automated integration tests | Manual commands and screenshots | Manual verification | Future enhancement |

## Evidence integrity

For each published screenshot, record the test ID, timestamp, expected behavior, observed behavior, and whether the screenshot has been redacted. Avoid claims of production security assurance based only on sample findings.

## Acceptance criteria for the completed lab

1. Private application architecture responds through the ALB.
2. ASG recovery behavior is observed.
3. GuardDuty sample finding invokes the configured EventBridge target.
4. Lambda logs the expected rejection for an unapproved synthetic instance.
5. SNS publishes the alert and the email arrives.
6. No live EC2 security-group modification is claimed.

**All six acceptance criteria were met for the agreed lab scope.**
