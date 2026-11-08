# Security Controls and Engineering Decisions

## Implemented and verified controls

| Control | How it was applied | Purpose |
|---|---|---|
| VPC network segmentation | Separate public and private subnets over two AZs | Reduce direct exposure of application servers |
| Security-group source restriction | EC2 application HTTP inbound from the ALB security group | Prevent general internet access to EC2 web ports |
| No public EC2 IPs | Application instances placed in private subnets | Reduce exposed attack surface |
| Controlled outbound connectivity | NAT gateway for private subnet egress | Enable updates without public inbound routes |
| Managed administration | EC2 IAM role for AWS Systems Manager | Avoid public SSH |
| High availability | ASG desired capacity 2, distributed across AZs | Replace failed or terminated compute |
| Threat detection | Amazon GuardDuty enabled | Surface security findings |
| Event filtering | EventBridge GuardDuty rule matches EC2 `Instance` findings | Route selected findings to automation |
| Allowlist validation | Lambda requires explicit approved instance ID | Reject unexpected containment requests |
| VPC match verification | Lambda checks selected instance and quarantine SG VPC IDs | Prevent cross-VPC mistakes |
| Dry run | `DRY_RUN=true` and no EC2 modification API | Preserve application availability during testing |
| Logging | CloudWatch Lambda logs | Auditable execution and troubleshooting |
| Alerting | Amazon SNS email | Notify on rejected containment requests |

## Tested behavior

- Successful ALB application access.
- Successful Auto Scaling instance replacement.
- Successful EventBridge custom simulation, including an unapproved instance rejection.
- GuardDuty-generated sample EC2 finding matched the GuardDuty rule, invoked Lambda, generated a CloudWatch log, and delivered an SNS email notification.

## Important limitations

1. No evidence of a real threat actor or compromised EC2 instance; the GuardDuty test used a synthetic sample finding.
2. **No live containment occurred.** Lambda does not call `ec2:ModifyInstanceAttribute` or alter security group membership.
3. The allowlist alone is insufficient for production authorization. Add finding source/account/region verification, freshness, severity thresholds, resource ownership checks, and manual approval where appropriate.
4. The project does not claim complete production hardening, formal compliance certification, or proof of WAF effectiveness.
5. A production deployment should establish log retention, monitoring thresholds, retry/dead-letter handling, least-privilege policy review, change control, incident playbooks, and evidence preservation.

## Recommended next phase (outside Project 3 scope)

Plan, test, and authorize a distinct live-containment design in an isolated environment with forensic safeguards and special treatment for ASG-managed instances. This is a future enhancement, not a requirement for the completed lab.
