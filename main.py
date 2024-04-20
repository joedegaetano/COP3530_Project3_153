import sys
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QTextEdit, QComboBox


from helper_functions import shell_sort

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read JSON file into DataFrame
try:
    df = pd.read_json("yelp_academic_dataset_business.json", lines=True)
except Exception as e:
    print(f"Failed to read file: {e}")
    sys.exit(1)

# Filter only restaurant records
filtered_df = df[df['categories'].str.contains('Restaurants', case=False, na=False)]

# Drop unnecessary columns
reduced_df = filtered_df.drop(columns=['business_id', 'hours', 'is_open', 'latitude', 'longitude', 'attributes'])

# Convert DataFrame to a list of dictionaries and sort it
business_list = reduced_df.to_dict(orient='records')
shell_sort(business_list)  

# Convert the sorted list back to a DataFrame
sorted_df = pd.DataFrame(business_list)
sorted_df = sorted_df[sorted_df['stars'] > 4.0]
print(sorted_df.head(1000))
