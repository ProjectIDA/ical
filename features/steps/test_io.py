from behave import *
from hamcrest import *

import os
import tempfile
from pathlib import Path

from config.io import *
import config.ical_dbcfg as dbcfg

@given('DB Temp Location needed')
def step_impl(context):
    context.tmpdirobj = tempfile.TemporaryDirectory()
    context.tmpdirpath = context.tmpdirobj.name


# Scenario: Ask to read file_key
@given('An empty file_key to read')
def step_impl(context):
    context.file_key = ''

@when('I try to read file with empty file_key')
def step_impl(context):
    context.file_key = ''

@then('should receive ICAL_FILEKEY_IS_EMPTY exception on read')
def step_impl(context):
    assert_that(calling(read_icalfile).with_args('.', context.file_key, dbcfg.DB_file_struct), raises(IcalFileKeyEmpty))



@given('An invalid file_key {invalid} to read')
def step_impl(context, invalid):
    context.file_key = invalid

@when('I try to read file with invalid file_key')
def step_impl(context):
    pass    

@then('should receive ICAL_FILEKEY_UNKNOWN exception on read')
def step_impl(context):
    assert_that(calling(read_icalfile).with_args(context.tmpdirpath, context.file_key, dbcfg.DB_file_struct), raises(IcalFileKeyUnknown))


# Scenario Outline: Ask to read valid file_keys
@given('An valid file_key {file_key} to read')
def step_impl(context, file_key):
    context.file_key = file_key

@when('I try to read file having contents {content}')
def step_impl(context, content):
    context.content = content

    p = Path(os.sep.join([context.tmpdirpath, dbcfg.DB_file_struct[context.file_key]['path']]))
    fpath = p.__str__()
    os.makedirs(fpath, exist_ok=True)

    f = open(fpath + os.sep + dbcfg.DB_file_struct[context.file_key]['file'], 'w')
    f.write(context.content)
    f.close()

@then('should return the correct content string')
def step_impl(context):

    data = read_icalfile(context.tmpdirpath, context.file_key, dbcfg.DB_file_struct)

    context.tmpdirobj.cleanup()
    assert_that(data, equal_to(context.content))


# Scenario Outline: Ask to read missing DB file
@given('A file_key {file_key} to read')
def step_impl(context, file_key):
    context.file_key = file_key

@when('The file does not exist')
def step_impl(context):

    fpath = os.sep.join([dbcfg.DB_file_struct[context.file_key]['path'], dbcfg.DB_file_struct[context.file_key]['file']] )

    if Path(fpath).exists():
        Path(fpath).unlink()

@then('should receive IcalFileNotFound exception')
def step_impl(context):
    assert_that(calling(read_icalfile).with_args(context.tmpdirpath, context.file_key, dbcfg.DB_file_struct), raises(IcalFileNotFound))

#####################
# WRITE TESTS
#####################

@given(u'A file_key {wfile_key} to write')
def step_impl(context, wfile_key):
    context.file_key = wfile_key

@when(u'and IOError is raised')
def step_impl(context):
    context.bad_root_path = '/deleteme2'

@then(u'should receive IcalWriteError exception')
def step_impl(context):
    assert_that(calling(save_icalfile).with_args(context.bad_root_path, context.file_key, dbcfg.DB_file_struct, "qwerty"), raises(IcalWriteError))


@given(u'a valid file_key {wfile_key} to write')
def step_impl(context, wfile_key):
    context.file_key = wfile_key
    context.dbpath = '.'

@when(u'I try to write file having contents {wcontent}')
def step_impl(context, wcontent):
    context.content = wcontent

@then(u'should write the correct string')
def step_impl(context):
    
    save_icalfile(context.dbpath, context.file_key, dbcfg.DB_file_struct, context.content)

    fpath = os.sep.join([context.dbpath, dbcfg.DB_file_struct[context.file_key]['path'], dbcfg.DB_file_struct[context.file_key]['file']])
    fpath = Path(fpath).__str__()
    with open(fpath, 'r') as fl:
        data = fl.read()

    assert_that(data, equal_to(context.content))

@given(u'An empty file_key to write')
def step_impl(context):
    context.file_key = ''

@then(u'should receive ICAL_FILEKEY_IS_EMPTY exception on write')
def step_impl(context):
    assert_that(calling(save_icalfile).with_args('.', context.file_key, dbcfg.DB_file_struct, "qwerty"), raises(IcalFileKeyEmpty))

@given(u'An invalid file_key "invalid" to write')
def step_impl(context):
    context.file_key = 'holy_grail'

@then(u'should receive ICAL_FILEKEY_UNKNOWN exception on write')
def step_impl(context):
    assert_that(calling(save_icalfile).with_args('.', context.file_key, dbcfg.DB_file_struct, "qwerty"), raises(IcalFileKeyUnknown))


