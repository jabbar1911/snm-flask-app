from random import randint
from secrets import choice


def genotp():
    otp = ""
    for i in range(6):
        otp += choice("0123456789")
    return otp

