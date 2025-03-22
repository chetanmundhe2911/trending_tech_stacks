import pandas as pd



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


# Remove "business_category" from the Group/Color section and add "aligned_business_category" instead.
# Ensure "sportpesa_v_gaming" is also part of the Grouping
# "sportpesa_v_gaming" determines whether a transaction belongs to "Gaming", "SportPesa", or "Other".
# Keep it as a secondary grouping or use it to filter data.
# Check the VALUE Field
# The Value field (SelectedMetricField (Custom)) is likely tx_value or tx_count.
# Total Transaction Count (tx_count)
# Total Transaction Value (tx_value)
# If needed, sum the total value for each "aligned_business_category".
# Review Small Multiples (Options_CP)
# If this field segments the data further, ensure it does not exclude "Gaming" or "SportPesa" transactions from the main visualization.
# Expected Results After This Fix:
# ✅ "Gaming" transactions will now appear as "Betting Industry" in the chart!
# ✅ "SportPesa" transactions will correctly appear under "Betting Company - SportPesa" instead of "Other"!
# ✅ Your pie chart will now accurately compare "Gaming", "SportPesa", and other business categories.




# ```
# 1️⃣ Where does Gaming fall in the business categories?
# Previously, many transactions under "Gaming" were being categorized as "Other", which made it difficult to track them separately.
# Now, all Gaming transactions are explicitly categorized as "Betting Industry" in the new column (aligned_business_category).
# Dashboard Fix:
# Use "aligned_business_category" instead of "business_category" to ensure Gaming's transactions show under "Betting Industry" in visualizations.

# 2️⃣ Where does SportPesa fall?
# In the original dataset, SportPesa transactions were mostly under "Other".
# Now, transactions under "SportPesa" are grouped as "Betting Company - SportPesa" instead of "Other", making them clearly visible on the dashboard.
# Dashboard Fix:
# Create a filter or breakdown where "SportPesa" is properly displayed under "Betting Company - SportPesa".

# 3️⃣ How do they compare relative to all other categories?
# Before, "Gaming" and "SportPesa" were mixed into "Other" and lacked uniqueness for clear comparisons.
# Now, with distinct categories (Betting Industry & Betting Company - SportPesa), you can:
# Compare transaction volumes & values of "Gaming" vs "SportPesa" vs "Other" business categories.
# Keep Finance & Investment, Retail, and other sectors intact in your dashboard visuals.
# Dashboard Fix:
# Modify your pie chart to use "aligned_business_category" so each category is properly segmented.
# How to Implement in QuickSight (or Any BI Tool)
# Load the updated dataset (transformed_data.csv) into QuickSight.
# Change the fields used in charts:
# Replace business_category with aligned_business_category in the data visualization.
# Ensure "Betting Industry" and "Betting Company - SportPesa" appear correctly.
# Modify Pie Chart or Bar Chart settings:
# Group the data based on "aligned_business_category".
# Compare their transaction value or count to see the share of gaming & betting.


# ✅ Gaming transactions would be properly classified under Betting Industry, not "Other".
# ✅ SportPesa will be treated as a distinct business category for clearer analysis.





