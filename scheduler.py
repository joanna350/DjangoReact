import os
import requests
import schedule
import calendar

from argparse import ArgumentParser
from csv import DictWriter
from datetime import date
from datetime import datetime


class Holder():
    cache = {}

    def __init__(self, postD, commentD):
        '''
        :Str start: starting datetime to filter
        :Str end: ending datetime to filter
        :Str postD: day on which post will be filtered
        :List[Str] commentD: days over which comments are filtered
        '''
        self.postD = postD
        self.commentD = commentD

    def count(self, category):
        '''
        consumed by trigger functions
        category 1 for post 0 for comment
        '''

        url = 'http://localhost:8000/api/lead'

        try:
            page = requests.get(url).json() # List[dict()]
        except:
            print('host the Django web service first')
            raise

        if category: filtered_posts = 0
        else: filtered_comments = 0

        for content in page:
            timestamp = content['created_at']
            y,m,d = int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10])
            if category:
                if d == self.postD:
                    filtered_posts += 1
            else:
                if d in self.commentD:
                    filtered_comments += 1

        return filtered_posts if category else filtered_comments

    def trigger(self):
        '''
        store daily counts of comment and post as class variable
        will not keep track of anomalous behaviors by the user
        '''

        timeinfo = datetime.utcnow().date()
        today, m, y = timeinfo.day, timeinfo.month, timeinfo.year

        daily_post_count = 0
        if today == self.postD:
            daily_post_count = self.count(1)

        daily_comment_count = 0
        if today in self.commentD:
            daily_comment_count = self.count(0)

        if 'daily_comment_count' not in self.cache:
            self.cache['daily_comment_count'] = {}
        if y not in self.cache['daily_comment_count']:
            self.cache['daily_comment_count'][y] = {}
        if m not in self.cache['daily_comment_count'][y]:
            self.cache['daily_comment_count'][y][m] = [] # index = day-1
        self.cache['daily_comment_count'][y][m].append(daily_comment_count)

        if 'daily_post_count' not in self.cache:
            self.cache['daily_post_count'] = {}
        if y not in self.cache['daily_post_count']:
            self.cache['daily_post_count'][y] = {}
        if m not in self.cache['daily_post_count'][y]:
            self.cache['daily_post_count'][y][m] = []
        self.cache['daily_post_count'][y][m].append(daily_post_count)

        if self.check_end_of_month(timeinfo):

            filtered_comments = sum(self.cache['daily_comment_count'][y][m])
            filtered_posts = sum(self.cache['daily_post_count'][y][m])

            headers = ['monthly_comment_count', 'monthly_post_count']
            fn = 'monthly_aggregate.csv'
            if not os.path.isfile(fn):
                with open(fn, 'w', newline='') as file:
                    a = DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
                    a.writeheader()
                    a.writerow({headers[0]: filtered_comments, headers[1]: filtered_posts})
            else:
                with open(fn, 'a+', newline='') as file:
                    a = DictWriter(file, fieldnames=headers)
                    a.writerow({headers[0]: filtered_comments, headers[1]: filtered_posts})

    @staticmethod
    def check_day(dt):
        '''
        debugging purpose
        '''
        base = date(2021,7,15)
        return True if date(dt.year, dt.month, dt.day) == base else False

    @staticmethod
    def check_end_of_month(timeinfo):
        '''
        for monthly aggregation
        '''
        last_day_of_month = calendar.monthrange(timeinfo.year, timeinfo.month)[1]
        return True if timeinfo.day == last_day_of_month else False


def argparser():
    '''
    receives and passes start time, end time, post day, commenting days
    '''
    parser = ArgumentParser()
    parser.add_argument('s', nargs= '?', action='store', default=0, type =str)
    parser.add_argument('e', nargs= '?', action='store', default=0, type =str)
    parser.add_argument('p', nargs= '?', action='store', default=0, type =int)
    parser.add_argument('c', nargs= '+', action='store', default=0, type =int)

    args = vars(parser.parse_args())

    return args['s'], args['e'], args['p'], args['c']


def parseDate(input):
    y, m, d = int(input[:4]), int(input[5:7]), int(input[8:])
    return y, m, d


def main():
    '''
    main script to
    - retrieve parameters from stdin
    - sets the time period for long running task with schedule API with the params
    - invokes relevant functions in the sequence to conduct the goal
    separated for testing purpose
    '''
    start, end, postD, commentD = argparser()

    y, m, d = parseDate(start)
    _from = date(y, m, d)

    y, m, d = parseDate(end)
    _until = date(y, m, d)

    inst = Holder(postD, commentD)
    schedule.every().day.at("23:59").do(inst.trigger)

    while True:
        while _from <= datetime.utcnow().date() <= _until:
            schedule.run_pending()
        else:
            break


if __name__ == '__main__':
    main()