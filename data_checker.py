
import pandas as pd

# Load the data
df = pd.read_csv("demo_data.csv")

# Check for missing values
missing_values = df[df.isnull().any(axis=1)]

# Flag empty client names
empty_names = df[df['Client Name'].str.strip() == ""]

# Print summary
print("=== MISSING VALUE ROWS ===")
print(missing_values)
print("\n=== EMPTY CLIENT NAME ROWS ===")
print(empty_names)

# Save results (optional)
df['Flag - Missing Info'] = df.isnull().any(axis=1) | df['Client Name'].str.strip().eq("")
df.to_csv("review_output.csv", index=False)
print("\nResults saved to review_output.csv")
