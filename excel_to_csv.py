import pandas as pd

# Path to your .xlsx file
input_file = 'HalfBridgeLLC.xlsx'

# Read the Excel file
df = pd.read_excel(input_file)

# Path to save the .csv file
output_file = 'halfBridgeMatlab.csv'

# Save as a .csv file
df.to_csv(output_file, index=False)

print(f"Conversion complete! File saved as '{output_file}'")