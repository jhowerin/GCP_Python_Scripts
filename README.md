### Google Cloud Python3 script to list all VM's in all Projects with the following information
VM zone <br>
VM internal IP <br>
VM external IP if configured <br>
VM FQDN - using appspot.com as the domain <br>

Requirements<br>
Access Google Cloud via a service account created in a project you specify. The service account key must be accesible via the file path specified in line 11 of the code. Then, add that service account to the Organization IAM with appropriate permissions - aka "compute viewer"

Security Reminder:
Do not share your service account key. Prevent inadvertently uploading to Github or other repos by using
a .gitignore file
### Please contact Jake Howering if needed - jhowerin@gmail.com
