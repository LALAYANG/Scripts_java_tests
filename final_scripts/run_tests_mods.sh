#compile modules in idoft and collect all tests in the specific module
#usage:

projects_to_install=$1

mkdir -p $(pwd)/ifixflakies_run_idoft/module_install_log
cd $(pwd)/ifixflakies_run_idoft/projects

linenum=$(cat $projects_to_install | wc -l)
echo $linenum

for ((i=1;i<=$linenum;i++));do
    for item in $i;do
        url=$(sed -n ${i}p $projects_to_install | cut -d "," -f1)
   	    sha=$(sed -n ${i}p $projects_to_install | cut -d "," -f2)
        project=${url##*/}
	    module=$(sed -n ${i}p $projects_to_install | cut -d "," -f3)

        if [[ ! -d $project ]]; then
            echo "[ PROJECT ] $project doesn't exist." | tee -a ../module_install.log
            echo "$project,$module,project does not exist" >> error_module_install.csv
            continue
        fi

        cd $project
        mvn -pl $module -am install | tee ../../module_install_log/install_$project$module.log
        xml_dir=$(grep -a "for the individual tes" ../../module_install_log/install_$project$module.log)
        temp=${xml_dir#*to }
	#echo $temp | cut -d" " -f1 >>temp.log
	echo $url,$sha,$project,$module,$temp | cut -d" " -f1 >>../../xml_dir.csv
        cd ..
    done
done 
