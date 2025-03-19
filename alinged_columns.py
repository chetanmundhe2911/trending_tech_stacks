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
