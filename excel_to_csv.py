import pandas as pd


def convertExcelToCSV(input_file, output_file):


    # Read the Excel file
    df = pd.read_excel(input_file)



    # Save as a .csv file
    df.to_csv(output_file, index=False)

    print(f"Conversion complete! File saved as '{output_file}'")



# half bridge
input_file = 'HalfBridgeLLC.xlsx'
output_file = 'halfBridgeMatlab.csv'
convertExcelToCSV(input_file, output_file)

# full bridge
input_file = "FullBridgeMatlab.xlsx"
output_file = "fullBridgeMatlab.csv"
convertExcelToCSV(input_file, output_file)