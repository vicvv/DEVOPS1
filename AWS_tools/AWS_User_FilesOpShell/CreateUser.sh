#!/bin/bash
echo "The script will crete allusers bucket with prefix shellallusersb."
echo "All buckets will have unifided name structure such as prefix-sufix"
echo "Bucket's prefix will be equal to the user name. The sufix part is rundom."
echo "User name can not have a hyphen."
echo " "
# procesing parameters
if [ $# = 3 ]; then
    echo "Your command line contains $# arguments"
    user=$1
    password=$2
    email=$3
else    
    echo "Usage: $0 user password email"
    echo "There is something wrong with your command arguments"
    exit 1   
fi

# cant allaw the dash in user name 
if [[ $user == *"-"* ]]; then
  echo "User name can not have hyphen, exiting ..."
  exit 1
fi

# declaring vars
REGION='us-west-1'
ALLUSERSBUCKET="shellallusersb"
RAND=$(date |md5 | head -c8)


function create_bucket() {
    CHECK=$(aws s3 ls --recursive 2>&1| cut -d"-" -f 3| grep "$1$")
    #echo $CHECK
    echo $2

    if [ -z "$CHECK" ]; then                                                                                                                                                                                                                              
        aws s3 mb s3://$2
        echo "If this value is not 0 something went wrong: " $?
        
    else       
        #echo "create failed, maybe bucket exists??"
        B=$(aws s3 ls --recursive | cut -d" " -f 3| grep "$1")
        if [ ! -z B ]; then
            echo "found the following existing bucket: $B"
        else
            echo "Create bucket for $B failed!"
        fi
    fi
}

touch $user
echo "$password $email" > $user
value=`cat $user`
echo "The content of the  $user file: "
echo "$value"


# creating allusers bucket and individual user bucket if it does not exists

create_bucket "$ALLUSERSBUCKET" "$ALLUSERSBUCKET-$RAND"
create_bucket "$user" "$user-$RAND"


# getting name of allusers bucket
ALLUB=$(aws s3 ls --recursive | cut -d" " -f 3| grep "$ALLUSERSBUCKET")
echo "........................."
#echo $ALLUB

if [ ! -z "$ALLUB" ]; then                                                                                                                                                                                                                              
        echo "$ALLUB - allusers bucket found"
        aws s3 cp $user s3://$ALLUB 
        chmod 755 $user
        rm $user

    else
        echo "something is wrong. there is no alluser bucket!"
        exit 1
fi



                                       
