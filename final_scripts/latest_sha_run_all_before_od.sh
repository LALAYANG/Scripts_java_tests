# checkout to the latest version
url=$1
project=$2
module=$3
test_1st_method=$4
od_test_method=$5
md5_str=$6


mkdir -p $(pwd)/ifixflakies_run_idoft
cd $(pwd)/ifixflakies_run_idoft
mkdir -p $(pwd)/install_project_log
mkdir -p $(pwd)/latest_projects
mkdir -p $(pwd)/xml_test_log
cd $(pwd)/latest_projects


#echo $(pwd)
#echo $project
rm -rf $project

#echo $url,$module
#echo Start to clone $project at: $(date) >> ../clone_log
timeout 600s git clone $url >> ../clone_log

# exit_status=${PIPESTATUS[0]}

# if [[ ${exit_status} -eq 124 ]] || [[ ${exit_status} -eq 137 ]]; then
#     echo "[ PROJECT ] $project not found." >> ../clone_log
#     echo "$project, not_found" >> error_projects.csv
#     continue
# fi
# if [[ ! -d $project ]]; then
#     echo "[ PROJECT ] $project not cloned." >> ../clone_log
#     echo "$project,fail_to_clone" >> error_projects.csv
#     continue
# fi	

cd $project 
#echo $(pwd) >> tee -a ../../clone_log
sha=$(git rev-parse HEAD)
echo $sha
#mvn install -DskipTests >> ../../install_project_log/install_$project.log

# install_result=$(grep -n "BUILD SUCCESS" ../../install_project_log/install_$project.log)
# if [[ $install_result ]]; then
#     echo "$project,$sha,Success" >> ../../compile_project.csv
# else echo "$project,$sha,Failure" >> ../../compile_project.csv
# fi


mvn -pl $module -am install -DskipTests > ../../module_install_log/install_$project$module.log
mvn -pl $module test -Dsurefire.runOrder=testorder -Dtest=$test_one,$test_two > ../../../xml_test_log/ter_$md5_str.log

cd ..
