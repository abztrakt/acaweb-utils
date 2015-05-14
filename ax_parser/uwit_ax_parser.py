""" uwit_ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets used by UW-IT.
"""
from xml.dom import minidom
import argparse


#TODO: make this take the timesheet file as an argument, not as a hard-coded var
TIMESHEET = "/Users/cstimmel/Downloads/TSTimesheetSignOff.Report.xml"
WEEK_HOURS = 40  # The number of hours that should be used to calculate each project as a percentage of the week's work.


class TimesheetDatum():
    project = None
    activity = None
    totalhrs = 0

    def __repr__(self):
        return "%s (%s)" % (self.project, self.activity)

    def percentage(self):
        weekhours = WEEK_HOURS * args.timesheets.__len__()
        return self.totalhrs/weekhours * 100

def tsparse(timesheets):
    data = {}
    for timesheet in timesheets:
        xmldoc = minidom.parse(timesheet)
        details = xmldoc.getElementsByTagName('Detail')
        for detail in details:
            repr = "%s (%s)" % (detail.getAttribute('Textbox_59'), detail.getAttribute('ActivityTxt'))
            try:
                data[repr].totalhrs = data[repr].totalhrs + float(detail.getAttribute('TotalHours1'))
            except KeyError:
                obj = TimesheetDatum()
                obj.project = detail.getAttribute('Textbox_59')
                obj.activity = detail.getAttribute('ActivityTxt')
                obj.totalhrs = float(detail.getAttribute('TotalHours1'))
            data[obj.__repr__()] = obj
    return data


def printdata(data):
    for datum in data.values():
        print "%s: %s%% (%s hrs)" % (datum.__repr__(), datum.percentage(), datum.totalhrs)

def main(args):
    data = tsparse(args.timesheets)
    printdata(data)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(nargs='+', action='store', dest='timesheets')
    args = argparser.parse_args()
    main(args)
