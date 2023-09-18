import time

result_function = [{'position': 0, 'event_id': 10349416, 'remaining_quarter_secs': 320, 'quarter_name': '4TH', 'quarter_no': 4}, {'position': 2, 'event_id': 10352587, 'remaining_quarter_secs': 332, 'quarter_name': '1ST', 'quarter_no': 1}]

def find_below_260_or_nearest_second(dictionary_list):
    print("Result function", dictionary_list)
    below_260 = None
    nearest_second = None
    min_time_diff = float("inf")

    for item in dictionary_list:
        if "remaining_quarter_secs" in item:
            if item["remaining_quarter_secs"] < 260:
                return item  # Return the dictionary if "second" is below 260
            else:
                time_diff = abs(item["remaining_quarter_secs"] - 260)
                if time_diff < min_time_diff:
                    nearest_second = item
                    min_time_diff = time_diff

    if below_260 is not None:
        return below_260  # If a "second" below 260 was found, return it
    elif nearest_second is not None:
        time_to_wait = nearest_second["remaining_quarter_secs"] - 260
        if time_to_wait > 0:
            print(f"Waiting for {time_to_wait} seconds...")
            time.sleep(time_to_wait)
        return nearest_second  # If not below 260, return the nearest to 260

    return None  # Return None if no "second" values found

print(find_below_260_or_nearest_second(result_function))