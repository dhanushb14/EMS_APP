FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /Timesheet_2.0

COPY requirements.txt /Timesheet_2.0/

RUN pip install -r requirements.txt

COPY . /Timesheet_2.0/

EXPOSE 8081

CMD  python manage.py migrate && python manage.py runserver 0.0.0.0:8081

