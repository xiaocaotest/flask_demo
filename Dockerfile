FROM python

ENV DIR_HOME /Project/flask_demo

COPY . $DIR_HOME
WORKDIR $DIR_HOME

RUN pip install -r requirements.txt
CMD ["gunicorn", "run:application", "-c", "./gunicorn.conf.py"]