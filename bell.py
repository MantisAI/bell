import subprocess
import argparse
import os

from loguru import logger
import requests
import boto3


BELL_MODE = os.environ["BELL_MODE"]

def get_status_message():
    if BELL_MODE == "LOCAL":
        return ":bellhop_bell: local mode"

    response = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
    instance_id = response.text

    ec2 = boto3.client("ec2")
    response = ec2.describe_tags(
        Filters=[
            {"Name": "resource-id", "Values": [instance_id]},
        ]
    )
    ec2_instance_name = response["Tags"][0]["Value"]
    logger.debug(f"ec2 instance name: {ec2_instance_name}")

    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    status = response["InstanceStatuses"][0]["InstanceState"]["Name"]
    logger.debug(f"ec2 instance status: {status}")
    return f":bellhop_bell: {ec2_instance_name} is {status}"


def send_slack_message(message):
    logger.debug(f"slack message: {message}")

    if BELL_MODE == "LOCAL":
        return

    response = requests.post(
        webhook_url, json={"text": message}
    )
    logger.debug(f"slack response code: {response.status_code}")


def bell(webhook_url, *command_args):
    if command_args:
        logger.debug(f"command: {command_args}")
        try:
            send_slack_message("command started")
            subprocess.run(command_args, check=True)
        except subprocess.CalledProcessError:
            logger.error("command failed")
            send_slack_message("command failed")
            raise

        send_slack_message("command finished")
    else:
        instance_status = get_status_message()
        send_slack_message(instance_status)


def cli():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--webhook-url", help="incoming slack webhook url")

    args, command_args = argument_parser.parse_known_args()
    logger.debug(f"args: {args}")
    logger.debug(f"command_args: {command_args}")

    bell(args.webhook_url, *command_args)


if __name__ == "__main__":
    cli()
