# Google Cloud VM name, IP address and FDQN Report
# This script uses a service account to access the GCP API
# The service account is created in a project and then must be granted
# to other projects.  This is done by adding the service account to the
# IAM of the project.
import json
import googleapiclient.discovery
from google.oauth2 import service_account

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
    print("  ", "Project:",project['projectId'])
    # Code block for the list of VMs in the project per zone
    compute = googleapiclient.discovery.build('compute', 'v1', credentials=myCredentials)
    zones = compute.zones().list(project=project['projectId']).execute().get('items', [])
    for zone in zones:
        instances = list_instances(compute, project['projectId'], zone['name'])
        if instances:
            for instance in instances:
                # Get the internal FQDN
                try:
                    internalFQDN = instance['name'] + "." + project['projectId'] + ".internal"
                except KeyError:
                    internalFQDN = 'None'
                # Create FQDN using appsot.com from Google's App Engine
                FQDN=instance['name'] + '.' + project['projectId'] + '.appspot.com'
                try:
                    publicIP = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
                except KeyError:
                    publicIP = 'None'
                privateIP = instance['networkInterfaces'][0]['networkIP']
                zoneName = zone['name']
                instanceName = instance['name']
                print("    ", "zone:", zoneName, "VM Name:", instanceName, "Private IP:", privateIP, "Public IP:", publicIP, "FQDN:", FQDN)
                # internal FQDN is how VMs in same VPC communicate
                # https://cloud.google.com/compute/docs/internal-dns
                # print("      ", "Internal FQDN:", internalFQDN)
    print("*****")
print("*********************************")




