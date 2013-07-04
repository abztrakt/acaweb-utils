""" uwit_ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets used by UW-IT.
"""
from xml.dom import minidom


#TODO: make this take the timesheet file as an argument, not as a hard-coded var
TIMESHEET = "/Users/cstimmel/Downloads/TSTimesheetSignOff.Report.xml"
WEEK_HOURS = 40  # The number of hours that should be used to calculate each project as a percentage of the week's work.


class TimesheetDatum():
    project = None
    activity = None
    totalhrs = None
    percentage = None


def parse(timesheet):
    xmldoc = minidom.parse(timesheet)
    details = xmldoc.getElementsByTagName('Detail')
    data = []
    for detail in details:
        obj = TimesheetDatum()
        obj.project = detail.getAttribute('Textbox_59')
        obj.activity = detail.getAttribute('ActivityTxt')
        obj.totalhrs = float(detail.getAttribute('TotalHours1'))
        obj.percentage = obj.totalhrs/WEEK_HOURS * 100
        data.append(obj)
    return data


def printdata(data):
    for datum in data:
        print "%s (%s): %s%% (%s hrs)" % (datum.project, datum.activity, datum.percentage, datum.totalhrs)


def main(timesheet):
    data = parse(timesheet)
    printdata(data)


if __name__ == "__main__":
    main(TIMESHEET)
