# IAM and Lambda Permissions

These files are **documented reference configurations**, not exact exports of the AWS account's live policies.

## Lambda execution role

The project used a Lambda execution role with an inline security automation policy permitting:

- `ec2:DescribeInstances` — inspect the target instance and VPC.
- `ec2:DescribeSecurityGroups` — inspect the quarantine security group's VPC.
- `sns:Publish` — publish alerts to the dedicated SNS topic.

The role also needs CloudWatch Logs permissions (typically supplied through `AWSLambdaBasicExecutionRole`) for creating log streams and writing logs.

The execution role's trust policy permits `lambda.amazonaws.com` to assume the role.

**No EC2 security group modification permission is included in the reference policy.** The Lambda is simulation-only.

## EventBridge permission to invoke Lambda

EventBridge does **not** assume the Lambda execution role to invoke the function. The Lambda function's **resource-based policy** permits the EventBridge service to invoke it, restricted by the specific rule ARN.

Example AWS CLI shape (placeholders are not real account values):

```bash
aws lambda add-permission \
  --function-name BonTech_Project3_Security_Containment \
  --statement-id AllowGuardDutyRuleInvoke \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn "arn:aws:events:REGION:ACCOUNT_ID:rule/BonTech-Project3-GuardDuty-Findings-Rule"
```

The lab verified a resource-based Lambda permission for both the GuardDuty rule and custom test rule. This command is documentation only; it has **not** been run as part of publishing this repository.

## Files

- [lambda-execution-policy.example.json](lambda-execution-policy.example.json): illustrative action and resource scope, with placeholders.
- [lambda-trust-policy.json](lambda-trust-policy.json): Lambda service trust policy.
- [../lambda/security_containment.py](../lambda/security_containment.py): reconstructed dry-run Lambda implementation.

Do not commit AWS account numbers, access keys, credentials, or policy exports containing sensitive internal resource identifiers.
