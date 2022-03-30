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
├── run_all_before_od.sh
    A script called to run two tests in order.
├── latest_sha_run_all_before_od.sh
    A script for verifying flaky tests in the latest version.
└── run_latest_sha.py
    A script for verifying flaky tests in the latest version.
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
├── latest_sha_run_all_before_od.sh
├── run_latest_sha.py

├── pr-data.csv
    Input file from iDoFT. The input file can be any lines of iDoFT/pr-data.csv.

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
Here is an example output of one line from idoft. 
- Input:
```
https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,OD,,,https://github.com/TestingResearchIllinois/idoft/issues/90
```
- Output: In `final_result.csv`,
```
URL, SHA, module, 1st test, 1st test result, 1st test time, 2nd test (OD test), 2nd test result, 2nd test time, MD5
...
16 https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.user.TestBasic.testUpdateByPrimaryKey,pass,2.989,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,pass,0.016,b35ca3f1da69b8ed2ec14dddb1dc1c52
17 https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.user.TestBasic.testDelete,pass,2.971,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,pass,0.001,84dd75154078ecfc93214d3822872dbf
18 https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.user.TestBasic.testInsert,pass,2.866,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,failure,0.005,f1f63888bac79e887b516512f48bc1bf
19 https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.user.TestBasic.testSelect,pass,2.978,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,pass,0.006,646ca4e5b0eb757b64d2eee32274facd
20 https://github.com/abel533/Mapper,3c0b3307011fad53f811e08d05147d94fc6c0d67,base,tk.mybatis.mapper.test.country.TestInsert.testDynamicInsertNull,pass,0.002,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,pass,3.09,a0a121d2653b302c45432eaaee80ebf1
...
```
We can see in line 18, column 5 is 'pass', column 8 is 'failure', that means test `tk.mybatis.mapper.test.able.TestBasicAble.testInsert` fails as a victim after test `tk.mybatis.mapper.test.user.TestBasic.testInsert` is run.
- To check whether this test is still flaky in the latest version: run `run_latest_sha.py` in the format of:
```
python3 run_latest_sha.py url project module test_1st od_test
```
e.g.,
```
python3 run_latest_sha.py https://github.com/abel533/Mapper Mapper base tk.mybatis.mapper.test.user.TestBasic.testInsert tk.mybatis.mapper.test.able.TestBasicAble.testInsert
```
- Output: In `./final_result_latest_sha.csv', we can check the result in the format of :
```
url,sha,module,1st test,1st test result,1st test time,2nd test,2nd test result,2nd test time,MD5
https://github.com/abel533/Mapper,3120d10848663c94dabd8bf14164b4dd61f865d5,base,tk.mybatis.mapper.test.user.TestBasic.testInsert,pass,0.008,tk.mybatis.mapper.test.able.TestBasicAble.testInsert,failure,0.009,3ece566fa75a83ba009a5deca8c67069
```
Still, in line 18, column 5 is 'pass', column 8 is 'failure', that means test `tk.mybatis.mapper.test.able.TestBasicAble.testInsert` fails as a victim in the latest version.



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
- output: in ./
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
