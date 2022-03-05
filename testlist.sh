#bash testlist.sh project module OD-test

project=$1
module=$2
ODtest=$3

echo script version: $(git rev-parse HEAD)
echo script running date: $(date)
md5=$(echo $(date) | md5sum | cut -d' ' -f1)
echo $md5

surefirereports=$project'/'$module'/target/surefire-reports'
echo "Surefire reports folder: "$surefirereports

cd $surefirereports
TEST_xml_files=$(find -name "TEST-*.xml")

module_test_file=$module$md5'.csv'
brittle_victim_file='result'$md5'.csv'
echo "All tests in module " $module "are saved in" $module_test_file
echo "Category of OD tests are saved in "$brittle_victim_file

#rm ../../../$module_test_file
echo "test,result,time" >../../../$module_test_file


ODtest_method=${ODtest##*.}
tmp_ODtest_class=${ODtest%%$ODtest_method}
ODtest_class=${tmp_ODtest_class%%.}
ODtest_final_name=$ODtest_class'#'$ODtest_method
echo To find all relavent tests for target test: $ODtest_final_name


for each_xml_file in $TEST_xml_files; do
	each_result_xml=${each_xml_file#*-}
	testclass=${each_result_xml%%.xml*}
        xmlpath=$(pwd)/'TEST-'$testclass'.xml'

	#Get all test running results 
	python3 ~/iFixFlakies_improvement/parse_result.py $xmlpath >> ../../../$module_test_file 
done


cd ../../..
linenum=$(cat $module_test_file | wc -l)


for ((i=2;i<=$linenum;i++)) 
do
    test_full_name=$(sed -n ${i}p $module_test_file | cut -d "," -f1)    
    test_method_name=${test_full_name##*.}
    tmp_test_classname=${test_full_name%%$test_method_name}
    test_classname=${tmp_test_classname%%.}
    test_final_name=$test_classname'#'$test_method_name

    echo Test full path  $test_final_name

    testxmlpath=$module'/target/surefire-reports/TEST-'$test_classname'.xml'
    ODxmlpath=$module'/target/surefire-reports/TEST-'$ODtest_class'.xml'

    rm $(pwd)/$testxmlpath
    rm $(pwd)/$ODxmlpath
    mvn -pl $module test -Dsurefire.runOrder=testorder -Dtest=$test_final_name,$ODtest_final_name >> run-order-tests-$test_method_name$ODtest_method$md5.log
    totaltime=$(grep -n "Total time:" run-order-tests-$test_method_name$ODtest_method$md5.log | cut -d':' -f3)
    echo Running tests $test_final_name $ODtest_final_name time: $totaltime
    
    testresult=$(python3 ~/iFixFlakies_improvement/parse_result.py $(pwd)/$testxmlpath) #>> $brittle_victim_file)
    echo $testresult
    odresult=$(python3 ~/iFixFlakies_improvement/parse_result.py $(pwd)/$ODxmlpath) #>> $brittle_victim_file
    echo $odresult
    
    save_file='FinalResult'$md5'.csv'
    echo 1st testName,result,time,target OD test,result,time >> $save_file
    echo $testresult,$odresult >> $save_file
    
done
