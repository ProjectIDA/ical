from config.utils import ParseResult

import dateutil
from dateutil.tz import *
import datetime
import re


SENSOR_COLCOUNT = 5 # this is minimum cause last col (5) is quoted and contains spaces
SENSOR_NDX_SHORTNAME = 0
SENSOR_NDX_DESCR = 4

CALIB_COLCOUNT = 8
CALIB_NDX_CALTYPE = 0
CALIB_NDX_SENSNAME = 1
CALIB_NDX_WF = 2
CALIB_NDX_AMP = 3
CALIB_NDX_DUR = 4
CALIB_NDX_SET = 5
CALIB_NDX_TRL = 6
CALIB_NDX_DIV = 7

AUTH_COLCOUNT = 8
AUTH_NDX_TAGNO = 0
AUTH_NDX_SN = 1
AUTH_NDX_CFG_AUTH = 2
AUTH_NDX_SFN_AUTH = 3
AUTH_NDX_DP1_AUTH = 4
AUTH_NDX_DP2_AUTH = 5
AUTH_NDX_DP3_AUTH = 6
AUTH_NDX_DP4_AUTH = 7

Q330_COLCOUNT = 4
Q330_NDX_IP = 0
Q330_NDX_TAGNO = 1
Q330_NDX_SENS_COMPNAME_A = 2
Q330_NDX_SENS_COMPNAME_B = 3

ICAL_COLCOUNT = 9
ICAL_NDX_STA = 0
ICAL_NDX_TAGNO = 1
ICAL_NDX_DATAPORT = 2
ICAL_NDX_MONPORT_A = 3
ICAL_NDX_MONPORT_B = 4
ICAL_NDX_LAST_LF_A = 5
ICAL_NDX_LAST_HF_A = 6
ICAL_NDX_LAST_LF_B = 7
ICAL_NDX_LAST_HF_B = 8




def dbcfg_parse(data='', rec_parser=None):

    dbdict = {}
    infomsgs = []
    errmsgs = []

    data = data.strip()
    records = data.splitlines()

    for lineno, rec in enumerate(records):
        rec = rec.strip()

        if not (rec.startswith('#') or (len(rec) == 0)):
            tokens = re.split('\s+',rec)

            infos, errs, dbdict = rec_parser(dbdict, tokens)
            infomsgs.extend(map(lambda msg: 'Line: ' + str(lineno+1) + ': ' + msg, infos))
            errmsgs.extend(map(lambda msg: 'Line: ' + str(lineno+1) + ': ' + msg, errs))

    return ParseResult(infomsgs, errmsgs, dbdict)


def sensorcfg_parse(dbdict, tokens):

    infomsgs = []
    errmsgs = []

    # description filed is variable text with possible spaces. Assume at least 1 word
    # ? will need to strip any dbl quotes around tokens 4+
    if len(tokens) >= SENSOR_COLCOUNT:

        # get all description words together
        tokens[SENSOR_NDX_DESCR] = ' '.join(tokens[SENSOR_NDX_DESCR:])
        # strip quotes on description
        tokens[SENSOR_NDX_DESCR] = tokens[SENSOR_NDX_DESCR].strip('"')

        dbdict[tokens[SENSOR_NDX_SHORTNAME]] = { 'descr': tokens[SENSOR_NDX_DESCR] }

    else:
        errmsgs.append('Sensor record should have at least ' + str(SENSOR_COLCOUNT) + ' columns. [' + ' '.join(tokens) + ']. Record removed.')

    return ParseResult(infomsgs, errmsgs, dbdict)


def calibcfg_parse(dbdict, tokens):

    infomsgs = []
    errmsgs = []

    if len(tokens) == CALIB_COLCOUNT:
        
        success = True
        name_ok = (tokens[CALIB_NDX_CALTYPE].lower() in ['rblf', 'rbhf'])
        wf_ok = re.fullmatch('\d+', tokens[CALIB_NDX_WF]) != None
        amp_ok = re.fullmatch('\d+', tokens[CALIB_NDX_AMP]) != None
        dur_ok = re.fullmatch('\d+', tokens[CALIB_NDX_DUR]) != None
        set_ok = re.fullmatch('\d+', tokens[CALIB_NDX_SET]) != None
        trl_ok = re.fullmatch('\d+', tokens[CALIB_NDX_TRL]) != None
        div_ok = re.fullmatch('\d+', tokens[CALIB_NDX_DIV]) != None

        success = name_ok and wf_ok and amp_ok and dur_ok and set_ok and trl_ok and div_ok

        if not name_ok:
            errmsgs.append('Calib record has an invalid Name: ' + tokens[CALIB_NDX_CALTYPE] + '. Record removed.')
        if not wf_ok:
            errmsgs.append('Calib record has an invalid wf: '   + tokens[CALIB_NDX_WF] + '. Record removed.')
        if not amp_ok:
            errmsgs.append('Calib record has an invalid amp: '  + tokens[CALIB_NDX_AMP] + '. Record removed.')
        if not dur_ok:
            errmsgs.append('Calib record has an invalid dur: '  + tokens[CALIB_NDX_DUR] + '. Record removed.')
        if not set_ok:
            errmsgs.append('Calib record has an invalid set: '  + tokens[CALIB_NDX_SET] + '. Record removed.')
        if not trl_ok:
            errmsgs.append('Calib record has an invalid trl: '  + tokens[CALIB_NDX_TRL] + '. Record removed.')
        if not div_ok:
            errmsgs.append('Calib record has an invalid div: '  + tokens[CALIB_NDX_DIV] + '. Record removed.')
        
        if success:
            if tokens[CALIB_NDX_SENSNAME] not in dbdict:
                dbdict[tokens[CALIB_NDX_SENSNAME]] = {}

            dbdict[tokens[CALIB_NDX_SENSNAME]][tokens[CALIB_NDX_CALTYPE].lower()] = {
                'wf': tokens[CALIB_NDX_WF], 
                'amp': tokens[CALIB_NDX_AMP], 
                'dur': tokens[CALIB_NDX_DUR], 
                'set': tokens[CALIB_NDX_SET], 
                'trl': tokens[CALIB_NDX_TRL], 
                'div': tokens[CALIB_NDX_DIV]
                }

    else:
        errmsgs.append('Calib record should have ' + str(CALIB_COLCOUNT)  + 'columns. [' + ' '.join(tokens) + ']. Record removed.')

    return ParseResult(infomsgs, errmsgs, dbdict)


def authcfg_parse(dbdict, tokens):

    infomsgs = []
    errmsgs = []

    if len(tokens) == AUTH_COLCOUNT:

        tagno_ok = re.fullmatch('\d+', tokens[AUTH_NDX_TAGNO]) != None
        sn_ok = re.fullmatch('[0-9A-Fa-f]{16}', tokens[1]) != None

        success = tagno_ok and sn_ok

        if not tagno_ok:
            errmsgs.append('Auth record has an invalid TagNo: ' + tokens[AUTH_NDX_TAGNO])
        if not sn_ok:
            errmsgs.append('Auth record has an invalid Serial Number: ' + tokens[AUTH_NDX_SN])

        if success:
            dbdict[tokens[AUTH_NDX_TAGNO]] = {
                'valid'     : success,
                'tagno_auth': tokens[AUTH_NDX_TAGNO],
                'sn': tokens[AUTH_NDX_SN], 
                'cfgport_auth': tokens[AUTH_NDX_CFG_AUTH], 
                'sfnport_auth': tokens[AUTH_NDX_SFN_AUTH], 
                'dp1_auth': tokens[AUTH_NDX_DP1_AUTH], 
                'dp2_auth': tokens[AUTH_NDX_DP2_AUTH], 
                'dp3_auth': tokens[AUTH_NDX_DP3_AUTH], 
                'dp4_auth': tokens[AUTH_NDX_DP4_AUTH]
                }

    else:
        errmsgs.append('Auth record should have ' + str(AUTH_COLCOUNT) + ' columns [' + ' '.join(tokens) + ']. Record removed.')

    return ParseResult(infomsgs, errmsgs, dbdict)


def q330cfg_parse(dbdict, tokens):

    infomsgs = []
    errmsgs = []

    if len(tokens) == Q330_COLCOUNT:

        ip_ok = re.fullmatch('\d+\.\d+\.\d+\.\d+', tokens[Q330_NDX_IP]) != None
        tagno_ok = re.fullmatch('\d+', tokens[Q330_NDX_TAGNO]) != None

        if not ip_ok:
            errmsgs.append('q330.cfg record has an invalid IP address: ' + tokens[Q330_NDX_IP])
        if not tagno_ok:
            errmsgs.append('q330.cfg record has an invalid TagNo: ' + tokens[Q330_NDX_TAGNO])

        success = ip_ok and tagno_ok

        # going to leave bad TAGNO and SN in dict. Let it fail at qcal 
        dbdict[tokens[Q330_NDX_TAGNO]] = {
            'valid'         : success,
            'ip_address'    : tokens[Q330_NDX_IP], 
            'tagno_q330cfg' : tokens[Q330_NDX_TAGNO],
            'sensor_a_comp_name': tokens[Q330_NDX_SENS_COMPNAME_A], 
            'sensor_b_comp_name': tokens[Q330_NDX_SENS_COMPNAME_B], 
            'sensor_a_root_name': tokens[Q330_NDX_SENS_COMPNAME_A].split(':')[0], 
            'sensor_b_root_name': tokens[Q330_NDX_SENS_COMPNAME_B].split(':')[0]
        }

    else:
        errmsgs.append('q330.cfg record should have ' + str(Q330_COLCOUNT) + ' columns [' + ' '.join(tokens) + ']. Record removed.')

    return ParseResult(infomsgs, errmsgs, dbdict)


def icalcfg_parse(dbdict, tokens):

    infomsgs = []
    errmsgs = []


    dbdict.setdefault('q330s', [])

    if len(tokens) == ICAL_COLCOUNT:

        sta_ok = re.fullmatch('[A-Za-z][A-Za-z0-9]{2,5}', tokens[ICAL_NDX_STA]) != None
        tagno_ok = re.fullmatch('\d+', tokens[ICAL_NDX_TAGNO]) != None
        dataport_ok = re.fullmatch('[1-4]', tokens[ICAL_NDX_DATAPORT]) != None
        monport_a_ok = re.fullmatch('[0,4-6]', tokens[ICAL_NDX_MONPORT_A]) != None
        monport_b_ok = re.fullmatch('[0,1-3]', tokens[ICAL_NDX_MONPORT_B]) != None
        
        if not sta_ok:
            errmsgs.append('ical.cfg record has an invalid STATION code: ' + tokens[ICAL_NDX_STA] + '. Record removed.')
        if not tagno_ok:
            errmsgs.append('ical.cfg record has an invalid TagNo: ' + tokens[ICAL_NDX_TAGNO] + '. Record removed.')
        if not dataport_ok:
            errmsgs.append('ical.cfg record has an invalid dataport: ' + tokens[ICAL_NDX_DATAPORT] + '. Record removed.')
        if not monport_a_ok:
            errmsgs.append('ical.cfg record has an invalid Monitor port for sensor A: ' + tokens[ICAL_NDX_MONPORT_A] + '. Record removed.')
        if not monport_b_ok:
            errmsgs.append('ical.cfg record has an invalid Monitor port for sensor B: ' + tokens[ICAL_NDX_MONPORT_B] + '. Record removed.')

        # write timestamps: datetime.now(tzutc()).isoformat() ==> '2016-01-06T19:59:39.423223+00:00'
        # read timestamps: date = dateutil.parser.parse('2016-01-06T19:59:39.423223+00:00')
        # now deal with timestamps....        
        try:
            sensor_a_last_lf = 'none' if tokens[ICAL_NDX_LAST_LF_A] == 'none' else dateutil.parser.parse(tokens[ICAL_NDX_LAST_LF_A])
            sensor_a_last_lf_ok = True
        except Exception:
            sensor_a_last_lf = 'none'
            sensor_a_last_lf_ok = False
            errmsgs.append('ical.cfg record has an invalid timestamp for the Previous Low Freq Calibration for sensor A: ' + tokens[ICAL_NDX_LAST_LF_A] + '. Value set to "none".')

        try:
            sensor_a_last_hf = 'none' if tokens[ICAL_NDX_LAST_HF_A] == 'none' else dateutil.parser.parse(tokens[ICAL_NDX_LAST_HF_A])
            sensor_a_last_hf_ok = True
        except Exception:
            sensor_a_last_hf = 'none'
            sensor_a_last_hf_ok = False
            errmsgs.append('ical.cfg record has an invalid timestamp for the Previous High Freq Calibration for sensor A: ' + tokens[ICAL_NDX_LAST_HF_A] + '. Value set to "none".')

        try:
            sensor_b_last_lf = 'none' if tokens[ICAL_NDX_LAST_LF_B] == 'none' else dateutil.parser.parse(tokens[ICAL_NDX_LAST_LF_B])
            sensor_b_last_lf_ok = True
        except Exception:
            sensor_b_last_lf = 'none'
            sensor_b_last_lf_ok = False
            errmsgs.append('ical.cfg record has an invalid timestamp for the Previous Low Freq Calibration for sensor B: ' + tokens[ICAL_NDX_LAST_LF_B] + '. Value set to "none".')

        try:
            sensor_b_last_hf = 'none' if tokens[ICAL_NDX_LAST_HF_B] == 'none' else dateutil.parser.parse(tokens[ICAL_NDX_LAST_HF_B])
            sensor_b_last_hf_ok = True
        except Exception:
            sensor_b_last_hf = 'none'
            sensor_b_last_hf_ok = False
            errmsgs.append('ical.cfg record has an invalid timestamp for the Previous High Freq Calibration for sensor B: ' + tokens[ICAL_NDX_LAST_HF_B] + '. Value set to "none".')


        success = sta_ok and \
                tagno_ok and \
                dataport_ok and \
                monport_a_ok and \
                monport_b_ok

        dbdict['q330s'].append({
                'valid'             : success,
                'station'           : tokens[ICAL_NDX_STA],
                'tagno'             : tokens[ICAL_NDX_TAGNO],
                'dataport'          : tokens[ICAL_NDX_DATAPORT], 
                'sensor_a_mon_port' : tokens[ICAL_NDX_MONPORT_A],
                'sensor_b_mon_port' : tokens[ICAL_NDX_MONPORT_B],
                'sensor_a_last_lf'  : sensor_a_last_lf,
                'sensor_a_last_hf'  : sensor_a_last_hf,
                'sensor_b_last_lf'  : sensor_b_last_lf,
                'sensor_b_last_hf'  : sensor_b_last_hf,
            }
        )
    else:
        errmsgs.append('ical.cfg record should have ' + str(ICAL_COLCOUNT) + ' columns [' + ' '.join(tokens) + ']. Record removed.')

    print(errmsgs, dbdict)
    return ParseResult(infomsgs, errmsgs, dbdict)

