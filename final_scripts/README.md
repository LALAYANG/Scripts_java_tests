# Requirements:
## python 3.8
```
pip install bs4
pip install lxml
```
## maven-surefire
https://github.com/TestingResearchIllinois/maven-surefire

# File structure
## Scripts
```
├── get_modules.py
    Collect all the projects and modules with OD tests from iDoFT.
├── install_projects.sh
    Clone and install the projects.
├── run_tests_mods.sh
    Install these modules and meanwhile run the tests in them.
├── collect_all_tests.py
    Collect all the tests from the modules.
├── final_pair.py
    Get all the pairs<test_in_the_same_module,OD_test> to run.
├── final_run_pairs.py
    Run all the pairs and get the final result.
└── run_all_before_od.sh
    A script called to run two tests in order.
```

## All files (including input, scripts and results after all scripts are run)
```
├── get_modules.py
├── install_projects.sh
├── run_tests_mods.sh
├── collect_all_tests.py
├── final_pair.py
├── final_run_pairs.py
├── run_all_before_od.sh

├── pr-data.csv
    Input file from iDoFT.

├── projects_modules.csv
    All modules and projects with OD tests.
├── all_od_tests.csv
    All OD tests collected from iDoFT.
├── all_tests_query.csv
    All tests in each module.
├── paired_tests.csv
    All test pairs<test_in_the_same_module,OD_test>.
├── xml_dir.csv
    A record of locations of surefire-reports.
├── xml_test_log
    ├── 00e2cb9e55db990a994b4dd749227dc1_1.xml
    ├── 00e2cb9e55db990a994b4dd749227dc1_2.xml
    └── ...
    All surefire-reports are moved into this directory. For each test pair, there is a MD5. For the 1st test, its name is MD5_1.xml, the name of the 2nd test is MD5_2.xml.
├── ifixflakies_run_idoft
    ├── projects: Cloned projects.
    ├── install_project_log: Logs for installation of the projects.
    ├── module_install_log: Logs for running tests of the modules.
    ├── clone_log: A log for cloning projects.
    └── compile_project.csv: A file to record success/failure when cloning projects.
└── final_result.csv
    Final result. 
    In the format of: URL, SHA, module, 1st test, 1st test result, 1st test time, 2nd test (OD test), 2nd test result, 2nd test time, MD5
    e.g., https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.helper.FieldTest.test2,pass,0,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,pass,3.462,3146513902aa1807e09d1de4629b4ccf

```

# Example
Here is an example of one line from idoft. 

# Steps

1. get all the od tests and projects to install  
- usage: `python3 get_modules.py ./pr-data.csv`
- input:
```
./pr-data.csv
```
- output:
```
./projects_modules.csv
./all_od_tests.csv
```
2. install all the projects
- usage: `bash ./install_projects.sh $(pwd)/projects_modules.csv`
- output:
```
./ifixflakies_run_idoft/clone_log
./ifixflakies_run_idoft/compile_project.csv
./ifixflakies_run_idoft/install_project_log
```

3. intsall all the modules 
- usage: `bash ./run_tests_mods.sh $(pwd)/projects_modules.csv`
- output: 
```
./xml_dir.csv
./ifixflakies_run_idoft/module_install_log
```
4. collect all tests in these modules
- usage: `python3 collect_all_tests.py`
- output: 
```
./all_tests.query.csv
```
5. pair all the tests
- usage: `python3 final_pair.py`
- output：
```
./paired_tests.csv
```
6. run all the pairs and get final results
- usage: `python3 final_run_pairs.py`
- output：
```
./final_result.csv
./xml_test_log
```
