import random


def round_quantity(number, base):
    return base * round(number/base, 2)


def random_float(min, max, decimals):
    print('start random float ' + str(min) + ' ' + str(max))
    min_range = int(min * pow(10, decimals))
    max_range = int(max * pow(10, decimals))
    number = random.randrange(min_range, max_range, 1)
    number = round(number/pow(10, decimals), decimals)
    return number
