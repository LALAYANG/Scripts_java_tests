# Please check all files in `./final_scripts`


# Scripts_java_tests
Scripts for java flaky tests.

### ./preparation/clone.sh
- usage: `bash clone.sh URLSha.csv`
- clone all projects from a csv.
### ./preparation/install.sh
- usage: `bash install.sh tests.csv`
- install the cloned projects and check whether the modules in which tests located can be compiled.

### getODtests.py
- usage: `python3 getODtests.py`, need to change file paths in the script
- collect certain tests (e.g. OD tests) from idoft.

### parse_result.py 
- usage: `python3 parse_result.py xml_file`
- parse test results from .xml files.

### run_tests_order.sh
- usage: `sh run_tests_order.sh project module test_1st_method od_test_method md5_str`
- to run tests in order

### run_tests_order.py 
- usage: `python3 run_tests_order.py`, need to change file paths in the script
- read tests from a csv and run them
- function `get_output_xml_results` can also be used to collect test results from .xml files.

### testlist.sh
- usage: `bash testlist.sh project module OD-test`
- get tests in certain module and run them before a target OD test

### call_testlist.sh
- usage: `bash call_testlist.sh data.csv`
- Automatically call testlist.sh
