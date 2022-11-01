from socket import timeout
import urllib.request
import subprocess
import logging
import argparse
import json
import sys
import os

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(funcName)20s:%(lineno)s - %(message)s",
    level=os.environ.get("LOGGING_LEVEL", logging.INFO),
)
logger = logging.getLogger(__name__)


def get_status_message():
    try:
        response = urllib.request.urlopen(
            "http://169.254.169.254/latest/meta-data/instance-id", timeout=5
        )
        instance_id = response.read().decode("utf-8")

        response = urllib.request.urlopen(
            "http://169.254.169.254/latest/meta-data/public-hostname", timeout=5
        )
        public_hostname = response.read().decode("utf-8")
    except urllib.request.URLError:
        logger.debug(
            "Metadata request timed out. You are probably not in an AWS instance."
        )
        return ":bellhop_bell: local mode"

    try:
        import boto3
    except ImportError:
        return f":bellhop_bell: {public_hostname} is running"

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


def send_slack_message(webhook_url, message):
    logger.debug(f"slack message: {message}")

    data = json.dumps({"text": message}).encode("utf-8")

    request = urllib.request.Request(webhook_url)
    request.add_header("Content-Type", "application/json; charset=utf-8")
    request.add_header("Content-Length", len(data))

    try:
        response = urllib.request.urlopen(request, data, timeout=5)
        logger.debug(f"slack response code: {response.getcode()}")
    except urllib.request.URLError:
        logger.error(
            "slack message not sent. probably timeout. this is normal if you are testing or running locally."
        )


def bell(webhook_url, capture_output=False, *command):
    if command:
        logger.debug(f"command: {command}")
        try:
            if not capture_output:
                send_slack_message(
                    webhook_url,
                    f":bellhop_bell: command `{' '.join(command)}` started :rocket:",
                )

            # Capture the result of the process so we can use it later

            result = subprocess.run(command, check=True, capture_output=capture_output)

            if capture_output:
                send_slack_message(
                    webhook_url,
                    f"```{result.stdout.decode('utf-8')}```",
                )

        except subprocess.CalledProcessError:
            logger.error("command failed")
            send_slack_message(
                webhook_url, f":bellhop_bell: command `{' '.join(command.stdout)}` failed :x:"
            )
            raise

        except AttributeError:
            logger.error("command failed")
            send_slack_message(
                webhook_url, f":bellhop_bell: command `{' '.join(command.stdout)}` failed :x:"
            )
            raise

        if not capture_output:
            send_slack_message(
                webhook_url, f":bellhop_bell: command `{' '.join(command)}` finished :boom:"
            )
    else:
        instance_status = get_status_message()
        send_slack_message(webhook_url, instance_status)


def cli():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--webhook-url",
        default=os.environ.get("SLACK_WEBHOOK_URL"),
        help="incoming slack webhook url",
    )
    argument_parser.add_argument(
        "--capture-output",
        action="store_true",
        help="capture output of command",
        default=False,
    )

    args, command_args = argument_parser.parse_known_args()

    if not args.webhook_url:
        print(
            "You need to pass a value for webhook url either through --webhook-url or as an environment variable SLACK_WEBHOOK_URL"
        )
        sys.exit(1)

    bell(args.webhook_url, args.capture_output, *command_args)


if __name__ == "__main__":
    cli()
