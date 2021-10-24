#export FLASK_APP=main
#flask run
while getopts a:p:n:s: flag
do
    case "${flag}" in
        a) address=${OPTARG};;
        p) port=${OPTARG};;
        n) db_user=${OPTARG};;
        s) db_pass=${OPTARG};;
    esac
done

python3 app.py -a $address -p $port -n $db_user -s $db_pass

