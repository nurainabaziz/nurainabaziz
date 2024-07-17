import pandas as pd
import re
import matplotlib.pyplot as plt
from user_agents import parse

# Re-read the CSV file
file_path = '/Users/nurainabaziz/logs.csv'
df = pd.read_csv(file_path, quotechar='"', on_bad_lines='skip')

def parse_apache_log_line(log_line):
    log_pattern = re.compile(
        r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>[A-Z]+) (?P<url>[^ ]+) HTTP/[^\"]+" (?P<status>\d+) (?P<size>\d+) "(?P<referrer>[^\"]*)" "(?P<user_agent>[^\"]*)"'
    )
    match = log_pattern.match(log_line)
    if match:
        return match.groupdict()
    else:
        return None

# Apply the parsing function to each log line
parsed_logs = df.iloc[:, 0].apply(parse_apache_log_line).dropna().tolist()

# Convert the list of dictionaries to a DataFrame
parsed_df = pd.DataFrame(parsed_logs)

# Convert the timestamp to datetime format
parsed_df['timestamp'] = pd.to_datetime(parsed_df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')

# Ensure timestamp is set as index
parsed_df.set_index('timestamp', inplace=True)

# Resample the data by hour to analyze traffic trends over time
hourly_traffic = parsed_df['url'].resample('H').count()

# Display the cleaned and structured data
print(parsed_df.head())

# Save the cleaned data to a new CSV file
output_file_path = '/Users/nurainabaziz/cleaned_logs.csv'
parsed_df.to_csv(output_file_path)

# Plot the hourly traffic
plt.figure(figsize=(12, 6))
hourly_traffic.plot(title='Hourly Traffic Trends', ylabel='Number of Requests', xlabel='Date and Time')
plt.grid(True)
plt.savefig('/Users/nurainabaziz/hourly_traffic_trends.png')
plt.show()

# Step 9: Plot page view trends and traffic sources
# Page view trends
daily_traffic = parsed_df['url'].resample('D').count()

plt.figure(figsize=(12, 6))
daily_traffic.plot(title='Daily Page View Trends', ylabel='Number of Requests', xlabel='Date')
plt.grid(True)
plt.savefig('/Users/nurainabaziz/daily_page_view_trends.png')
plt.show()

# Traffic sources from referrer
def categorize_referrer(referrer):
    if referrer == '-':
        return 'Direct'
    elif any(search_engine in referrer for search_engine in ['google', 'bing', 'yahoo']):
        return 'Search'
    else:
        return 'Referral'

parsed_df['traffic_source'] = parsed_df['referrer'].apply(categorize_referrer)
traffic_sources = parsed_df['traffic_source'].value_counts()

plt.figure(figsize=(8, 6))
traffic_sources.plot(kind='bar', title='Traffic Sources', ylabel='Number of Requests', xlabel='Source')
plt.xticks(rotation=0)
plt.grid(True)
plt.savefig('/Users/nurainabaziz/traffic_sources.png')
plt.show()

# Analyze traffic by device type
def get_device_type(user_agent):
    ua = parse(user_agent)
    if ua.is_mobile:
        return 'Mobile'
    elif ua.is_tablet:
        return 'Tablet'
    elif ua.is_pc:
        return 'Desktop'
    elif ua.is_bot:
        return 'Bot'
    else:
        return 'Other'

parsed_df['device_type'] = parsed_df['user_agent'].apply(get_device_type)
device_types = parsed_df['device_type'].value_counts()

plt.figure(figsize=(8, 6))
device_types.plot(kind='bar', title='Traffic by Device Type', ylabel='Number of Requests', xlabel='Device Type')
plt.xticks(rotation=0)
plt.grid(True)
plt.savefig('/Users/nurainabaziz/traffic_by_device_type.png')
plt.show()

# Plot traffic sources over different days
daily_traffic_sources = parsed_df.groupby([pd.Grouper(freq='D'), 'traffic_source']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
daily_traffic_sources.plot(kind='line', title='Daily Traffic Sources', ylabel='Number of Requests', xlabel='Date')
plt.grid(True)
plt.savefig('/Users/nurainabaziz/daily_traffic_sources.png')
plt.show()

# Output the file path for reference
output_file_path