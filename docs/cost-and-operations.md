# Cost, Operations, and Cleanup

## Cost model

This project uses chargeable AWS infrastructure. **Do not assume the lab is free.** Exact charges depend on region, usage, free-tier eligibility, runtime, and current AWS pricing.

| Resource | Primary cost driver | Cost-reduction consideration |
|---|---|---|
| EC2 Auto Scaling instances | Running instance-hours and attached EBS storage | Stop or delete the lab after evidence capture; ASG may replace manually terminated instances |
| Application Load Balancer | ALB-hours and load balancer capacity units | Delete when the lab is no longer needed |
| NAT Gateway | Gateway-hours and data processed | Often a significant idle-lab cost; delete after private workloads no longer need it |
| Public IPv4 | Allocated/in-use public IPv4 addresses | Release unused Elastic IPs after deleting dependent resources |
| CloudWatch | Logs ingested/stored and metrics/alarms | Set reasonable retention and remove unneeded logs |
| GuardDuty | Monitored resources/events and enabled protection features | Review enabled coverage and disable lab-only protection if appropriate |
| SNS | Published notifications and delivery | Review topic/subscriptions |
| Data transfer | Internet and inter-AZ traffic | Minimize unnecessary traffic |

## Check actual spending

In the AWS Console:

1. Open **Billing and Cost Management**.
2. Open **Cost Explorer** and select the relevant time range.
3. Group by **Service**, filter the appropriate account and region as needed.
4. Review EC2, EC2-Other (including some networking charges), Elastic Load Balancing, CloudWatch, GuardDuty, and SNS.
5. Compare against **Bills** for billed charges. Cost Explorer data can be delayed.

If you continue using this lab, configure a budget alert and review costs regularly.

## Safe shutdown / teardown sequence

**Only perform this when you no longer need the running lab.** These steps are a checklist, not commands executed by this repository.

1. Export and sanitize the final evidence; preserve any logs required for the portfolio.
2. Confirm there are no active incidents or dependencies.
3. Delete or scale down the ASG as part of an intentional teardown; merely terminating its instances may cause automatic replacement.
4. Remove the ALB and target group after application validation is no longer required.
5. Remove NAT gateway and release associated Elastic IPs once dependent routes/workloads are retired.
6. Review and remove unused EC2 volumes, launch templates, security groups, and networking components in dependency order.
7. Delete or disable lab-only EventBridge rules, Lambda function, SNS topic/subscriptions, and GuardDuty configuration if no longer required.
8. Review CloudWatch log groups and retention settings.
9. Recheck Billing/Cost Explorer over subsequent days because reporting can lag.

**Warning:** Teardown is destructive and may permanently remove logs or other evidence. Confirm each dependency and retention requirement first.

## Operational readiness checklist

- [x] Test ALB access to private EC2 application
- [x] Test ASG instance replacement
- [x] Verify custom EventBridge simulation and Lambda response
- [x] Verify GuardDuty sample finding → EventBridge → Lambda
- [x] Verify CloudWatch log and SNS email
- [x] Maintain dry-run-only containment behavior
- [ ] Configure automated cost budget alerts (not verified)
- [ ] Define CloudWatch log retention policy (not verified)
- [ ] Add failed-invocation alarms and DLQ (not implemented)
- [ ] Plan and execute approved teardown when finished
