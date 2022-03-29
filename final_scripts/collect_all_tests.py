from bs4 import BeautifulSoup
import os
import sys
import csv

xml_dir_csv = './xml_dir.csv'

output_all_tests_csv = './all_tests_query.csv'

all_results = []

def get_all_xml():
    xml_dir = open(xml_dir_csv,"r")
    xml_dir_reader = csv.reader(xml_dir)

    for eachline in xml_dir_reader:
        dir = eachline[4]
        sha = eachline[1]
        files = os.listdir(eachline[4])
        project = eachline[2]
        module = eachline[3]
        url = eachline[0]
        print(dir)
        for eachfile in files:
            #print(eachfile)
            file_path = os.path.join(dir, eachfile)
            if ".xml" in file_path:
                print(file_path)
                get_all_tests(url,project, sha, module, file_path)


def get_all_tests(url,project,sha,module,xml_file):
    with open(xml_file) as fp:
        xml_content = BeautifulSoup(fp, features="xml")
        tout = []
        failedconstructor = ""
        tests = set()
        for eachtest in xml_content.testsuite.findAll("testcase"):
            test_result = "unknown"

            if eachtest.find('failure'):
                test_result = "failure"
            elif eachtest.find('error'):
                test_result = "error"
            else:
                test_result = "pass"

            if eachtest["name"] == eachtest["classname"] or eachtest["name"] == "":
                t = xml_file[3]
                failedconstructor = str.format("{},{},{},{},{},{},{}", url, sha, module, project, t, test_result, eachtest["time"])
                break
            else:
                t = str.format("{}.{}", eachtest["classname"], eachtest["name"])
                if t in tests:
                    t = str.format("{}.{}=DUPLICATE", eachtest["classname"], eachtest["name"])
                tests.add(t)

            tout.append(str.format("{},{},{},{},{},{},{}", url, sha, module, project, t, test_result, eachtest["time"]))

        if failedconstructor != "":
            print(failedconstructor)
            all_results.append(failedconstructor)
        else:
            for eachtest in tout:
                print(eachtest)
                all_results.append(eachtest)

    with open(output_all_tests_csv,"w",newline='') as tests_csv:
        writer = csv.writer(tests_csv)
        for each in all_results:
            writer.writerow(each.split(','))

get_all_xml()
