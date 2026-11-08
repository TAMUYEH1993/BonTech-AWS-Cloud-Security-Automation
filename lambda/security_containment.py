"""BonTech Project 3 — AWS Lambda security response simulation.

Reconstructed from the implementation verified during the lab.
This is a portfolio reference, not an exported byte-for-byte copy of the deployed function.

Required environment variables:
  SNS_TOPIC_ARN, QUARANTINE_SG_ID, APPROVED_INSTANCE_IDS, DRY_RUN=true

Security: This function does NOT modify EC2 security groups.
"""
import json
import os

import boto3

ec2 = boto3.client("ec2")
sns = boto3.client("sns")


def send_security_alert(subject, message):
    response = sns.publish(
        TopicArn=os.environ["SNS_TOPIC_ARN"],
        Subject=subject,
        Message=json.dumps(message, indent=2),
    )
    print("SNS notification published:", response["MessageId"])
    return response["MessageId"]


def lambda_handler(event, context):
    dry_run = os.environ.get("DRY_RUN", "true").lower() == "true"
    quarantine_sg = os.environ["QUARANTINE_SG_ID"]
    approved_instances = {
        item.strip()
        for item in os.environ.get("APPROVED_INSTANCE_IDS", "").split(",")
        if item.strip()
    }

    instance_id = event.get("instance_id")
    if not instance_id:
        detail = event.get("detail", {})
        instance_id = detail.get("instance_id")
        if not instance_id:
            resource = detail.get("resource", {})
            instance_id = resource.get("instanceDetails", {}).get("instanceId")

    if not instance_id:
        raise ValueError("Missing instance_id")

    if instance_id not in approved_instances:
        result = {
            "instance_id": instance_id,
            "approved": False,
            "dry_run": dry_run,
            "action": "CONTAINMENT_REJECTED",
            "message": "Instance is not on the approved containment list. No changes made.",
        }
        print(json.dumps(result))
        send_security_alert(
            subject="BonTech - Containment Request Rejected",
            message=result,
        )
        return {"statusCode": 403, "body": json.dumps(result)}

    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response["Reservations"][0]["Instances"][0]
    instance_vpc = instance["VpcId"]
    current_sgs = [group["GroupId"] for group in instance["SecurityGroups"]]

    quarantine_vpc = ec2.describe_security_groups(
        GroupIds=[quarantine_sg]
    )["SecurityGroups"][0]["VpcId"]

    vpc_match = instance_vpc == quarantine_vpc
    result = {
        "instance_id": instance_id,
        "approved": True,
        "instance_vpc": instance_vpc,
        "quarantine_vpc": quarantine_vpc,
        "vpc_match": vpc_match,
        "current_security_groups": current_sgs,
        "quarantine_security_group": quarantine_sg,
        "dry_run": dry_run,
        "action": "SIMULATION_ONLY" if vpc_match else "CONTAINMENT_BLOCKED",
        "message": (
            "Validation passed. No changes made."
            if vpc_match
            else "VPC mismatch. Containment blocked."
        ),
    }
    print(json.dumps(result))
    return {
        "statusCode": 200 if vpc_match else 400,
        "body": json.dumps(result),
    }


# IMPORTANT:
# DRY_RUN is a reporting flag in this reference implementation.
# No containment mutation is performed even if DRY_RUN is set to false.
# Production response requires a separate, reviewed design.
