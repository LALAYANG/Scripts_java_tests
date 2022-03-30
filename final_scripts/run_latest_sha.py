#input: url, project, module, test1,test2

import csv
import os
import sys
from hashlib import md5
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE

test_before_od_csv = './paired_tests.csv'
save_csv = './final_result_latest_sha.csv'

def get_output_xml_results(testcase_name, xml_file):
    #os.system('echo $(pwd)')
    try:
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
                    failedconstructor = str.format("{},{},{}", t, test_result, eachtest["time"])
                    break
                else:
                    t = str.format("{}.{}", eachtest["classname"], eachtest["name"])
                    if t in tests:
                        t = str.format("{}.{}=DUPLICATE", eachtest["classname"], eachtest["name"])
                    tests.add(t)
                tout.append(str.format("{},{},{}", t, test_result, eachtest["time"]))


            if failedconstructor != "":
                return failedconstructor
            else:
                for eachtest in tout:
                    #print(eachtest)
                    if testcase_name in eachtest:
                        return eachtest
            return 'ERROR_Parse'
            
    except FileNotFoundError:
        return 'test not found'


def run_All_tests(url,project,module,test_1st,od_test):

    hash_md5 = md5()
    with open(save_csv,"w",newline='') as save:
            writer = csv.writer(save)
            writer.writerow(['url','sha','module','1st test', '1st test result', '1st test time', '2nd test', '2nd test result', '2nd test time', 'MD5'])
    
    h_md5 = hash_md5.copy()
    h_md5.update(test_1st.encode())
    h_md5.update(od_test.encode())
    h_md5.update('latest sha'.encode())
    md5_str = h_md5.hexdigest()

    test_1st_method = test_1st[::-1].replace(".","#",1)[::-1]
    od_test_method = od_test[::-1].replace(".","#",1)[::-1]

    dir = './ifixflakies_run_idoft/latest_projects/'+project+'/'+module+'/target/surefire-reports/'

    xml_test_1st = dir +'TEST-'+'.'.join(test_1st.split('.')[0:-1])+'.xml'
    xml_od_test = dir +'TEST-'+'.'.join(od_test.split('.')[0:-1])+'.xml'
        #print(xml_test_1st,xml_od_test)
    if(os.path.isfile(xml_test_1st)): 
        os.remove(xml_test_1st)
    if(os.path.isfile(xml_od_test)):
        os.remove(xml_od_test)
    #print(url, project, module, test_1st_method, od_test_method, md5_str)
    #os.system('sh ./latest_sha_run_all_before_od.sh '+url+' '+project+' '+module+' '+test_1st_method+' '+od_test_method+' '+md5_str)
    mainargs = ["sh", "./latest_sha_run_all_before_od.sh", url, project, module, test_1st_method, od_test_method, md5_str]
    
    process = Popen(mainargs, stdout=PIPE, stderr=PIPE)
    std, err = process.communicate()
    sha = std.decode("utf-8").split('\n')[0]
    error = err.decode("utf-8")
    #print(sha,'~~~~~~~~~~~~',error)

    test_1st_result = get_output_xml_results(test_1st,xml_test_1st)
    test_od_result = get_output_xml_results(od_test,xml_od_test)
    if(os.path.isfile(xml_test_1st)):
        os.system('mv ' + xml_test_1st +' ./xml_test_log/'+md5_str+'_1.xml')
    if(os.path.isfile(xml_od_test)):
        os.system('mv ' + xml_od_test +' ./xml_test_log/'+md5_str+'_2.xml')
        
    final_result = [url,str(sha),module]
    for each in test_1st_result.split(','):
        final_result.append(each)
    for each in test_od_result.split(','):
        final_result.append(each)
    final_result.append(md5_str)

#        print(test_1st_result,test_od_result)

    with open(save_csv,"a",newline='') as save:
        writer = csv.writer(save)
        writer.writerow(final_result)

run_All_tests(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
