#bash clone.sh URLSha.csv

dataset=$1

for i in $(cut -d, -f1 $dataset | uniq | sed '1d'); do
    cd iFixFlakies_improvement
    git clone $i
    cd -
done
