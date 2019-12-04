H9 contains 2 esential files:

- AWS_9_Tomcat.py
- AWS_helper.py

One file to free the AWS resources:

- delete_instances.py

One README.txt file

Web App directory MyApp with html, css and js files.

The main script AWS_H9_Tomcat imports the class from AWS_H_helper.
Please see comments for each method in the AWS_H_helper file.

The file takes 8 parameters, starts 2 instances in 2 diferent regions, updates the OS,
installs Tomcat, starts Tomcat and moves MyApp under the Tomcat. If requires the AWS
resources can be free by running the delete_instances method (see uncomment part) or
runnig separate delete_instances.py script.



