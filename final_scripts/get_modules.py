# get all od tests and project-sha-module turples where the od tests are in
# usage: python get_modules.py
# input: idoft/pr-data.csv
# output: all_od_tests.csv projects_modules.csv

import csv

idoft_pr_data_path = '../pr-data.csv'

output_od_tests_csv = '../all_od_tests.csv'
output_projects_csv = '../projects_modules.csv'

od_tests_info = []
project_module_info = []


def get_all_od_tests():
    pr_data = open(idoft_pr_data_path,"r")
    pr_data_reader = csv.reader(pr_data)

    for eachline in pr_data_reader:
        if 'OD' in eachline[4] and 'NOD' not in eachline[4] and 'NDOD' not in eachline[4]:
            if eachline[0:6] not in od_tests_info:
                od_tests_info.append(eachline[0:5])
    
    with open(output_od_tests_csv,"w",newline='') as od_csv:
        writer = csv.writer(od_csv)
        writer.writerow(['Project URL','sha','module','test','category'])
        for each in od_tests_info:
            writer.writerow(each)


def get_projects_to_clone():
    pr_data = open(output_od_tests_csv,"r")
    pr_data_reader = csv.reader(pr_data)

    for eachline in pr_data_reader:
        if eachline[0] != 'Project URL':
            if eachline[0:3] not in project_module_info:
                project_module_info.append(eachline[0:3])
    
    with open(output_projects_csv,"w",newline='') as mod_csv:
        writer = csv.writer(mod_csv)
        writer.writerow(['Project URL','sha','module'])
        for each in project_module_info:
            writer.writerow(each)


get_all_od_tests()
get_projects_to_clone()
