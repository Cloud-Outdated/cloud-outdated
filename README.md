# cloud-outdated
Service that tracks cloud products versions and releases

## Local Development

Requires docker, docker-compose and make

Commands:
- `make start`, to start server
- `make stop`, to stop server
- `make rebuild`, to rebuild docker images
- `make destroy`, to stop server and delete volumes

### Testing

Tests are run within the Docker container.

```
docker-compose exec django pytest .
```

or if you use zsh and oh my zsh with docker compose plugin:

```
dce django pytest .
```

## Deploy process

Regular deployment is done through Github Actions. 

Everything that lands in `master` is deployed to `dev` environment available at [dev.cloud-outdated.com](https://dev.cloud-outdated.com).

To deploy to `prod` available at [cloud-outdated.com](https://cloud-outdated.com) open a pull request from `master` to `prod`.

## Zappa

In special circumstances, such as initial deployment, it can also be done from local machine. aws-vault and an admin user is required for it.

Before running any `zappa` commands locally through `aws-vault` comment out `profile_name` key from `zappa_settings.json` for the deploy environment on which you are currently working on.

- `pip install -r requirements.txt`
- `python manage.py collectstatic`
- `aws-vault exec cloud-outdated-x -- zappa deploy dev` for new deploy
- `aws-vault exec cloud-outdated-x -- zappa update dev` for updates

## Infrastructure

Infrastructure is managed via Terraform and [Terraform Cloud](https://app.terraform.io/) is used as the executor.

There are two workspaces: `dev` and `prod`.

Use aws-vault and an admin user to switch to desired workspace and apply changes:

```
aws-vault exec cloud-outdated-x -- terraform workspace select dev
aws-vault exec cloud-outdated-x -- terraform apply
```

### Zappa config from infra changes

After terraform changes have been applied `zappa_settings.json` file can be populated with appropriate values.

After `zappa_settings.json` is populated run locally:

```
aws-vault exec cloud-outdated-x -- zappa certify <env>
```

to configure API Gateway to honor the domain name specified. Changes can take up to 40 minutes to get applied.

### CockroachDB

CockroachDB database needs to be created manually since there is no terraform provider for it.

- go to [cockroachlabs.cloud](https://cockroachlabs.cloud/clusters) and create a cluster for the environment
- get connection info and store it to SSM

### New Relic

Single installation per account, not per deploy env.

- install [New Relic' Lambda CLI tool](https://github.com/newrelic/newrelic-lambda-cli#installation) in your venv
    - `pip install newrelic-lambda-cli`
- install New Relic integration for all Lambdas in account
    - `aws-vault exec cloud-outdated-x --no-session -- newrelic-lambda integrations install --nr-account-id 3438061 --nr-api-key {REDACTED - SEE aws_ssm_parameter.new-relic-api-key} --nr-region eu`
    - `aws-vault exec cloud-outdated-x --no-session -- newrelic-lambda layers install -f all --nr-account-id 3438061 --nr-api-key {REDACTED - SEE aws_ssm_parameter.new-relic-api-key} --nr-region eu --enable-extension-function-logs --aws-region eu-central-1`


### Adding/updating scrapped service

When adding or updating a service whose versions are fetched by using webscrapping, make sure to also update the source_url in the service definition located in `services/base.py`
