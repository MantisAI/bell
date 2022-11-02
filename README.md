# 🛎 Bell

A tool to send you alerts from your AWS instances

# Quickstart

Install

```
pip install git+https://github.com/MantisAI/bell.git@main
```

Use bell 🛎  to get alerts that your AWS instance is on

```
bell --webhook-url SLACK_WEBHOOK_URL
```

Use bell 🛎  to get alerts about when a command starts, fails or finishes

```
export SLACK_WEBHOOK_URL=xxx

bell python -c "print('hello')"
```

Note that you can pass the slack webhook URL either as a command line parameter
`--webhook-url` or as an environment variable `SLACK_WEBHOOK_URL`

You can capture the output of the process by passing the `--capture-output`
option. This will then get printed to slack.

```
bell --cpature-output python -c "print('hello')"
```

The results will be printed in slack as:

:bellhop_bell: command python -c print('hello') started :rocket:
```
hello
```
:bellhop_bell: command python -c print('hello') finished :boom:


You can read how to setup a slack webbook [here](https://api.slack.com/incoming-webhooks)


# Cron

This tool works well with a scheduler like cron. Here is an example cron
command which sends an alert every 2 hours

```
SLACK_WEBHOOK_URL=xxx

0 */2 * * * bell
```

Note that cron's environment is different to your user or root environment. See troubleshooting
if you have problems setting up bell to work with cron.

# CLI

```
usage: bell [-h] [--webhook-url WEBHOOK_URL]

optional arguments:
  -h, --help            show this help message and exit
  --webhook-url WEBHOOK_URL
                        incoming slack webhook url
```

# Troubleshooting

## Logs

By default bell sets the logging level at INFO. For debugging purposes, it is more helpful
to set it at DEBUG. You can do that via the environment variable `LOGGING_LEVEL` by running
```
export LOGGING_LEVEL=DEBUG
```

## Bell works when run manually but not through cron

In order for cron to work it needs to have access to both bell, python packages and AWS
credentials. For this reason we recommend you install a cron job under your user account
and not root, otherwise you might need to install the tool with sudo and ensure root has
access to AWS credentials.

Even in that case as it turns out cron has a different more minimal PATH
than what you see in the terminal if you run `echo $PATH`. For that reason, you should
probably define the same PATH in your cron job as the one you see when you test the
tool.

## Region not specified

We assume you have AWS credentials setup either through environment variables, aws configure
or proper IAM roles. We use boto under the hood to query AWS, see its documentation around
credentials [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
