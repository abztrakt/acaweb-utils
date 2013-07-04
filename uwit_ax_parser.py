""" uwit_ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets used by UW-IT.
"""
from xml.dom import minidom


#TODO: make this take the timesheet file as an argument, not as a hard-coded var
TIMESHEET = "/Users/cstimmel/Downloads/TSTimesheetSignOff.Report.xml"
WEEK_HOURS = 40  # The number of hours that should be used to calculate each project as a percentage of the week's work.


def main(timesheet):
    xmldoc = minidom.parse(timesheet)
    details = xmldoc.getElementsByTagName('Detail')
    for detail in details:
        project = detail.getAttribute('Textbox_59')
        totalhrs = float(detail.getAttribute('TotalHours1'))
        percentage = totalhrs/WEEK_HOURS * 100
        print "%s: %s%% (%s)" % (project, percentage, totalhrs)


if __name__ == "__main__":
    main(TIMESHEET)
