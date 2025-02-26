import pandas as pd
import numpy as np
pd.set_option('future.no_silent_downcasting', True)

# Load the Excel file
file_path = 'data/pass_fail.xlsx'
rd_nn_unprocessed_data = pd.read_excel(file_path)

# DrawDate is recognised as object converting it to datetime object
rd_nn_unprocessed_data["DrawDate"] = pd.to_datetime(rd_nn_unprocessed_data["DrawDate"])

rd_nn_unprocessed_data.drop(columns=['Comments','IngredientLotNumber', 'JulianLotNumber'], inplace=True)
print(rd_nn_unprocessed_data.head())
# Identify all datetime columns
datetime_cols = rd_nn_unprocessed_data.select_dtypes(include=['datetime64']).columns

# Print the names of datetime columns
print("Datetime columns:", datetime_cols)

# Check for datetime columns and convert to numeric
for col in rd_nn_unprocessed_data.select_dtypes(include=['datetime64[ns]']):
    rd_nn_unprocessed_data[col] = rd_nn_unprocessed_data[col].astype(np.int64) // 10**9
print(rd_nn_unprocessed_data.columns,rd_nn_unprocessed_data.dtypes)

adjustments_list = [1259, 1261, 1262, 1264, 1265, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1279, 1282, 1310, 2740, 2750]

# Remove rows where 'Formula' is in adjustment_list
rd_nn_unprocessed_data = rd_nn_unprocessed_data[~rd_nn_unprocessed_data['Formula'].isin(adjustments_list)]

# Remove rows where 'ingredients' is 1000000
rd_nn_unprocessed_data = rd_nn_unprocessed_data[rd_nn_unprocessed_data['Ingredient'] != 100000]

rd_nn_unprocessed_data['Ingredient'] = rd_nn_unprocessed_data['Ingredient'].replace('6300000 (HA)', 63000001).infer_objects(copy=False)
rd_nn_unprocessed_data['RunResultName'] = rd_nn_unprocessed_data['RunResultName'].str.lower().replace({'aborted':0,'completed':0}).infer_objects(copy=False)
rd_nn_unprocessed_data['UserID'] = rd_nn_unprocessed_data['UserID'].str.lower().replace({'admin':1,'operator':2, 'batching svc':3, 'lclark':4, 'wfaught':5 ,'kbacon':6, 'gpenner': 7}).infer_objects(copy=False)
rd_nn_unprocessed_data['DrawStatusName'] = rd_nn_unprocessed_data['DrawStatusName'].str.lower().replace({'in tolerance':1,'over tolerance':-2, 'under tolerance': 2}).infer_objects(copy=False)
rd_nn_unprocessed_data['IngTypeName'] = rd_nn_unprocessed_data['IngTypeName'].str.lower().replace({'hand add': 1,'tote':2,'liquid':3, 'dry':4}).infer_objects(copy=False)

rd_nn_unprocessed_data['JulianBatchNumber'] = rd_nn_unprocessed_data['JulianBatchNumber'].apply(
    lambda x: str((ord(x[0]) - 64) * 10 + {'A': 1, 'B': 2, 'E': 6, 'H': 3, 'D': 5, 'C': 4, 'G': 7}.get(x[1], 0)) + x[2:]
)

rd_nn_unprocessed_data.to_excel('output/rd_nn_processed.xlsx', index=False)
print("Preprocessing complete. The output file is saved as 'rd_nn_processed.xlsx' at folder 'output' ")
