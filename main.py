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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        # Set up the main window
        self.setWindowTitle("Best Eats")
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create label for the title
        title_label = QLabel("Best Eats", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Predefined filters ComboBox
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Best Restaurants", "Worst Restaurants", "Custom Search"])
        self.filter_combo.currentIndexChanged.connect(self.toggle_custom_search)
        layout.addWidget(self.filter_combo)

        # Custom search inputs
        self.star_input = QLineEdit(self)
        self.star_input.setPlaceholderText("Enter Minimum Stars")
        self.cuisine_input = QLineEdit(self)
        self.cuisine_input.setPlaceholderText("Type of Cuisine")
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Restaurant Name")
        self.custom_search_layout = QHBoxLayout()
        self.custom_search_layout.addWidget(self.star_input)
        self.custom_search_layout.addWidget(self.cuisine_input)
        self.custom_search_layout.addWidget(self.name_input)
        layout.addLayout(self.custom_search_layout)

        # Toggle visibility
        self.toggle_custom_search()

        # Create input fields for city and state
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter City")
        self.state_input = QLineEdit(self)
        self.state_input.setPlaceholderText("Enter State")
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.state_input)
        layout.addLayout(input_layout)

        # Create go and clear
        go_button = QPushButton("Go", self)
        go_button.clicked.connect(self.display_results)
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.clear_inputs)
        button_layout = QHBoxLayout()
        button_layout.addWidget(go_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Create the output text area
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        self.text_edit.setAlignment(Qt.AlignLeft)


    def toggle_custom_search(self):
        # Show or hide custom search fields based on combo selection
        is_custom = self.filter_combo.currentText() == "Custom Search"
        self.star_input.setVisible(is_custom)
        self.cuisine_input.setVisible(is_custom)
        self.name_input.setVisible(is_custom)

    def display_results(self):
        filter_choice = self.filter_combo.currentText()
        results_df = sorted_df.copy()

        if filter_choice == "Custom Search":
            stars = float(self.star_input.text()) if self.star_input.text().isdigit() else 0
            cuisine = self.cuisine_input.text().lower()
            name = self.name_input.text().lower()
            results_df = results_df[(results_df['stars'] >= stars) & (results_df['categories'].str.contains(cuisine, case=False, na=False)) & (results_df['name'].str.lower().contains(name))]
            results_df = results_df.sort_values(by='stars', ascending=False)

        elif filter_choice == "Best Restaurants":
            results_df = results_df[results_df['stars'] >= 4.0]
            newarray = results_df.to_dict(orient='records')
            shell_sort(newarray) # Using Custom Sort
            results_df = pd.DataFrame(newarray)

        elif filter_choice == "Worst Restaurants":
            results_df = results_df[results_df['stars'] <= 2.0]
            results_df = results_df.sort_values(by='stars', ascending=True)

        city = self.city_input.text().lower()
        state = self.state_input.text().lower()
        results_df = results_df[(results_df['city'].str.lower() == city) & (results_df['state'].str.lower() == state)]
        results_df = results_df[['name', 'stars', 'review_count']]  # Display only name, stars, and review count

        if not results_df.empty:
            formatted_results = ""
            rank = 1  # Start the rank counter at 1
            for _, row in results_df.iterrows():
                formatted_results += f"{rank}. {row['name']} - Stars: {row['stars']} - Reviews: {row['review_count']}\n"
                rank += 1  # Increment the rank for each item
            self.text_edit.setText(formatted_results)
        else:
            self.text_edit.setText("No results found.")

    def clear_inputs(self):
        self.city_input.clear()
        self.state_input.clear()
        self.text_edit.clear()
        self.star_input.clear()
        self.cuisine_input.clear()
        self.name_input.clear()

# PyQt5 application initialization
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
