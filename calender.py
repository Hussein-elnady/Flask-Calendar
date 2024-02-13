# Import necessary libraries
from flask import Flask, render_template, request
import calendar
import datetime

# Create Flask application instance
app = Flask(__name__)

# Define a function to generate a customized calendar
def get_calendar(year, month):
    """
    Creates a customized calendar with the following features:

    - Weeks start on Saturday
    - Fridays have a different color
    - Days outside the current month have a different color
    - Today's date is highlighted

    Args:
        year (int): The year for the calendar.
        month (int): The month for the calendar (1-12).

    Returns:
        list: A list of weeks (lists of days) representing the calendar month.
    """

    # Start by fetching the standard calendar layout using the "calendar" library
    cal = calendar.monthcalendar(year, month)

    # Adjust the calendar to start with Saturday instead of Monday
    # This involves moving the first day of each week (index 0) to the end
    for week in cal:
        week.insert(0, week.pop())

    # Highlight today's date if the provided year and month are correct
    today = datetime.date.today()
    for week in cal:
        for day in week:
            if day != 0 and (day, month, year) == (today.day, today.month, today.year):
                # Instead of a regular number, store day information and a CSS class for styling
                day = {'day': day, 'class': 'today'}

    # Add different CSS classes for Fridays and days outside the current month
    for week in cal:
        for i, day in enumerate(week):
            if day != 0:
                # Use the day's index (0-6) to determine the weekday
                if i == 5:  # Change index based on day of the week (Saturday)
                    day = {'day': day, 'class': 'saturday'}
                elif i == 4:  # Change index based on day of the week (Friday)
                    day = {'day': day, 'class': 'friday'}
                else:
                    # Check if the day is within the current month's range using "calendar.monthrange"
                    if day not in range(1, calendar.monthrange(year, month)[1] + 1):
                        day = {'day': day, 'class': 'out-of-month'}

    # Return the modified calendar with styling information
    return cal

# Get the current year and month for default display
def get_current_year():
    return datetime.datetime.now().year

def get_current_month():
    return datetime.datetime.now().month

# Define the main route for the application
@app.route('/', methods=['GET', 'POST'])
def home():
    # Handle form submission (POST) or display initial calendar (GET)
    if request.method == 'POST':
        # Read submitted year and month values from the form
        year = int(request.form['year'])
        month = int(request.form['month'])
    else:
        # Use helper functions to get the current year and month
        year = get_current_year()
        month = get_current_month()

    # Generate the customized calendar for the chosen year and month
    cal = get_calendar(year, month)

    # Calculate the number of days in the current month
    num_days_in_month = calendar.monthrange(year, month)[1]

    # Get today's date for highlighting
    today = datetime.date.today()

    # Pass data to the template for rendering
    return render_template('calendar.html', year=year, month=month, cal=cal, num_days_in_month=num_days_in_month, today=today)

# Run the application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
