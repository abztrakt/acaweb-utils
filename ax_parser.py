""" ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets.
"""
from xml.dom import minidom


#TODO: make this take the timesheet file as an argument, not as a hard-coded var
TIMESHEET = "/Users/cstimmel/Downloads/TSTimesheetSignOff.Report.xml"


def main(timesheet):
    xmldoc = minidom.parse(timesheet)
    print xmldoc.toxml()


if __name__ == "__main__":
    main(TIMESHEET)
