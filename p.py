import requests
import time
import json
from datetime import datetime, timedelta

# Function to load login payload from a file
def load_login_payload(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            raise ValueError("File is empty.")
        return [line.strip() for line in lines]

# Function to login and get authorization token
def login_and_get_token(login_url, login_payload):
    response = requests.get(login_url, params=login_payload)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            token = data['data']['token']
            print(f'Login successful. Token: {token}')
            return token
        else:
            print(f'Login failed. Code: {data["code"]}')
            return None
    else:
        print(f'Login request failed. Status code: {response.status_code}')
        return None

# Function to save token to a file
def save_token_to_file(file_path, token):
    with open(file_path, 'w') as file:
        file.write(token)

# Function to read authorization tokens from file
def read_authorizations(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to display a moving countdown timer
def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f'Countdown: {timer}', end='\r')
        time.sleep(1)
        seconds -= 1
    print(' ' * 20, end='\r')  # Clear the countdown line

# Function to take a task
def take_task(headers, task_payload):
    url = 'https://api.prod.piggypiggy.io/game/TakeTask'
    response = requests.post(url, headers=headers, json=task_payload)
    if response.status_code == 200:
        data = response.json()
        if 'curTaskStartTime' in data:
            cur_task_start_time = data['curTaskStartTime']
            cur_task_start_time = datetime.fromtimestamp(cur_task_start_time / 1000)
            print(f'Task {task_payload["TaskID"]} taken successfully. Start Time: {cur_task_start_time}')
            return cur_task_start_time
        else:
            print(f'Task {task_payload["TaskID"]} taken but start time not received.')
            return None
    else:
        print(f'Failed to take task {task_payload["TaskID"]}. Status code: {response.status_code}')
        return None

# Function to complete a task
def complete_task(headers, task_payload):
    url = 'https://api.prod.piggypiggy.io/game/CompleteTask'
    response = requests.post(url, headers=headers, json=task_payload)
    if response.status_code == 200:
        print(f'Task {task_payload["TaskID"]} completed successfully.')
    else:
        print(f'Failed to complete task {task_payload["TaskID"]}. Status code: {response.status_code}')

# Function to handle tasks for each account
def handle_tasks(authorization, account_index, total_accounts):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Authorization': f'Bearer {authorization}',
        'Cache-Control': 'no-cache',
        'Content-Length': '28',
        'Content-Type': 'application/json',
        'Origin': 'https://restaurant-v2.piggypiggy.io',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://restaurant-v2.piggypiggy.io/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

    tasks = [
        (1001, 3*3600),
        (1002, 4*60),
        (1003, 5*60),
        (1004, 7*60),
        (1005, 11*60),
        (1006, 16*60)
    ]

    print(f'Processing account {account_index + 1} of {total_accounts}')
    
    for task_id, delay in tasks:
        task_payload = {"TaskID": task_id, "PlayerID": 0}
        cur_task_start_time = take_task(headers, task_payload)
        
        if cur_task_start_time:
            next_task_time = cur_task_start_time + timedelta(seconds=delay)
            wait_time = (next_task_time - datetime.now()).total_seconds()
            
            if wait_time > 0:
                print(f'Waiting {wait_time} seconds before completing the task...')
                countdown(int(wait_time))
        
        complete_task(headers, task_payload)
        
        print('Waiting 5 seconds before switching accounts...')
        countdown(5)

# Main script execution
def main():
    login_file_path = 'data.txt'
    login_url = 'https://api.prod.piggypiggy.io/tgBot/login'
    
    # Load login payloads from file
    try:
        login_payloads = load_login_payload(login_file_path)
    except ValueError as e:
        print(f"Error loading login payloads: {e}")
        return

    for login_payload in login_payloads:
        # Get token from login
        token = login_and_get_token(login_url, login_payload)
        if not token:
            continue
        
        # Save token to file
        save_token_to_file('data.txt', token)

        # Read authorization tokens from file
        authorization_tokens = read_authorizations('data.txt')
        total_accounts = len(authorization_tokens)

        # Handle tasks for each account
        for i, authorization in enumerate(authorization_tokens):
            handle_tasks(authorization, i, total_accounts)

        # Countdown 1 hour before restarting
        print('All accounts processed. Starting 1-hour countdown...')
        countdown(3600)

if __name__ == '__main__':
    main()
