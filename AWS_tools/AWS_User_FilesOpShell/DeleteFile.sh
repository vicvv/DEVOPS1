!/bin/bash
echo "The script will compare user password with the user passwrd on AWS."
echo "If password is a match then delete the file."
echo " "

# procesing parameters
if [ $# = 3 ]; then
    echo "Your command line contains $# arguments $1, $2, $3"
    user=$1
    password=$2
    file_to_delete=$3
    echo $file_to_delete
    
else
    echo "Some arguments are missing: need user, passwrod and file to delete!"
    echo "Usage: $0 user password file_to_delete"
    exit 1   
fi

# declaring vars
REGION='us-west-1'
ALLUSERSBUCKET="shellallusersb"

#getting all unique bucket prefixes
LPREFIX=$(aws s3 ls --recursive | cut -d" " -f 3| cut -d"-" -f1)
#echo $LPREFIX

# getting complete bucket name
# LALLBNAMES=$(aws s3 ls --recursive | cut -d" " -f 3)
LALLBNAMES=$(aws s3 ls --recursive | awk '{print substr($0, index($0,$3))}')
#echo $LALLBNAMES


if [[ $LPREFIX == *"$ALLUSERSBUCKET"* ]] && [[ $LPREFIX == *"$user"* ]]; then 
    ALL_BUCKET=$(echo "$LALLBNAMES" | grep "$ALLUSERSBUCKET-")
    echo "Available All Users bucket: $ALL_BUCKET"
    USER_BUCKET=$(echo "$LALLBNAMES" | grep "$user-")
    echo "Availale bucket for $user: $USER_BUCKET"   
    uparms=$(aws s3 cp s3://${ALL_BUCKET}/${user} - )
    stringarray=($uparms)
        if [ "${stringarray[0]}"  = "$password" ]; then
            echo "passwords are ok. Deleting the file $file_to_delete..."
            #exists=$(aws s3 ls s3://$USER_BUCKET/$file_to_delete | grep -oE '[^ ]+$')
            exists=$(aws s3 ls s3://$USER_BUCKET/"$file_to_delete"| awk '{print substr($0, index($0,$4))}')
            echo "Exists $exists"        
                if [ "$file_to_delete" = "$exists" ]; then
                    aws s3 rm "s3://$USER_BUCKET/$file_to_delete"                      
                else
                    echo "$file_to_delete does not exists in bucket $USER_BUCKET"
                fi   
        else
            echo "passwords do not match! Exiting ..."
                           
        fi   
    else
        echo "All users bucket or $user bucket does not exists! Exiting ... "
        exit 1         
fi