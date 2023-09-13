import random
import csv
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Define a bold font (you may need to specify the path to a bold font file)
bold_font = ImageFont.truetype("arialbd.ttf", size=20)  # Change the font file and size as needed

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
print("Which week do want to start on?")
start_week = int(input("Enter start week: "))     # Change this to the desired start week

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

# Create an image
image_width = 400
image_height = 700
image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
draw = ImageDraw.Draw(image)

# Define fonts and text colors
font = ImageFont.truetype("arial.ttf", size=20)
text_color = (0, 0, 0)

# Define the position to start drawing the schedule
x_pos = 50
y_pos = 50

# Loop through the schedule and draw it on the image
for assignments in schedule:
    week = assignments["Week"]
    start_date = assignments["Start Date"]
    end_date = assignments["End Date"]
    tuesday_pair = assignments['Tuesday']
    saturday_pair = assignments['Saturday']

    # Calculate the Tuesday and Saturday dates
    tuesday_date = start_date + timedelta(days=(1 - start_date.weekday()) % 7)  # Find the next Tuesday
    saturday_date = start_date + timedelta(days=(5 - start_date.weekday()) % 7)  # Find the next Saturday

    # Draw the week number and date range using the bold font
    week_text = f"Semana {week}:"
    draw.text((x_pos, y_pos), week_text, fill=text_color, font=bold_font)

    # Increment the y position
    y_pos += 30

    # Assign jobs and draw names with their respective jobs for Tuesday
    job1, job2 = "Som", "Zoom"
    left_name, right_name = tuesday_pair[0], tuesday_pair[1]

    # Draw Tuesday assignments
    draw.text((x_pos, y_pos), f"Terça-feira ({tuesday_date.strftime('%Y-%m-%d')}):", fill=text_color, font=font)
    y_pos += 30
    draw.text((x_pos + 20, y_pos), f"Som: {left_name}, Zoom: {right_name}", fill=text_color, font=font)
    y_pos += 30

    # Assign jobs and draw names with their respective jobs for Saturday
    jom, job2 = "Som", "Zoom"
    left_name, right_name = saturday_pair[0], saturday_pair[1]

    # Draw Saturday assignments
    draw.text((x_pos, y_pos), f"Sábado ({saturday_date.strftime('%Y-%m-%d')}):", fill=text_color, font=font)
    y_pos += 30
    draw.text((x_pos + 20, y_pos), f"Som: {left_name}, Zoom: {right_name}", fill=text_color, font=font)
    y_pos += 30  # Increase the vertical space between weeks

# Save the image as a JPG file
image.save("schedule.jpg")

# Close the image
image.close()