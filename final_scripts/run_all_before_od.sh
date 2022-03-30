project=$1
module=$2
test_one=$3
test_two=$4
md5_str=$5

mkdir -p $(pwd)/xml_test_log

echo $(pwd)
cd ./ifixflakies_run_idoft/projects
cd $project
mvn -pl $module test -Dsurefire.runOrder=testorder -Dtest=$test_one,$test_two | tee ../../../xml_test_log/ter$md5.log
cd ..
