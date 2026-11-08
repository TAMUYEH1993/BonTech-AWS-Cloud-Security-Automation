# Screenshots — Evidence Publishing Guide

Only publish screenshots after redacting any sensitive or identifying information.

## Recommended evidence

1. VPC overview and public/private subnet layout.
2. ALB listener and target group showing healthy targets.
3. Auto Scaling Group showing two instances across AZs.
4. GuardDuty sample finding (without any account identifiers).
5. EventBridge rule name and target.
6. CloudWatch metric confirming EventBridge invocation.
7. Lambda CloudWatch log demonstrating a dry-run rejection.
8. SNS email alert with the recipient and any unsubscribe or subscription links redacted.

## Redaction requirements

Remove AWS account numbers, email addresses, subscription/unsubscribe links, tokens, ARNs with account IDs, credential material, personal information, internal organizational information, and other sensitive values. Ensure screenshot filenames are neutral.

Use labels such as `01-vpc-overview.png` and `07-lambda-dry-run-log.png`. Include a brief caption in [../docs/test-evidence.md](../docs/test-evidence.md) if you upload screenshots.

No screenshots are included yet.
