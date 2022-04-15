from loguru import logger
import requests
import typer
import boto3


app = typer.Typer()

@app.command()
def bell(webhook_url):
    response = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
    instance_id = response.text

    ec2 = boto3.client('ec2')
    response = ec2.describe_tags(
        Filters=[
            {"Name": "resource-id", "Values": [instance_id]},
        ]
    )
    ec2_instance_name = response["Tags"][0]["Value"]
    logger.debug(f"ec2 instance name: {ec2_instance_name}")
    
    response = ec2.describe_instance_status(
        InstanceIds=[instance_id]
    )
    status = response["InstanceStatuses"][0]["InstanceState"]["Name"]
    logger.debug(f"ec2 instance status: {status}")
    
    response = requests.post(webhook_url, json={"text": f":bell: {ec2_instance_name} is {status}"})
    logger.debug(f"slack response code: {response.status_code}")

if __name__ == "__main__":
    app()
