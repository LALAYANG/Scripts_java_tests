import csv

share_csv='F:/share/IM-NI-status.csv'
idoft_csv='F:/idoft/pr-data.csv'
ODtests_csv='F:/OD/tests.csv'

share_dict={}


def process_csv(share_csv):
    share_reader = csv.reader(open(share_csv))
    idoft_reader = csv.reader(open(idoft_csv))
    for sharerow in share_reader:
        if sharerow[0] not in share_dict:
            share_dict[sharerow[0]] = sharerow[1]
    with open(ODtests_csv, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["URL","SHA","Module","Test name","Caqtegory","Status","PR Link","Notes"])

        for idoftrow in idoft_reader:
            if idoftrow[0] in share_dict:
                if idoftrow[1] == share_dict[idoftrow[0]]:
                    if "OD" in idoftrow[4] and 'NOD' not in idoftrow[4]:
                        csv_writer.writerow(idoftrow)

if __name__ == '__main__':
    process_csv(share_csv)
