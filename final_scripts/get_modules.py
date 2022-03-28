# get all project-sha-module turples
# usage: python get_modules.py
# input: idoft/pr-data.csv
# output: projects_module.csv

import csv

idoft_pr_data_path = '../pr-data.csv'

output_projects_csv = '../projects_module.csv'

project_module_info = []

def get_projects_to_clone():
    pr_data = open(idoft_pr_data_path,"r")
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

get_projects_to_clone()
