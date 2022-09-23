# Google Cloud VM name, IP address and FDQN Report
# Required: pip3 install google-api-python-client
# Required: pip3 install google-auth
# Required: pip3 install google-auth-httplib2
# Required: pip3 install google-auth-oauthlib
# Required: pip3 install google-cloud
# pip3 install --upgrade google-cloud-storage
import os
import sys
import json
import googleapiclient.discovery
from google.oauth2 import service_account
from google.cloud import storage
import google.auth

# Get Credentials
myCredentials = service_account.Credentials.from_service_account_file('Org-SA_keys.json')


# Code block for the list of all projects in the Organization
def list_projects(organization_id):
    service = googleapiclient.discovery.build('cloudresourcemanager', 'v1', credentials=myCredentials)
    request = service.projects().list(filter='parent.id:' + organization_id)
    response = request.execute()
    return response['projects']

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None
print("Welcome to the GCP Organization VM Name, IP and FQDN Report")
print("To get started, please enter the GCP Organization ID: ")
organization_id = input()
print("*********************************")
# Ask for the Organization ID
# organization_id = input("Enter the Organization ID: ")
# Call the list_projects function
projects = list_projects(organization_id)
# Print the list of projects in the Organization
print('Projects in Organization:')
for project in projects:
    print(project['projectId'])
print("*********************************")
# List all the VM's in all the projects in the Organization
print('All the VM''s in all the Projects in the Organization:')
for project in projects:
    print("  ", project['projectId'])
    # Code block for the list of VMs in the project
    compute = googleapiclient.discovery.build('compute', 'v1', credentials=myCredentials)
    zones = compute.zones().list(project=project['projectId']).execute().get('items', [])
    for zone in zones:
        instances = list_instances(compute, project['projectId'], zone['name'])
        if instances:
            for instance in instances:
                FQDN=instance['name'] + '.' + project['projectId'] + '.appspot.com'
                print("    ", zone['name'], instance['name'], instance['networkInterfaces'][0]['networkIP'], FQDN)
                # print the FQDN of the VM
                # print('FQDN: ' + instance['name'] + '.' + project['projectId'] + '.appspot.com')
    print("*****")
print("*********************************")
# Code block to list the VM's
# credentials = service_account.Credentials.from_service_account_file('Org-SA_keys.json')
# compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

list_instances(compute, "opencti-id", "us-east1-b")
# End of code block to list the VM's

# Code block to the list of the GCP Buckets in GCS
# storage_client = storage.Client.from_service_account_json('Org-SA_keys.json')
# buckets = list(storage_client.list_buckets())
# print(buckets)




