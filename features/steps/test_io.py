from behave import *
from hamcrest import *

import os
import tempfile
from pathlib import Path

from config.io import *

@given('DB Temp Location needed')
def step_impl(context):
    context.tmpdirobj = tempfile.TemporaryDirectory()
    context.tmpdirpath = context.tmpdirobj.name

    print(context.tmpdirpath)


# Scenario: Ask to read file_key
@given('An empty file_key')
def step_impl(context):
    context.file_key = ''

@when('I try to read file with empty file_key')
def step_impl(context):
    context.file_key = ''

@then('should receive ICAL_FILEKEY_IS_EMPTY exception')
def step_impl(context):
    assert_that(calling(read_file).with_args('.', context.file_key), raises(IcalFileKeyEmpty))



@given('An invalid file_key {invalid}')
def step_impl(context, invalid):
    context.file_key = invalid

@when('I try to read file with invalid file_key')
def step_impl(context):
    pass    

@then('should receive ICAL_FILEKEY_UNKNOWN exception')
def step_impl(context):
    assert_that(calling(read_file).with_args(context.tmpdirpath, context.file_key), raises(IcalFileKeyUnknown))


# Scenario Outline: Ask to read valid file_keys
@given('An valid file_key {file_key}')
def step_impl(context, file_key):
    context.file_key = file_key

@when('I try to read file having contents {content}')
def step_impl(context, content):
    context.content = content

    p = Path(os.sep.join([context.tmpdirpath, DB_file_struct[context.file_key]['path']]))
    fpath = p.__str__()
    os.makedirs(fpath, exist_ok=True)

    f = open(fpath + os.sep + DB_file_struct[context.file_key]['file'], 'w')
    f.write(context.content)
    f.close()

@then('should return the correct content string')
def step_impl(context):

    data = read_file(context.tmpdirpath, context.file_key)

    context.tmpdirobj.cleanup()
    assert_that(data, equal_to(context.content))


# Scenario Outline: Ask to read missing DB file
@given('A file_key {file_key}')
def step_impl(context, file_key):
    context.file_key = file_key

@when('The file does not exist')
def step_impl(context):

    fpath = os.sep.join([DB_file_struct[context.file_key]['path'], DB_file_struct[context.file_key]['file']] )

    if Path(fpath).exists():
        Path(fpath).unlink()

@then('should receive IcalFileNotFound exception')
def step_impl(context):
    assert_that(calling(read_file).with_args(context.tmpdirpath, context.file_key), raises(IcalFileNotFound))

