import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Connecting to sqlite database
conn = sqlite3.connect(r'D:\develop\SqlTools\databases\olistDB.db')

# Query for the selected columns in the tables
query = """
SELECT
    c.customer_unique_id,
    c.customer_city,
    o.order_purchase_timestamp,
    oi.price,
    oi.freight_value,
    p.product_category_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
AND c.customer_unique_id IS NOT NULL
AND oi.price > 0
AND o.order_purchase_timestamp BETWEEN '2016-01-01' AND '2018-12-31';
"""

df = pd.read_sql(query, conn)
conn.close()

# Making sure the format is set to date-only
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp']).dt.date

# Total Price Calculation
df['TotalPrice'] = df['price'] + df['freight_value']

# RFM analysis
current_date = pd.to_datetime(df['order_purchase_timestamp']).max() + pd.Timedelta(days=1)

rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': ['max', 'count'],
    'TotalPrice': 'sum'
})

# Flattening columns
rfm.columns = ['LastPurchaseDate', 'Frequency', 'Monetary']
rfm.reset_index(inplace=True)

# Calculating Recency
rfm['Recency'] = (current_date - pd.to_datetime(rfm['LastPurchaseDate'])).dt.days
rfm.drop(columns=['LastPurchaseDate'], inplace=True)

# Now adding the most frequent product category and city per customer
category_pref = df.groupby('customer_unique_id')['product_category_name'].agg(lambda x: x.mode()[0]
if not x.mode().empty else None).reset_index()

city_pref = df.groupby('customer_unique_id')['customer_city'].agg(lambda x: x.mode()[0]
if not x.mode().empty else None).reset_index()

rfm = rfm.merge(category_pref, on='customer_unique_id').merge(city_pref, on='customer_unique_id')

# Normalizing rfm data
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Segment'] = kmeans.fit_predict(rfm_scaled)

# Map segments to labels
segment_map = {
    0: 'High Value',
    1: 'Loyal',
    2: 'At-Risk',
    3: 'Low Value'
}
rfm['Segment'] = rfm['Segment'].map(segment_map)

# Saving results here
rfm.to_csv('olist_customer_segmentation.csv', index=False)
print("Customer segmentation completed. Results have been saved to olist_customer_segmentation.csv")