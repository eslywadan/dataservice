from celery import Celery

def make_celery(app):
    """ The function accepts flask app as an input, then a celery instance is created with given config.
        A subclass 'ContextTask' defines the task type of celery instance.
    """
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])
    
    class ContextTask(celery.Task):
      def __call__(self, *args, **kwargs):
        with app.app_context():
          return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
