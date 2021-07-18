from scheduler import Holder, parseDate
from datetime import date, datetime


inst = Holder(1, [2])

def test_init():
    assert inst.postD == 1
    assert inst.commentD == [2]

def test_count():

    assert inst.count(1) == 0
    assert inst.count(0) == 0

def test_trigger():
    inst.trigger()
    assert inst.cache['daily_post_count'] == {}
    assert inst.cache['daily_comment_count'] == {}

def test_check_day():
    dt = date(2021,7,15)
    assert inst.check_day(dt) == True

def test_check_end_of_month():
    dt = date(2021,7,15)
    assert inst.check_end_of_month(dt) == False

def test_parseDate():
    y, m, d = parseDate('2021-07-15')
    assert y == 2021
    assert m == 7
    assert d == 15

def test_main():
    pass