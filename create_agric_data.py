import csv
import pandas as pd

# Data for agricultural advice
data = {
    "advice_id": [1, 2, 3],
    "advice_text": [
        "Rotate crops to prevent soil depletion and improve yield.",
        "Use organic compost to enrich soil nutrients and promote healthy plant growth.",
        "Monitor weather conditions and adjust irrigation schedules accordingly."
    ],
    "steps": [
        "1. Plan crop rotation to include legumes and cover crops.\n"
        "2. Avoid planting the same crop family in the same spot year after year.",

        "1. Prepare compost with a mix of green (nitrogen-rich) and brown (carbon-rich) materials.\n"
        "2. Turn the compost regularly to aerate and accelerate decomposition.",

        "1. Use soil moisture sensors or weather data to determine irrigation needs.\n"
        "2. Adjust irrigation frequency and duration based on plant type and weather conditions."
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to CSV
df.to_csv('agriculture_data.csv', index=False, quoting=csv.QUOTE_MINIMAL)

print("agriculture_data.csv file has been created successfully.")
