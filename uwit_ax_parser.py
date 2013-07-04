""" uwit_ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets used by UW-IT.
"""
from xml.dom import minidom


#TODO: make this take the timesheet file as an argument, not as a hard-coded var
TIMESHEET = "/Users/cstimmel/Downloads/TSTimesheetSignOff.Report.xml"


def main(timesheet):
    xmldoc = minidom.parse(timesheet)
    details = xmldoc.getElementsByTagName('Detail')
    for detail in details:
        project = detail.getAttribute('Textbox_59')
        totalhrs = detail.getAttribute('TotalHours1')
        print project
        print totalhrs


if __name__ == "__main__":
    main(TIMESHEET)
