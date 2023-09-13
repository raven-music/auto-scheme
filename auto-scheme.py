import random
import csv
from datetime import datetime, timedelta

# Function to get the start date of a week based on the week number and year
def start_date_of_week(year, week_number):
    return datetime.strptime(f'{year}-W{week_number}-1', "%Y-W%U-%w").date()

# Function to get the end date of a week based on the week number and year
def end_date_of_week(year, week_number):
    return start_date_of_week(year, week_number) + timedelta(days=6)

# Function to create pairs of two people while ensuring everyone gets a turn
def create_pairs(names):
    random.shuffle(names)
    pairs = []
    
    # Determine the number of pairs needed
    num_pairs = len(names) // 2
    
    for i in range(num_pairs):
        pair = [names[i], names[num_pairs + i]]
        pairs.append(pair)
    
    return pairs

# Initialize lists to store names by gender
males = []
females = []

# Load names from the CSV file
with open('names.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        name, gender = row
        if gender == 'M':
            males.append(name)
        elif gender == 'F':
            females.append(name)

# Determine the year and week number you want to start from
start_year = 2023  # Change this to the desired start year
start_week = 1     # Change this to the desired start week

# Determine the number of weeks you want to schedule
num_weeks = 4  # Change this to the desired number of weeks

# Create pairs of men and pairs of women while ensuring everyone gets a turn
male_pairs = create_pairs(males)
female_pairs = create_pairs(females)
pairs = male_pairs + female_pairs

# Initialize a list to store the schedule
schedule = []

for week in range(start_week, start_week + num_weeks):
    # Get the pairs for Tuesday and Saturday
    # tuesday_pair = male_pairs[week % len(male_pairs)] if week % 2 == 1 else female_pairs[week % len(female_pairs)]
    tuesday_pair = pairs[week % len(pairs)]
    saturday_pair = tuesday_pair[::-1]

    # Calculate the start and end dates for the week
    week_start_date = start_date_of_week(start_year, week)
    week_end_date = end_date_of_week(start_year, week)

    # Store the pairs in the schedule along with the dates for both Tuesday and Saturday
    schedule.append({"Week": week, "Start Date": week_start_date, "End Date": week_end_date, "Tuesday": tuesday_pair, "Saturday": saturday_pair})

# Print the schedule
for assignments in schedule:
    week = assignments["Week"]
    start_date = assignments["Start Date"].strftime("%Y-%m-%d")
    end_date = assignments["End Date"].strftime("%Y-%m-%d")
    tuesday_pair = assignments['Tuesday']
    saturday_pair = assignments['Saturday']

    print(f"Week {week} ({start_date} to {end_date}):")
    print(f"Tuesday: {tuesday_pair[0]} and {tuesday_pair[1]}")
    print(f"Saturday: {saturday_pair[0]} and {saturday_pair[1]}\n")
