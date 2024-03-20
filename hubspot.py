import requests
from dotenv import load_dotenv
import os
load_dotenv()

class HubSpotClient:
    def __init__(self):
        self.api_key = os.getenv("HUBSPOT_API_KEY")
        self.base_url = 'https://api.hubapi.com/crm/v3/objects/contacts'

    def create_contact(self, contact_data):
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        response = requests.post(self.base_url, headers=headers, json=contact_data)
        print("Create contact response status code:", response.status_code)
        print("Create contact response content:", response.content)
        return response

    def get_contacts(self):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(self.base_url, headers=headers)
        return response.json().get('results', [])
    def get_contact_by_name(self, first_name):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {
            'properties': ['email', 'firstname', 'lastname','phone','key_information','hs_lead_status','user_messages'],
            'filterGroups': [
                {
                    'filters': [
                        {'value': first_name, 'propertyName': 'firstname', 'operator': 'EQ'}
                    ]
                }
            ]
        }
        response = requests.post(f'{self.base_url}/search', headers=headers, json=params)
        return response.json().get('results', [])
    def get_contact_by_email(self, email):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {
            'properties': ['email', 'firstname', 'lastname', 'phone', 'key_information', 'hs_lead_status', 'user_messages'],
            'filterGroups': [
                {
                    'filters': [
                        {'value': email, 'propertyName': 'email', 'operator': 'EQ'}
                    ]
                }
            ]
        }
        response = requests.post(f'{self.base_url}/search', headers=headers, json=params)
        return response.json().get('results', [])

    def update_contact(self, contact_id, key_information=None, hs_lead_status=None, user_messages=None):
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        endpoint = f'{self.base_url}/{contact_id}'
        
        # Constructing the data dictionary
        contact_data = {'properties': {}}
        if key_information is not None:
            contact_data['properties']['key_information'] = key_information
        if hs_lead_status is not None:
            contact_data['properties']['hs_lead_status'] = hs_lead_status
        if user_messages is not None:
            contact_data['properties']['user_messages'] = user_messages
        
        # Sending the PATCH request
        response = requests.patch(endpoint, headers=headers, json=contact_data)
        return response



    def delete_contact(self, contact_id):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        endpoint = f'{self.base_url}/{contact_id}'
        response = requests.delete(endpoint, headers=headers)
        return response
    def get_properties(self):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        endpoint = f'{self.base_url}/properties'
        response = requests.get(endpoint, headers=headers)
        return response.json()

    
if __name__ == "__main__":
    hubspot_client = HubSpotClient()
    result = hubspot_client.update_contact('5145719838', key_information='key information test 2', hs_lead_status="IN_PROGRESS", user_messages='this is a user message')
    print("Update contact response:", result.status_code)
    print("Update contact response:", result.content)

    # result = hubspot_client.get_contact_by_name('john')
    # print("result",result)

    # result = hubspot_client.get_properties()
    # print(result)
    # # result = hubspot_client.get_contacts()
    # user_messages = result[0]['id']

    # print("User Messages:", user_messages)
    #     # Create a new contact
#     new_contact_data = {
#     "properties": {
#         "email": "email@example.com",
#         "firstname": "John",
#         "lastname": "Doe"
#     }
# }
#     response = hubspot_client.create_contact(new_contact_data)
#     print("Create contact response:", response.status_code)

#     # Get all contacts
#     contacts = hubspot_client.get_contacts()
#     if contacts:
#         print("Contacts:",'\n')
#         for contact in contacts:
#             print(contact, '\n')

    # # Update a contact (assuming you have contact_id)
    # contact_id = 'CONTACT_ID_TO_UPDATE'
    # updated_contact_data = {"properties": [{"name": "firstname", "value": "John"}]}
    # response = hubspot_client.update_contact(contact_id, updated_contact_data)
    # print("Update contact response:", response.status_code)

    # # Delete a contact (assuming you have contact_id)
    # response = hubspot_client.delete_contact(contact_id)
    # print("Delete contact response:", response.status_code)