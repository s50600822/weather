import json
import matplotlib.pyplot as plt
from datetime import datetime

json_file = 'Pymble2022.json'

with open(json_file, 'r') as file:
    data = json.load(file)

# Extract datetime, tempmax, and tempmin values
datetime_values = [entry['datetime'] for entry in data['days']]
tempmax_values = [entry['tempmax'] for entry in data['days']]
tempmin_values = [entry['tempmin'] for entry in data['days']]

# Convert datetime strings to datetime objects
datetime_values = [datetime.strptime(dt, '%Y-%m-%d') for dt in datetime_values]

# Create dictionaries to store monthly aggregates
monthly_tempmax = {}
monthly_tempmin = {}

# Calculate monthly averages for tempmax and tempmin
for dt, tempmax, tempmin in zip(datetime_values, tempmax_values, tempmin_values):
    month_year = (dt.year, dt.month)
    if month_year not in monthly_tempmax:
        monthly_tempmax[month_year] = []
        monthly_tempmin[month_year] = []
    monthly_tempmax[month_year].append(tempmax)
    monthly_tempmin[month_year].append(tempmin)

# Calculate monthly averages
monthly_avg_tempmax = [sum(monthly_tempmax[month_year]) / len(monthly_tempmax[month_year]) for month_year in sorted(monthly_tempmax)]
monthly_avg_tempmin = [sum(monthly_tempmin[month_year]) / len(monthly_tempmin[month_year]) for month_year in sorted(monthly_tempmin)]

# Create list of datetime objects for each month
months = [datetime(year, month, 1) for year, month in sorted(monthly_tempmax)]

# Find the indices of the lowest and highest points
lowest_index = monthly_avg_tempmin.index(min(monthly_avg_tempmin))
highest_index = monthly_avg_tempmax.index(max(monthly_avg_tempmax))

# Plotting
plt.plot(months, monthly_avg_tempmax, label='Average Max Temperature', color='red')
plt.plot(months, monthly_avg_tempmin, label='Average Min Temperature', color='blue')
plt.scatter(months[lowest_index], monthly_avg_tempmin[lowest_index], color='red', label='Lowest Point')
plt.scatter(months[highest_index], monthly_avg_tempmax[highest_index], color='green', label='Highest Point')

# plt.vlines(months[highest_index], 0, monthly_avg_tempmax[highest_index], linestyle='dotted', color='grey')
plt.hlines(monthly_avg_tempmax[highest_index], datetime(months[highest_index].year, 1, 1), months[highest_index], linestyle='dotted', color='grey')

# plt.vlines(months[highest_index], 0, monthly_avg_tempmax[highest_index], linestyle='dotted', color='grey')
plt.hlines(monthly_avg_tempmin[lowest_index], datetime(months[lowest_index].year, 1, 1), months[lowest_index], linestyle='dotted', color='grey')


plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Monthly Average Min and Max Temperature')
# plt.legend()
plt.ylim(0) # y-axis to start from 0

plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
# plt.show()
# plt.figure()
plt.savefig(json_file.split('.')[0]+'.png')
