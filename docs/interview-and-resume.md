# Resume and Interview Preparation

## Resume-ready project bullets

- Architected a two-Availability Zone AWS security lab using public/private VPC subnets, private EC2 application instances, an Application Load Balancer, Auto Scaling, security groups, and AWS Systems Manager access.
- Integrated Amazon GuardDuty, EventBridge, Lambda, CloudWatch, and SNS to validate a sample-finding detection-to-notification workflow, including allowlist-based rejection of unapproved synthetic resources.
- Tested application reachability, Auto Scaling recovery, EventBridge routing, Lambda logging, and SNS email delivery; maintained dry-run-only response logic to avoid unapproved EC2 changes.

## Questions and suggested answer themes

### Why use private EC2 subnets behind an ALB?

The ALB accepts public application traffic, while private EC2 servers are not directly internet-addressable. Security groups restrict incoming application traffic to the ALB's security group.

### Why use multiple Availability Zones?

To reduce dependence on a single AZ and give the ASG more placement and recovery options. An ASG can launch replacement instances when capacity is lost.

### What is the role of NAT?

A NAT gateway provides outbound internet access for private subnet workloads when configured with appropriate routes, without enabling internet-initiated inbound connections to those instances.

### Why does EventBridge filter GuardDuty events?

Filtering routes only selected categories of findings to response automation. This project matched GuardDuty finding events for EC2 `Instance` resources.

### Why use a Lambda allowlist?

It rejects requests targeting unapproved instance IDs rather than acting on arbitrary IDs found in input events. For production, an allowlist is not enough: validate account, region, finding authenticity, resource ownership, severity, and freshness.

### Why is live quarantine risky for ASG-managed instances?

If quarantine prevents application health checks from succeeding, the ASG may replace the instance. This could remove forensic evidence unless containment is coordinated with ASG behavior and evidence-preservation controls.

### Did this project automatically isolate a compromised instance?

**No.** The project verified synthetic GuardDuty finding delivery, safe Lambda rejection, CloudWatch logs, and SNS notification. Live EC2 security-group modification was intentionally not enabled.

## Portfolio discussion summary

“I built a multi-AZ AWS cloud security lab and verified the detection-to-notification pipeline from a GuardDuty sample finding through EventBridge and Lambda to CloudWatch and SNS. The Lambda was restricted to dry-run validation, which allowed me to demonstrate authorization controls safely and explain the additional safeguards required before production containment.”
