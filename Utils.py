# --------------------------------------------------------
#       UTILITY FUNCTIONS
# created on May 19th 2016 by M. Reichmann
# --------------------------------------------------------

from datetime import datetime, timedelta
from termcolor import colored
from numpy import sqrt
from os import makedirs, _exit
from os import path as pth
from os.path import join
from time import time
from collections import OrderedDict
import pickle
from string import maketrans


# ==============================================
# UTILITY FUNCTIONS
# ==============================================
def get_t_str():
    return datetime.now().strftime('%H:%M:%S')


def log_warning(msg):
    print '{head} {t} --> {msg}'.format(t=get_t_str(), msg=msg, head=colored('WARNING:', 'red'))


def log_info(msg):
    print '{head} {t} --> {msg}'.format(t=get_t_str(), msg=msg, head=colored('INFO:', 'grey'))


def log_critical(msg):
    print '{head} {t} --> {msg}\n'.format(t=get_t_str(), msg=msg, head=colored('CRITICAL:', 'red'))
    _exit(1)


def log_message(msg, overlay=False, prnt=True):
    if prnt:
        print '{ov}{t} --> {msg}{end}'.format(t=get_t_str(), msg=msg, ov='\033[1A\r' if overlay else '', end=' ' * 20 if overlay else '')


def round_down_to(num, val):
    return int(num) / val * val


def round_up_to(num, val):
    return int(num) / val * val + val


def calc_mean(l):
    l = [float(i) for i in l]
    mean_ = sum(l) / len(l)
    mean2 = sum(map(lambda x: x ** 2, l)) / len(l)
    sigma = sqrt(mean2 - mean_ ** 2)
    return mean_, sigma


def calc_weighted_mean(means, sigmas):
    weights = map(lambda x: x ** (-2), sigmas)
    variance = 1 / sum(weights)
    mean_ = sum(map(lambda x, y: x * y, means, weights))
    return mean_ * variance, sqrt(variance)


def file_exists(path):
    return pth.isfile(path)


def dir_exists(path):
    return pth.isdir(path)


def ensure_dir(path):
    if not pth.exists(path):
        log_message('Creating directory: {d}'.format(d=path))
        makedirs(path)


def print_banner(msg, symbol='=', new_lines=True):
    print '{n}{delim}\n{msg}\n{delim}{n}'.format(delim=len(str(msg)) * symbol, msg=msg, n='\n' if new_lines else '')


def print_small_banner(msg, symbol='-'):
    print '\n{delim}\n{msg}\n'.format(delim=len(str(msg)) * symbol, msg=msg)


def print_elapsed_time(start, what='This', show=True):
    t = '{d}'.format(d=timedelta(seconds=time() - start)).split('.')
    string = 'Elapsed time for {w}: {d1}.{m:2d}'.format(d1=t[0], m=int(round(int(t[1][:3])) / 10.), w=what)
    print_banner(string) if show else do_nothing()
    return string


def has_bit(num, bit):
    assert (num >= 0 and type(num) is int), 'num has to be non negative int'
    return bool(num & 1 << bit)


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def isint(x):
    try:
        a = float(x)
        b = int(a)
        return a == b
    except ValueError:
        return False


def get_resolution():
    try:
        from screeninfo import get_monitors
        m = get_monitors()
        return round_down_to(m[0].height, 500)
    except Exception as exc:
        log_warning('Could not get resolution! Using default ...\n\t{e}'.format(e=exc))
        return 1000


def print_table(rows, header=None):
    closing_row = '~' * len('| {r} |'.format(r=' | '.join(rows[-1])))
    if header is not None:
        print closing_row
        print '| {r} |'.format(r=' | '.join(header))
    print closing_row
    for row in rows:
        print '| {r} |'.format(r=(' | '.join(row) if len(row) > 1 else row[0]).ljust(len(closing_row) - 4))
    print closing_row


def get_base_dir():
    return join('/', *__file__.split('/')[1:3])


def do_pickle(path, func, value=None, params=None, redo=False):
    if value is not None:
        f = open(path, 'w')
        pickle.dump(value, f)
        f.close()
        return value
    if file_exists(path) and not redo:
        f = open(path, 'r')
        return pickle.load(f)
    else:
        ret_val = func() if params is None else func(params)
        f = open(path, 'w')
        pickle.dump(ret_val, f)
        f.close()
        return ret_val


def int_to_roman(integer):
    """ Convert an integer to Roman numerals. """
    if type(integer) != int:
        raise (TypeError, 'expected integer, got {t}'.format(t=type(integer)))
    if not 0 < integer < 4000:
        raise (ValueError, 'Argument must be between 1 and 3999')
    dic = OrderedDict([(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
                       (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')])
    result = ''
    for i, num in dic.iteritems():
        count = int(integer / i)
        result += num * count
        integer -= i * count
    return result


def remove_letters(string):
    new_str = ''
    for l in string:
        if l.isdigit():
            new_str += l
    return new_str


def clear_string(data):
    data = data.translate(None, '\r\n\x00\x13\x11\x10')
    data = data.translate(maketrans(',', ' '))
    return data.strip()


def convert_unicode(qstring):
    return unicode(str(qstring.toUtf8()).decode('utf8'))


def do(fs, pars, exe=-1):
    fs, pars = ([fs], [pars]) if type(fs) is not list else (fs, pars)
    exe = pars if exe == -1 else [exe]
    for f, p, e in zip(fs, pars, exe):
        f(p) if e is not None else do_nothing()


def do_nothing():
    pass