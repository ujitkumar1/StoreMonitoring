from celery import Celery


def make_celery(app):
    celery = Celery(
        "app",
        backend=app.config['result_backend'],
        broker=app.config['CELERY_BROKER_URL'],
        timezone="Asia/Kolkata",
        enable_utc=False
    )

    # Configuring the flask app
    celery.conf.update(app.config)

    # Configuring the celery task
    celery.conf.imports = ('app.Task',)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
