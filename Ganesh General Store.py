import pandas as pd

# Load the two Excel files
file1 = "C:\\Users\\91941\\Desktop\\Office\\Ganesh General Store\\Invoice with invo no..xlsx"  # Replace with actual file path
file2 = "C:\\Users\\91941\\Desktop\\Office\\Ganesh General Store\\PR with invoice no..xlsx"

df1 = pd.read_excel(file1, sheet_name="Sheet1", dtype={'Invoice No.': str})
df2 = pd.read_excel(file2, sheet_name="Sheet1", dtype={'Invoice No.': str})

# Selecting only the Invoice No. column and dropping any NaN values
df1_invoices = df1[['Supplier Invoice No.']].dropna()
df2_invoices = df2[['Supplier Invoice No.']].dropna()

df1_invoices['Supplier Invoice No.'] = df1_invoices['Supplier Invoice No.'].astype(str).str.strip()
df2_invoices['Supplier Invoice No.'] = df2_invoices['Supplier Invoice No.'].astype(str).str.strip()

missing_in_df2 = df1_invoices[~df1_invoices['Supplier Invoice No.'].isin(df2_invoices['Supplier Invoice No.'])]

missing_in_df1 = df2_invoices[~df2_invoices['Supplier Invoice No.'].isin(df1_invoices['Supplier Invoice No.'])]


with pd.ExcelWriter("Missing_Invoices.xlsx") as writer:
    missing_in_df2.to_excel(writer, sheet_name="Missing in File2", index=False)
    missing_in_df1.to_excel(writer, sheet_name="Missing in File1", index=False)

print("Comparison complete. Missing invoice numbers saved in 'Missing_Invoices.xlsx'.")
