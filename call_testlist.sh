#bash call_testlist.sh data.csv 

csv=$1
linenum=$(cat $csv | wc -l)

echo script version: $(git rev-parse HEAD)
echo script running date: $(date)
md5=$(echo $(date) | md5sum | cut -d' ' -f1)
echo $md5

for ((i=2;i<=$linenum;i++))
do
    url=$(sed -n ${i}p $csv | cut -d "," -f1)
    module=$(sed -n ${i}p $csv | cut -d "," -f3)
    test=$(sed -n ${i}p $csv | cut -d "," -f4)
    category=$(sed -n ${i}p $csv | cut -d "," -f5)
    project=${url##*/}


    if [[ $category=='OD' ]]; then
	bash testlist.sh $project $module $test >> call_testlist$md5.log
    fi
done
