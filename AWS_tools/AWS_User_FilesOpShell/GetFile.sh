#!/bin/bash
echo "The script will compare user password with the user passwrd on AWS."
echo "If password is a match then download the key-value from user bucket on AWS to local dir."
echo " "
# procesing parameters
if [ $# = 3 ]; then
    echo "Your command line contains $# arguments $1, $2, $3"
    user=$1
    password=$2
    file_to_download=$3
    
else
    echo "Some arguments are missing: need user, passwrod and file to download!"
    echo "Usage: $0 user password file_to_download"
    exit 1   
fi

# declaring vars
REGION='us-west-1'
ALLUSERSBUCKET="shellallusersb"
RAND=$(date |md5 | head -c8)


if [ -f "$file_to_download" ]; then
    echo "File $file_to_download found on local disk. Renaming..."   
    newfile=${RAND}_${file_to_download}; echo "to New file: $newfile "
    mv "$file_to_download" "$newfile"
    echo "File $file_to_download was renamed to $newfile"
fi

#getting all unique bucket prefixes
LPREFIX=$(aws s3 ls --recursive | cut -d" " -f 3| cut -d"-" -f1)

#echo $LPREFIX

# getting complete bucket name
#LALLBNAMES=$(aws s3 ls --recursive | cut -d" " -f 3)
LALLBNAMES=$(aws s3 ls --recursive | awk '{print substr($0, index($0,$3))}')
#echo $LALLBNAMES


if [[ $LPREFIX == *"$ALLUSERSBUCKET"* ]] && [[ $LPREFIX == *"$user"* ]]; then 
    ALL_BUCKET=$(echo "$LALLBNAMES" | grep "$ALLUSERSBUCKET-")
    echo "Available All Users bucket: $ALL_BUCKET"
    USER_BUCKET=$(echo "$LALLBNAMES" | grep "$user-")
    echo "Availale bucket for $user: $USER_BUCKET"   
    uparms=$(aws s3 cp s3://${ALL_BUCKET}/${user} - )
    stringarray=($uparms)
        if [ "${stringarray[0]}" = "$password" ]; then
                    echo "passwords are ok. Downloading the file $file_to_download..."
                    aws s3 cp s3://"$USER_BUCKET/$file_to_download" .
                else
                    echo "passwords do not match! Exiting ..."              
        fi   
else
    echo "All users bucket or $user bucket does not exists! Exiting ... "
    exit 1         
fi



