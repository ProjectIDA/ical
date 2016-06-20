#-------------------------------------------------
#
# Project created by QtCreator 2015-12-29T11:46:40
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = iCalGui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui \
    run_dlg.ui \
    edit_dlg.ui \
    progress_dlg.ui \
    logview_dlg.ui \
    analysis_progress_window.ui \
    cool_off_progress_window.ui \
    about.ui

RESOURCES += \
    resources.qrc
