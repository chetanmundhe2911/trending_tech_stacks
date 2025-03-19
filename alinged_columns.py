import pandas as pd

# Load the dataset
file_path = "data.csv"  # Change this to your actual file path
df = pd.read_csv(file_path)

# Define mapping logic
def categorize_business(row):
    """
    Function to align 'sportpesa_v_gaming' with 'business_category'
    so that all Gaming & SportPesa entries have a clearly defined category.
    """
    if row['sportpesa_v_gaming'] == 'Gaming':
        return 'Betting Industry'  # Assign a unique identifier for Gaming transactions
    elif row['sportpesa_v_gaming'] == 'SportPesa':
        return 'Betting Company - SportPesa'  # Assign SportPesa transactions uniquely
    return row['business_category']  # Keep other categories as they are

# Apply the mapping function
df['aligned_business_category'] = df.apply(categorize_business, axis=1)

# Save the transformed dataset for sharing
transformed_file = "transformed_data.csv"
df.to_csv(transformed_file, index=False)

# View the first few rows to verify
df.head()

```
How to Fix in QuickSight:
Replace "business_category" with "aligned_business_category"
Your transformed dataset has a new column "aligned_business_category" that correctly maps "Gaming" as "Betting Industry" and "SportPesa" as "Betting Company - SportPesa".
Action:
Remove "business_category" from the Group/Color section and add "aligned_business_category" instead.
Ensure "sportpesa_v_gaming" is also part of the Grouping
"sportpesa_v_gaming" determines whether a transaction belongs to "Gaming", "SportPesa", or "Other".
Keep it as a secondary grouping or use it to filter data.
Check the VALUE Field
The Value field (SelectedMetricField (Custom)) is likely tx_value or tx_count.
Make sure that it represents either:
Total Transaction Count (tx_count)
Total Transaction Value (tx_value)
If needed, sum the total value for each "aligned_business_category".
Review Small Multiples (Options_CP)
If this field segments the data further, ensure it does not exclude "Gaming" or "SportPesa" transactions from the main visualization.
Expected Results After This Fix:
✅ "Gaming" transactions will now appear as "Betting Industry" in the chart!
✅ "SportPesa" transactions will correctly appear under "Betting Company - SportPesa" instead of "Other"!
✅ Your pie chart will now accurately compare "Gaming", "SportPesa", and other business categories.

Final Step
After updating this, check if the pie chart labels clearly reflect "Betting Industry" and "Betting Company - SportPesa".
If the changes don’t reflect immediately, try refreshing or updating the dataset in QuickSight.



```

