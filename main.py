import requests
import json



def decode_unicode_escape(data):
    if isinstance(data, dict):
        return {key: decode_unicode_escape(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_unicode_escape(item) for item in data]
    elif isinstance(data, str):
        return data.encode('utf-8').decode('unicode_escape')
    return data


# Function to get access token
def get_access_token():




    url = "https://api.avito.ru/token"  # URL for token request
    payload = {
        'client_id': '***',  # Your client_id
        'client_secret': '***',  # Your client_secret
        'grant_type': '***'  # Grant type
    }

    # Send POST request to get access token
    response = requests.post(url, data=payload)
    response_code = response.status_code
    response_body = response.text

    print(f"Response Code: {response_code}")
    print(f"Response Body: {response_body}")

    # Parse JSON response to get access_token
    if response_code == 200:
        json_response = response.json()
        access_token = json_response.get('access_token')
        print(f"Access Token: {access_token}")
        return access_token
    else:
        print(f"Failed to get access token: {response_body}")
        return None


# Function to get chats using user_id and access_token
def get_chats(user_id, access_token):
    off = 0
    for i in range (0,15):
        off = i * 100
        url = f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats' +'?offset=' +  str(off) ;  # Chat URL
                #https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/
        # Headers with authorization token
        headers = {
            'Authorization': f'Bearer {access_token}'  # Authorization header with Bearer token
        }

        # Send GET request to fetch chats
        try:
            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"
            status_code = response.status_code
            response_body = response.text
            with open(f"file{str(off)}.txt", "a", encoding="utf-8") as file:
                file.write(response_body)
            exit()
            #  print(f'Status Code: {status_code}')
            print(f'Response Body: {response_body}')

            if status_code == 200:
                chats = (response.json())  # Parse response JSON
                print(chats)
                #return chats  # Return chats data
            else:
                print(f"Error fetching chats: {response_body}")
                #return None
        except Exception as e:
            print(f'Request failed: {str(e)}')
            #return None


# Function to get user info using access token
def get_user_info(access_token):
    url = 'https://api.avito.ru/core/v1/accounts/self'  # URL for user info request

    # Headers with authorization token
    headers = {
        'Authorization': f'Bearer {access_token}'  # Authorization header with Bearer token
    }

    # Send GET request to fetch user info
    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        response_body = response.text

        print(f'Status Code: {status_code}')
        print(f'Response Body: {response_body}')

        if status_code == 200:
            user_info = response.json()  # Parse response JSON
            return user_info  # Return user info
        else:
            print(f"Error fetching user info: {response_body}")
            return None
    except Exception as e:
        print(f'Request failed: {str(e)}')
        return None


# Main function to get user chats and user info
def get_user_chats():
    access_token = get_access_token()  # Get access token
    if access_token:
        chats = get_chats('', access_token)  # Replace with your actual user ID

        for i in chats[('chats')]:
            try:
                print(i['id'])
                pass

            except:
                pass




        #print(f'Chats: {json.dumps(chats, indent=2)}')  # Print chats in JSON format
        return chats
    else:
        print('Failed to get access token')
        return None


# Main execution
if __name__ == "__main__":
    get_user_chats()  # Get user chats and print them
