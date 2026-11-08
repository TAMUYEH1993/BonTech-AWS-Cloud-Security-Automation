# EventBridge Rules and Test Payloads

## GuardDuty rule

The deployed GuardDuty EventBridge rule was named `BonTech-Project3-GuardDuty-Findings-Rule`. Its verified event pattern is stored in [guardduty-ec2-finding-rule.json](guardduty-ec2-finding-rule.json). It filters:

- Source: `aws.guardduty`
- Detail type: `GuardDuty Finding`
- Resource type: `Instance`

Its target is the `BonTech_Project3_Security_Containment` Lambda function.

## Custom test rule

The deployed custom rule `BonTech-Project3-Security-Test-Rule` uses [custom-test-rule.json](custom-test-rule.json) and also targets Lambda.

The synthetic test event in [sample-custom-event.json](sample-custom-event.json) uses a **non-approved example instance ID** so the expected response is `CONTAINMENT_REJECTED`, with no EC2 changes.

To submit a custom event from this directory, use the correctly formatted **array** in [put-events-entries.json](put-events-entries.json):

```bash
aws events put-events --entries file://put-events-entries.json --region us-east-1
```

The [sample-custom-event.json](sample-custom-event.json) file shows one illustrative entry object, but the CLI `--entries` argument requires an array.

**Do not attempt to impersonate the AWS-reserved `aws.guardduty` source** with `put-events`; that can return `NotAuthorizedForSourceException`. For the final integration test, GuardDuty's own `create-sample-findings` API generated the finding.

## Final validated result

On November 8, 2026, a GuardDuty-generated EC2 sample finding triggered the GuardDuty rule, Lambda rejected the synthetic instance ID, CloudWatch logged the response, and SNS delivered the email. No live quarantine occurred.
