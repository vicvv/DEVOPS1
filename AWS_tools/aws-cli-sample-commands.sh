# install -- aws.amazon.com/cli

# verify aws cli
aws --version

# NOTE: if first time using awscli, run aws --configure
# add your IAM user key information and AWS region

# list s3 buckets, good way to test awscli basic configuration
aws s3 ls

# for Security - return CloudTrail information
aws cloudtrail describe-trails --trail-name-list demo

# for Security - return CloudWatch dashboard information
aws cloudwatch get-dashboard --dashboard-name 'Monitoring'

# for Compliance - return CloudWatch alarm information
aws cloudwatch describe-alarm-history

