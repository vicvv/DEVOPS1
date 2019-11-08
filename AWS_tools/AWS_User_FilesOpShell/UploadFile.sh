#!/bin/bash
echo "The script will compare user password with the user passwrd on AWS."
echo "If password is a match then the file will be uploaded."
echo "To upload files with spaces in the name provide the filename in quotes"
echo " "

# procesing parameters
if [ $# = 3 ]; then
    echo "Your command line contains $# arguments $1, $2, $3"
    user=$1
    password=$2
    file_to_upload=$3
    
else
    echo "Some arguments are missing: need user, passwrod and file to upload!"
    echo "Usage: $0 user password file_to_upload"
    exit 1   
fi


if [ ! -f "$file_to_upload" ]  2>&1; then
    echo "$file_to_upload does not exists. Exiting ..."
    exit 1
fi


# declaring vars
REGION='us-west-1'
ALLUSERSBUCKET="shellallusersb"

#getting all unique bucket prefixes
LPREFIX=$(aws s3 ls --recursive | cut -d" " -f 3| cut -d"-" -f1)
#echo $LPREFIX

# getting complete bucket name
#LALLBNAMES=$(aws s3 ls --recursive | cut -d" " -f 3)
LALLBNAMES=$(aws s3 ls --recursive | awk '{print substr($0, index($0,$3))}')
echo $LALLBNAMES

if [[ $LPREFIX == *"$ALLUSERSBUCKET"* ]]; then 
    ALL_BUCKET=$(echo "$LALLBNAMES" | grep "$ALLUSERSBUCKET-")
    echo "availale bucket: $ALL_BUCKET"
    else
        echo "There is no All users bucket! Exiting ... "
        exit 1

fi

if [[ $LPREFIX == *"$user"* ]]; then 
    echo "user $user bucket is available."
        USER_BUCKET=$(echo "$LALLBNAMES" | grep "$user-")
        echo "availale bucket: $USER_BUCKET"
        aws s3 cp s3://$ALL_BUCKET/$user s3://$USER_BUCKET/$user
        version=$(aws s3 --version)
        echo $version
        uparms=$(aws s3 cp s3://${ALL_BUCKET}/${user} - )
        echo $uparms
        stringarray=($uparms)
            if [ "${stringarray[0]}" = "$password" ]; then
                echo "passwords are ok. Uploading file $file_to_upload..."
                aws s3 cp "$file_to_upload" s3://$USER_BUCKET
                        
            else
                echo "passwords do not match! Exiting ..."
                aws s3 rm s3://$USER_BUCKET/$user                                       
            fi                  

    else
        echo "There is no bucket for user $user... exiting"
        exit 1
        
fi