import time
from datetime import datetime
import requests
import json
import itertools

today_date = datetime.now().strftime("%Y-%m-%d")
# Define the number of tasks and task duration in minutes
num_tasks = 32
task_duration_minutes = 15


def update_task(project, task, task_created_date, task_type, start_time, end_time, subproject):
    url = "https://100098.pythonanywhere.com/task_module/?type=update_candidate_task&task_id=651cea3d5ca81f4ee9a2aec2"
    payload = json.dumps({
        "project": project,
        "applicant": "Winder",
        "task": task,
        "task_added_by": "Winder",
        "data_type": "Real_Data",
        "company_id": "6385c0f18eca0fb652c94561",
        "task_created_date": task_created_date,
        "task_type": task_type,
        "start_time": start_time.split()[0],
        "end_time": end_time.split()[0],
        "user_id": "62e7b0ff8ccd1fc0b0e835c9",
        "subproject": subproject
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://ll07-team-dowell.github.io',
        'Referer': 'https://ll07-team-dowell.github.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def generate_subtask_names(task_titles):
    # Define the categories
    categories = ['Ideation', 'Design', 'Brainstorming', 'Coding', 'Testing', 'commit', 'push code', 'analysing']

    # Generate all possible unique subtask names
    all_subtask_names = []

    for category in categories:
        subtask_names = [f"{title} - {category}" for title in task_titles]
        all_subtask_names.extend(subtask_names)

    # Shuffle the list of subtask names to randomize the order
    shuffled_subtask_names = list(set(all_subtask_names))
    itertools.cycle(shuffled_subtask_names)

    # Return one unique subtask name at a time
    while shuffled_subtask_names:
        yield shuffled_subtask_names.pop()

def add_tasks_function(task_titles):
    # Example usage:
    subtask_generator = generate_subtask_names(task_titles)

    # Initialize the start time
    start_hour = 8  # 8:00 AM
    start_minute = 0
    # Loop through tasks and select start and finish times
    for i in range(num_tasks):
        # Convert start time to string format (e.g., "08:00 AM")
        start_time = f"{start_hour:02}:{start_minute:02} {'AM' if start_hour < 12 else 'PM'}"

        # Calculate and select finish time
        finish_hour = start_hour
        finish_minute = start_minute + task_duration_minutes

        if finish_minute >= 60:
            finish_hour += 1
            finish_minute -= 60

        # Convert finish time to string format (e.g., "08:15 AM")
        finish_time = f"{finish_hour:02}:{finish_minute:02} {'AM' if finish_hour < 12 else 'PM'}"

        # Do your task-related actions here, such as filling in the task details.
        # if start_time == "12:00 PM":
        #     update_task("Living Lab Scales", "Gave updates regarding the scales editor and also regarding my task.", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development")
        #     # Perform specific logic at 11:30 AM and 11:45 AM
        #     print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        if start_time == "10:00 AM":
            update_task("Editor", "Meeting with scale team members to take there task updates and assign them new tasks", today_date, "MEETING UPDATE", start_time, finish_time, "Scales")
            # Perform specific logic at 10:30 AM and 10:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        else:
            task = next(subtask_generator)
            print(f"Subtask {i + 1}: {task}")
            update_task("Editor", task, today_date, "TASK UPDATE", start_time, finish_time, "Scales")
            print(f"Task {i+1:02}: Start time {start_time} - Finish time {finish_time}")

        # Update the start time for the next task
        start_hour = finish_hour
        start_minute = finish_minute

        # Wait for a while (optional)
        time.sleep(1)
    return "You are safe Norah, all tasks uploaded successfully."


task_titles = ["Fixing nps_lite API issues when update button is clicked", "Fixing nps_lite API issues when update button is clicked", "Meeting with Ambrose to discuss percent_sum document response API", "Fixing design issues in percent scale after saving and reloading"]
print(add_tasks_function(task_titles))

