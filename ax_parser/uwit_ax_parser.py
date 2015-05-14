""" uwit_ax_parser.py - a utility script for parsing XML exports of Dynamics AX timesheets used by UW-IT.
"""
from xml.dom import minidom
import argparse
import matplotlib.pyplot as plt
from colorama import Fore

class Activity():

    def __init__(self, name, total):
        self.totalhours = total
        self.name = name

class Project():

    def __init__(self, name):
        self.name = name
        self.activities ={}
        self.totalhours = 0

def tsparse(timesheets):
    projects = {}
    for timesheet in timesheets:
        xmldoc = minidom.parse(timesheet)
        details = xmldoc.getElementsByTagName('Detail')
        for detail in details:
            project = detail.getAttribute('Textbox_59')
            activityName = detail.getAttribute('ActivityTxt')
            try:
                projects[project].totalhours = projects[project].totalhours + float(detail.getAttribute('TotalHours1'))
                if activityName in projects[project].activities:
                    projects[project].activities[activityName].totalhours = projects[project].activities[activityName].totalhours + float(detail.getAttribute('TotalHours1'))
                else:
                    activity = Activity(activityName, float(detail.getAttribute('TotalHours1')))
                    projects[project].activities[activityName] = activity
            except KeyError:
                obj = Project(project)
                activity = Activity(activityName, float(detail.getAttribute('TotalHours1')))
                obj.activities[activityName] = activity
                obj.totalhours = float(detail.getAttribute('TotalHours1'))
                projects[project] = obj
                projects[project].activities[activityName] = activity

    return projects

def printdata(projects, graph):
    print "************************************************************************"
    print
    print
    labels = []
    sizes = []
    explode = []
    timeSheetHours = 0
    for project in projects:
        timeSheetHours = timeSheetHours + projects[project].totalhours
        labels.append(project)
        sizes.append(projects[project].totalhours)
        explode.append(0.025)
        print(Fore.RED + "%s (%s)" % (project, str(projects[project].totalhours)) + Fore.RESET)
        for activity in projects[project].activities:
            print(Fore.CYAN + "   - %s (%s)" % (activity, str(projects[project].activities[activity].totalhours)) + Fore.RESET)
        print
    print(Fore.RED + "Total number of hours on these timesheets: " + str(timeSheetHours) + Fore.RESET)
    print
    print "************************************************************************"
    if graph:
        colors = ('b', 'g', 'r', 'c', 'm', 'y')
        plt.pie(sizes, explode=explode, labeldistance=1.2, pctdistance=1.1, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

def main(args):
    data = tsparse(args.timesheets)
    graph = args.graph
    printdata(data, graph)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g", "--graph", action='store_true', default=False, dest='graph')
    argparser.add_argument(nargs="+", action='store', dest='timesheets')
    args = argparser.parse_args()
    main(args)
