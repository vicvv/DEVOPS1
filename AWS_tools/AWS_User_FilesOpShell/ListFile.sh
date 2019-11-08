echo "The script will list user key located in all users bucket."
echo "And keys that are in the users bucket."
echo " "

# procesing parameters
if [ $# = 2 ]; then
    echo "Your command line contains $# arguments $1, $2"
    user=$1
    password=$2
    
else
    echo "Some arguments are missing: need user, passwrod!"
    echo "Usage: $0 user password "
    exit 1   
fi

REGION='us-west-1'
ALLUSERSBUCKET="shellallusersb"

#getting all unique bucket prefixes
LPREFIX=$(aws s3 ls --recursive | cut -d" " -f 3| cut -d"-" -f1)
#echo $LPREFIX

# getting complete bucket name
#LALLBNAMES=$(aws s3 ls --recursive | cut -d" " -f 3)
LALLBNAMES=$(aws s3 ls --recursive | awk '{print substr($0, index($0,$3))}')
#echo $LALLBNAMES


# detecting all users bucket name
if [[ $LPREFIX == *"$ALLUSERSBUCKET"* ]] && [[ $LPREFIX == *"$user"* ]]; then 
    ALL_BUCKET=$(echo "$LALLBNAMES" | grep "$ALLUSERSBUCKET-")
    USER_BUCKET=$(echo "$LALLBNAMES" | grep "$user-")
    echo $USER_BUCKET
    echo "Listing $user file that is located in All Users Bucket"
    uparms=$(aws s3 cp s3://${ALL_BUCKET}/${user} - )
    stringarray=($uparms)
        if [ "${stringarray[0]}" = "$password" ]; then
            echo "passwords are checked! Listing the $user file locaded in All Users bucket: $ALL_BUCKET"
            UFILE=$(aws s3 ls s3://$ALL_BUCKET/$user | grep "$user$" | grep -oE '[^ ]+$')
            echo "user file: .... $UFILE"
            if [ -z "$UFILE" ]; then
                echo "There is no file for User $user in $ALL_BUCKET"
                echo " "
            else 
                echo "User $user file in All Users bucket folder:"
                echo "$UFILE"
            fi
            #UBUCKETFILES=$(aws s3 ls s3://$USER_BUCKET | grep -oE '[^ ]+$')
            UBUCKETFILES=$(aws s3 ls s3://$USER_BUCKET | awk '{print substr($0, index($0,$4))}')
            if [ -z "$UBUCKETFILES" ]; then
                echo "There are no files in $USER_BUCKET! Upload somehting first!"
                echo " "
            else 
                echo "User $user files in $USER_BUCKET"
                echo "$UBUCKETFILES"
            fi
                             
        else
            echo "passwords do not match! Exiting ..."
             
        fi  
else
    echo "All Users bucket or User's bucket are missing! Exiting ... "
    exit 1

fi

