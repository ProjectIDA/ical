from config.ical_config import *

cfg = None

def startup():
    cfg = IcalConfig('/Users/dauerbach/dev/ical')

    try:
        res, warns, errs, cfgdicts = cfg.load_config()
    except:
        errs.append('ERROR LOADING ICAL CONFIGURATION')

    print(res)

    for msg in warns:
        print('WARN:  ', msg)
    for msg in errs:
        print('ERROR: ', msg)
