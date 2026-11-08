# Lambda Security Containment Simulation

[security_containment.py](security_containment.py) is a **reconstruction of the verified lab handler**, based on the implementation used in Project 3. It has not been fetched directly from AWS for byte-for-byte comparison.

## Runtime and entry point

- Language: Python
- AWS SDK: `boto3`
- Handler: `security_containment.lambda_handler` if deployed using this filename
- Deployed lab function name: `BonTech_Project3_Security_Containment`

## Environment variables

| Variable | Example / guidance |
|---|---|
| `DRY_RUN` | `true` |
| `APPROVED_INSTANCE_IDS` | Comma-separated EC2 IDs; use your own current test instances |
| `QUARANTINE_SG_ID` | A quarantine SG ID in the expected VPC |
| `SNS_TOPIC_ARN` | ARN of the alert topic in your account |

**Do not paste real account IDs, private email addresses, or credentials into the public repository.**

## How it works

1. Read an instance ID from a custom event or GuardDuty event.
2. Reject unapproved IDs and publish an SNS alert.
3. For approved IDs, read EC2 instance and security-group metadata.
4. Confirm the quarantine SG and instance are in the same VPC.
5. Return `SIMULATION_ONLY` or `CONTAINMENT_BLOCKED`; log the result.

## Limitations

- The function does not quarantine any EC2 instance.
- `DRY_RUN` does not toggle a live containment action; **no mutation path exists** in this code.
- Missing or malformed instance IDs raise an error rather than being handled by a dedicated error-notification path.
- The current lab logic does not independently validate finding severity, age, account, region, tags, or GuardDuty finding ID.
- The approved-instance path returns a log result; SNS publishing in this reconstruction occurs on rejection, not on every validation result.

Production automation would require separate design, testing, IAM review, and approval.
