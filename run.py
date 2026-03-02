from my_app import app

if __name__ == '__main__':
    app.run()

#python run.py


#celery -A my_app.tasks.celery_app worker --loglevel=info
