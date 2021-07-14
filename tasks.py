#from .celery import app
import os
import redis
import requests

from celery import Celery
from celery.schedules import crontab
from csv import writer
from datetime import datetime
from django.conf import settings


app = Celery('tasks', broker='pyamqp://')


# todo 2: celery crontab (daily, monthly at fixed time) > store daily values in redis
# todo 3:                                               > populate monthly values into .csv file
# todo x: preprocess the 'post' text data and convert into data vector (cosine similarity for later)

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   db=0)

def count_post(start, end, postD):

    url = 'http://localhost:8000/api/lead'
    page = requests.get(url)
    page = page.json() # List[dict()]

    y, m, d = int(start[:4]), int(start[5:7]), int(start[8:])
    _from = datetime(y, m, d)

    y, m, d = int(end[:4]), int(end[5:7]), int(end[8:])
    _until = datetime(y, m, d)

    filtered_posts = 0
    for content in page:
        timestamp = content['created_at']
        y,m,d = int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10])
        if _from <= datetime(y,m,d) <= _until:
            if d == postD:
                filtered_posts += 1

    return filtered_posts


def count_comment(start, end, commentD):

    url = 'http://localhost:8000/api/lead'
    page = requests.get(url)
    page = page.json() # List[dict()]

    y, m, d = int(start[:4]), int(start[5:7]), int(start[8:])
    _from = datetime(y, m, d)

    y, m, d = int(end[:4]), int(end[5:7]), int(end[8:])
    _until = datetime(y, m, d)

    filtered_comments = 0
    for content in page:
        timestamp = content['created_at']
        y,m,d = int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10])
        if _from <= datetime(y,m,d) <= _until:
            if d in commentD:
                filtered_comments += 1

    return filtered_comments


# app.task()
def daily_trigger(start, end, postD, commentD):
    '''
    given
    -----
    :Str start: starting datetime for filter
    :Str end: ending datetime for filter
    :Str postD: day on which post will be filtered
    :List[Str] commentD: days over which comments are filtered
    '''

    timeinfo = datetime.utcnow().date()
    today, m, y = timeinfo.day, timeinfo.month, timeinfo.year

    daily_post_count = 0
    if today == postD:
        daily_post_count = count_post(start, end, postD)

    daily_comment_count = 0
    if today in commentD:
        daily_comment_count = count_comment(start, end, commentD)

    if 'daily_comment_count' not in redis_instance:
        redis_instance['daily_comment_count'] = {}
    if y not in redis_instance['daily_comment_count']:
        redis_instance['daily_comment_count'][y] = {}
    if m not in redis_instance['daily_comment_count'][y]:
        redis_instance['daily_comment_count'][y][m] = [daily_comment_count]

    redis_instance['daily_comment_count'][y][m].append(daily_comment_count)

    if 'daily_post_count' not in redis_instance:
        redis_instance['daily_post_count'] = {}
    if y not in redis_instance['daily_post_count']:
        redis_instance['daily_post_count'][y] = {}
    if m not in redis_instance['daily_post_count'][y]:
        redis_instance['daily_post_count'][y][m] = [daily_post_count]

    redis_instance['daily_post_count'][y][m].append(daily_post_count)


def monthly_trigger(start, end, postD, commentD):
    '''
    given
    -----
    :Str start: starting datetime for filter
    :Str end: ending datetime for filter
    :Str postD: day on which post will be filtered
    :List[Str] commentD: days over which comments are filtered
    '''

    timeinfo = datetime.utcnow().date()
    y, m = timeinfo.year, timeinfo.month

    # get from redis
    filtered_comments = sum(redis_instance['daily_comment_count'][y][m])
    filtered_posts = sum(redis_instance['daily_post_count'][y][m])

    fn = 'monthly_aggregate.csv'
    if not os.path.isfile(fn):
        with open(fn, 'w', newline='') as file:
            writer = writer(file, delimiter=',')
            writer.writerow(['monthly_comment_count', 'monthly_post_count'])
            writer.writerow([filtered_comments, filtered_posts])
    else:
        with open(fn, 'a+', newline='') as file:
            writer = writer(file)
            writer.writerow([filtered_comments, filtered_posts])


if __name__ == '__main__':
    daily_trigger('2011-07-13','2021-07-13', 13, [11])
