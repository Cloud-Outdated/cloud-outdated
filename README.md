# cloud-outdated
Service that tracks cloud products versions and releases

## Zappa Django + periodic tasks

Please note that this is using my local AWS credentials and deploying in my personal AWS account.
The code is that matters here.

## Deploy process

- `pip install -r requirements.txt`
- `python manage.py collectstatic`
- `zappa deploy dev` for new deploy
- `zappa update dev` for updates

## Testing

- tested
    - use Zappa to deploy django app - test single view and template
        - https://b4eu57c6a2.execute-api.eu-central-1.amazonaws.com/dev & https://b4eu57c6a2.execute-api.eu-central-1.amazonaws.com/dev/about/
    - use Zappa with [whitenoise](http://whitenoise.evans.io/en/stable/)
        - https://b4eu57c6a2.execute-api.eu-central-1.amazonaws.com/dev/admin/
        - for staticfiles to work:
            - see `STATIC_X` settings in `settings.py`
            - run locally `./manage.py collectstatic` and then deploy
    - call Zappa _event_ (periodi task)
        - see `zappa_settings.json -> dev.events.0.function`
        - can be seen that it is running using `zappa tail dev` command
- not tested
    - RDS connection
        - there might be some issues with psycopg2 driver
