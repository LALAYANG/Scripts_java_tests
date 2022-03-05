from bs4 import BeautifulSoup
import os
import sys
import csv


def get_output_xml_results(xml_file):
    with open(xml_file[1]) as fp:
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
                failedconstructor = str.format("{},{},{}", t, test_result, eachtest["time"])
                break
            else:
                t = str.format("{}.{}", eachtest["classname"], eachtest["name"])
                if t in tests:
                    t = str.format("{}.{}=DUPLICATE", eachtest["classname"], eachtest["name"])
                tests.add(t)
            tout.append(str.format("{},{},{}", t, test_result, eachtest["time"]))


        if failedconstructor != "":
            print(failedconstructor)
        else:
            for eachtest in tout:
                print(eachtest)
        
    #for each in tests:
     #  print(each)
       #print(tests)
'''
    module_test_list_file='testfor.csv'

    with open(module_test_list_file,"a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        #csv_writer.writerow(["moudle","test"])
        for each in tests:
            csv_writer.writerow([each])
'''

if __name__ == '__main__':
    get_output_xml_results(sys.argv)#sys.argv is xml_file
