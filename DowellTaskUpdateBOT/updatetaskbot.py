import time
from datetime import datetime, timedelta
import requests
import json
import itertools

# +++++++++++++++++++++++++Previous Days Tasks+++++++++++++++++++++++++++++
# today_date = datetime.now()
# # Calculate yesterday's date by subtracting one day
# yesterday_date = today_date - timedelta(days=1)
# # Format yesterday's date as a string in the desired format
# today_date = yesterday_date.strftime("%Y-%m-%d")


today_date = datetime.now().strftime("%Y-%m-%d")
# Define the number of tasks and   task duration in minutes
num_tasks = 42
task_duration_minutes = 15

def get_session(username, password):
    url="http://100014.pythonanywhere.com/api/login/"
    payload = {
        'username': username,
        'password': password,
    }
    # Make a POST request and save the response in the session
    with requests.Session() as s:
        p = s.post(url, data=payload)
        p = p.json()
        print(p['jwt'])
        return p['jwt']

def create_new_task(project, task, task_created_date, task_type, start_time, end_time, subproject, jwt):
    url = "https://100098.pythonanywhere.com/task_module/?type=add_task"

    payload = json.dumps({
        "project": project,
        "applicant": "Ndoneambrose",
        "task": task,
        "task_added_by": "Ndoneambrose",
        "data_type": "Real_Data",
        "company_id": "6385c0f18eca0fb652c94561",
        "task_created_date": task_created_date,
        "task_type": task_type,
        "start_time": start_time.split()[0],
        "end_time": end_time.split()[0],
        "user_id": "62cbc347f61e183b6beb4881",
        "subproject": subproject
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': jwt,
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
    r = response.json()
    print(r)
    return r['response']['task_id']


def update_task(project, task, task_created_date, task_type, start_time, end_time, subproject, id, jwt):
    url = f"https://100098.pythonanywhere.com/task_module/?type=update_candidate_task&task_id={id}"
    payload = json.dumps({
        "project": project,
        "applicant": "Ndoneambrose",
        "task": task,
        "task_added_by": "Ndoneambrose",
        "data_type": "Real_Data",
        "company_id": "6385c0f18eca0fb652c94561",
        "task_created_date": task_created_date,
        # "task_created_date": "2023-09-26",
        "task_type": task_type,
        "start_time": start_time.split()[0],
        "end_time": end_time.split()[0],
        "user_id": "62cbc347f61e183b6beb4881",
        "subproject": subproject
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': jwt,
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
    r = response.json()

def generate_subtask_names(task_titles):
    # Return task titles unmodified
    for title in task_titles:
        yield title

# def generate_subtask_names(task_titles):
#
#     # Define the categories
#     categories = ['Ideation', 'Design', 'Brainstorming', 'Coding', 'Testing', 'commit', 'push code', 'Deploying']
#
#     # Generate all possible unique subtask names
#     all_subtask_names = []
#
#     for category in categories:
#         subtask_names = [f"{title} - {category}" for title in task_titles]
#         all_subtask_names.extend(subtask_names)
#
#     # Shuffle the list of subtask names to randomize the order
#     shuffled_subtask_names = list(set(all_subtask_names))
#     itertools.cycle(shuffled_subtask_names)
#
#     # Return one unique subtask name at a time
#     while shuffled_subtask_names:
#         yield shuffled_subtask_names.pop()

def add_tasks_function(task_titles):
    jwt = get_session("Ndoneambrose","ambroseTall3436!")
    # Example usage:
    subtask_generator = generate_subtask_names(task_titles)

    # Initialize the start time
    start_hour = 8  # 8:00 AM
    start_minute = 0
    task_id = None
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

        if task_id is None:
            task_id = create_new_task("Living Lab Scales", "Planning for the day.", today_date, "TASK UPDATE", start_time, finish_time, "Scales API Development", jwt=jwt)

        # Do your task-related actions here, such as filling in the task details.
        if start_time == "11:00 AM":
            update_task("Living Lab Scales", "Getting updates Umar on the test cases", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        elif start_time == "11:15 PM":
            update_task("Living Lab Scales", "Updating attendance of the daily meeting", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        elif start_time == "11:30 PM":
            update_task("Living Lab Scales", "Getting updates from Rao on implementing the master link in nps lite", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        elif start_time == "15:15 PM":
            update_task("Living Lab Scales", "Meeting with Tijani and assigning him task to refactor code ", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")

        elif start_time == "15:45 PM":
            update_task("Living Lab Scales", "Overseeing implementation of new designs", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")
        elif start_time == "11:45 PM":
            update_task("Living Lab Scales", "Getting updates from Norah rergarding the front end implementation", today_date, "MEETING UPDATE", start_time, finish_time, "Scales API Development", task_id,jwt=jwt)
            # Perform specific logic at 11:30 AM and 11:45 AM
            print(f"Meeting {i+1:02}: Start time {start_time} - Finish time {finish_time}")

        else:
            task = next(subtask_generator)
            print(f"Subtask {i + 1}: {task}")
            update_task("Living Lab Scales", task, today_date, "TASK UPDATE", start_time, finish_time, "Scales API Development", task_id, jwt=jwt)
            print(f"Task {i+1:02}: Start time {start_time} - Finish time {finish_time}")

        # Update the start time for the next task
        start_hour = finish_hour
        start_minute = finish_minute

        # Wait for a while (optional)
        time.sleep(1)
    return "You are safe Ambrose, all tasks uploaded successfully."


task_titles = [
    "Conduct thorough debugging sessions to identify and resolve code issues.",
    "Collaborate with developers to understand the root causes of bugs and errors.",
    "Document debugging processes and solutions for knowledge sharing.",
    "Implement and follow debugging best practices for efficient issue resolution.",
    "Fetch scores using ThreadPoolExecutor and Dowell connection.",
    "Handle errors and return appropriate responses in the scalewise_report view.",
    "Generate random numbers for use in the scalewise_report view.",
    "Submit asynchronous tasks to ThreadPoolExecutor for concurrent execution.",
    "Load and parse JSON results from asynchronous tasks in the scalewise_report view.",
    "Check for the existence of scale data and scale type in the fetched results.",
    "Validate the scale type and return an appropriate response in the scalewise_report view.",
    "Iterate over fetched data to extract scores and handle nested dictionary structures.",
    "Ensure the availability of a minimum number of scores for report generation.",
    "Categorize and generate scale-specific reports using categorize_scale_generate_scale_specific_report.",
    "Submit asynchronous tasks to ThreadPoolExecutor for stattricks_api execution.",
    "Extract poison case and normal case results from statricks_api_response_json.",
    "Handle exceptions and gracefully fail in case of errors during the report generation process.",
    "Design and implement scalable and efficient algorithms.",
    "Optimize code for performance improvements and resource utilization.",
    "Work closely with cross-functional teams to gather requirements.",
    "Write clean, maintainable, and well-documented code.",
    "Implement the Normality API for statistical analysis in the scalewise_report view.",
    "Return appropriate responses based on the availability of data and scale type.",
    "Ensure the successful execution of the Normality API and handle exceptions.",
    "Implement the categorize_scale_generate_scale_specific_report function.",
    "Submit asynchronous tasks for parallel execution in the ThreadPoolExecutor.",
    "Generate random numbers using the generate_random_number function.",
    "Check for errors during the Dowell connection and return appropriate responses.",
    "Handle potential exceptions during the execution of the scalewise_report view.",
    "Validate and extract scale data, including scale ID and scale type.",
    "Check for the minimum number of responses before generating reports.",
    "Handle errors and exceptions during the categorization and report generation process.",
    "Extract and present poison case and normal case results in the final report.",
]

print(len(task_titles))
print(add_tasks_function(task_titles))

