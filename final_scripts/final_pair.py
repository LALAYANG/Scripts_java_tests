import csv

all_tests_csv = './all_tests_query.csv'
od_tests_csv = './all_od_tests.csv'

save_result= './paired_tests.csv'
all = []
od = []

def generate_final_data():
    final = []
    all_tests = open(all_tests_csv,"r")
    all_tests_reader = csv.reader(all_tests)

    od_tests = open(od_tests_csv,"r")
    od_tests_reader = csv.reader(od_tests)

    for eachline in od_tests_reader:
        for eachitem in all_tests_reader:
 #           print(eachline[0:3],eachitem[0:3])
            if eachline[0:3] == eachitem[0:3]:
               # print(eachitem[0:3])
                temp = eachitem[0:5]
                temp.append(eachline[3])
                temp.append(eachline[-1])
                final.append(temp)

    print(len(final))
    num=0
    with open(save_result,"w",newline='') as result_csv:
        writer = csv.writer(result_csv)
        for each in final:
            writer.writerow(each)


generate_final_data()
