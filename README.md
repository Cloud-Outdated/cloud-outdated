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
docker compose exec django pytest .
```

or if you use zsh and oh my zsh with docker compose plugin:

```
dce django pytest .
```

## Deploy process

- `pip install -r requirements.txt`
- `python manage.py collectstatic`
- `zappa deploy dev` for new deploy
- `zappa update dev` for updates

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
zappa certify <env>
```

to configure API Gateway to honor the domain name specified. Changes can take up to 40 minutes to get applied.

### CockroachDB

CockroachDB database needs to be created manually since there is no terraform provider for it.

- go to [cockroachlabs.cloud](https://cockroachlabs.cloud/clusters) and create a cluster for the environment
- get connection info and store it to SSM
