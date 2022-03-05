#bash install.sh tests.csv

csv=$1
linenum=$(cat $csv | wc -l)
echo $linenum

declare -A module_project
declare -A project_sha
  for ((i=2;i<=$linenum;i++))
  do
    for eachline in $i
    do
	  #  (cut -d, -f1 $csv | uniq | sed '1d')
	  url=$(sed -n ${i}p $csv | cut -d "," -f1)
   	  sha=$(sed -n ${i}p $csv | cut -d "," -f2)
          project=${url##*/}
	  module=$(sed -n ${i}p $csv | cut -d "," -f3)
   	  echo $project
          echo $sha
	  echo $module
          
          modulename=${module// /_}
	  projectname=${project// /_}
          if [ ! -v project_sha[$projectname] ];then
                 project_sha[$projectname]=$sha
          fi

	  if [ ! -v module_project[$modulename] ];then
		 module_project[$modulename]=$projectname
	  fi
          echo $modulename
    done
  done

    for project in $(echo ${!project_sha[*]})
    do
	sha=${project_sha[$project]}
        echo $project
	echo $sha  
     	cd $project
        mkdir OD_result
	#${sha%?}
        git checkout $sha | tee -a $(pwd)/OD_result/git_branch_result.txt
	mvn install -DskipTests | tee -a $(pwd)/OD_result/install_project.txt
        pass=0
	install_result=$(grep -n "BUILD SUCCESS" $(pwd)/OD_result/install_project.txt)
	if [[ $install_result ]]; then
		echo "$project,$sha,Success" >>$../../OD_result/compile_project.csv
		pass=1
	else echo "$project,$sha,Failure" >>$../../OD_result/compile_project.csv
	fi
	if [[ pass==1 ]]; then
		mvn test | tee -a $(pwd)/OD_result/run_test_suite.txt
		test_suite=$(grep -n "BUILD SUCCESS" $(pwd)/OD_result/run_test_suite.txt)
        	if [[ $test_suite ]]; then
                	echo "$project,$sha,Success" >>../../OD_result/test_suite.csv
        	else echo "$project,$sha,Failure" >>../../OD_result/test_suite.csv
       		fi
	else
		echo "$project,$sha,Failure" >>../../OD_result/test_suite.csv
	fi
	cd ..
    done	
    
    #Make sure the modules in which tests located can be compiled
    for module in $(echo ${!module_project[*]})
    do
	echo $module
	project=${module_project[$module]}     
        cd $project
        mvn -pl $module -am install -DskipTests -l $(pwd)/OD_result/install_modules.txt
	module_result=0
	module_result=$(grep -n "BUILD SUCCESS" $(pwd)/OD_result/install_modules.txt)
        if [[ $module_result ]]; then
                echo "$project,$sha,$module,Success" >>../../OD_result/compile_modules.csv
        else echo "$project,$sha,$module,Failure" >>../../OD_result/compile_modules.csv
        fi
        rm -rf OD_result
	cd ..
    done
