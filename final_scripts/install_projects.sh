#clone and install projects
#usage: bash ./ clone.sh projects.csv

projects_to_install=$1

mkdir -p $(pwd)/ifixflakies_run_idoft
cd $(pwd)/ifixflakies_run_idoft
mkdir -p $(pwd)/projects
cd $(pwd)/projects

linenum=$(cat $projects_to_install | wc -l)
echo $linenum

for ((i=1;i<=$linenum;i++));do
    for item in $i;do
        url=$(sed -n ${i}p $projects_to_install | cut -d "," -f1)
   	    sha=$(sed -n ${i}p $projects_to_install | cut -d "," -f2)
        project=${url##*/}
	    module=$(sed -n ${i}p $projects_to_install | cut -d "," -f3)

        rm -rf $project

	    echo $url,$sha,$module
        echo Start to clone $project at: $(date) | tee -a ../clone_log
        timeout 600s git clone $url | tee -a ../clone_log
        exit_status=${PIPESTATUS[0]}

        if [[ ${exit_status} -eq 124 ]] || [[ ${exit_status} -eq 137 ]]; then
            echo "[ PROJECT ] $project not found." | tee -a ../clone_log
            echo "$project, not_found" >> error_projects.csv
            continue
        fi
        if [[ ! -d $project ]]; then
            echo "[ PROJECT ] $project not cloned." | tee -a ../clone_log
            echo "$project,fail_to_clone" >> error_projects.csv
            continue
        fi
	

        cd $project 
	    echo $(pwd) | tee -a ../../clone_log
        git checkout $sha | tee -a ../../clone_log

        mvn install -DskipTests | tee -a ../../install_project.log
        install_result=$(grep -n "BUILD SUCCESS" ../../install_project.log)
        if [[ $install_result ]]; then
            echo "$project,$sha,Success" >> ../../compile_project.csv
        else echo "$project,$sha,Failure" >> ../../compile_project.csv
        fi

        cd ..
    done
done
