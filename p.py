import requests
import time
import json
from datetime import datetime, timedelta

# Function to read authorization tokens from data.txt
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

# Function to take a task
def take_task(headers, task_payload):
    url = 'https://api.prod.piggypiggy.io/game/TakeTask'
    response = requests.post(url, headers=headers, json=task_payload)
    if response.status_code == 200:
        print(f'Task {task_payload["TaskID"]} taken successfully.')
    else:
        print(f'Failed to take task {task_payload["TaskID"]}.')

# Function to complete a task
def complete_task(headers, task_payload):
    url = 'https://api.prod.piggypiggy.io/game/CompleteTask'
    response = requests.post(url, headers=headers, json=task_payload)
    if response.status_code == 200:
        print(f'Task {task_payload["TaskID"]} completed successfully.')
    else:
        print(f'Failed to complete task {task_payload["TaskID"]}.')

# Function to handle tasks for each account
def handle_tasks(authorization, account_index, total_accounts):
    headers = {
        ':authority': 'api.prod.piggypiggy.io',
        ':method': 'POST',
        ':path': '/game/CompleteTask',
        ':scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Authorization': authorization,
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
        take_task(headers, task_payload)
        complete_task(headers, task_payload)
        
        next_task_time = datetime.now() + timedelta(seconds=delay)
        print(f'Next task {task_id} in: {next_task_time.strftime("%Y-%m-%d %H:%M:%S")}')
        
        print('Waiting 30 seconds before next task...')
        countdown(30)

# Main script execution
def main():
    authorization_tokens = read_authorizations('data.txt')
    total_accounts = len(authorization_tokens)

    for i, authorization in enumerate(authorization_tokens):
        handle_tasks(authorization, i, total_accounts)
        if i < total_accounts - 1:
            print('Waiting 15 seconds before switching accounts...')
            countdown(15)

if __name__ == '__main__':
    main()
