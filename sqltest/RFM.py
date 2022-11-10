from matplotlib import pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
import dbconnection as dbc
from datetime import datetime

# importing the data
# df = pd.read_excel( 'rfmdata.xlsx' )
# print(df)

conn = dbc.db_connect('200.46.56.106\\WEBPMA,61525', 'ECOMPMA','icgadmin','masterkey')
df = dbc.db_rfmdata(conn)
df = df.astype({"orderdate": 'M'})

df_recency = df.groupby(by='customername', as_index=False)['orderdate'].max()
df_recency.columns = ['CustomerName', 'LastPurchaseDate']
recent_date = df_recency['LastPurchaseDate'].max()

df_recency['Recency'] = df_recency['LastPurchaseDate'].apply(lambda x: (recent_date - x).days)

frequency_df = df.drop_duplicates().groupby(by=['customername'], as_index=False)['orderdate'].count()
frequency_df.columns = ['CustomerName', 'Frequency']

df['Total'] = df['sales']*df['quantity']
monetary_df = df.groupby(by='customername', as_index=False)['Total'].sum()
monetary_df.columns = ['CustomerName', 'Monetary']

rf_df = df_recency.merge(frequency_df, on='CustomerName')
rfm_df = rf_df.merge(monetary_df, on='CustomerName').drop(columns='LastPurchaseDate')

rfm_df['R_rank'] = rfm_df['Recency'].rank(ascending=False)
rfm_df['F_rank'] = rfm_df['Frequency'].rank(ascending=True)
rfm_df['M_rank'] = rfm_df['Monetary'].rank(ascending=True)

# normalizing the rank of the customers
rfm_df['R_rank_norm'] = (rfm_df['R_rank']/rfm_df['R_rank'].max())*100
rfm_df['F_rank_norm'] = (rfm_df['F_rank']/rfm_df['F_rank'].max())*100
rfm_df['M_rank_norm'] = (rfm_df['F_rank']/rfm_df['M_rank'].max())*100

rfm_df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)

rfm_df['RFM_Score'] = 0.15*rfm_df['R_rank_norm']+0.28 * \
	rfm_df['F_rank_norm']+0.57*rfm_df['M_rank_norm']
rfm_df['RFM_Score'] *= 0.05
rfm_df = rfm_df.round(2)
rfm_df[['CustomerName', 'RFM_Score']].head(7)

rfm_df["Customer_segment"] = np.where(rfm_df['RFM_Score'] >
									4.5, "Top Customers",
									(np.where(
										rfm_df['RFM_Score'] > 4,
										"High value Customer",
										(np.where(
	rfm_df['RFM_Score'] > 3,
							"Medium Value Customer",
							np.where(rfm_df['RFM_Score'] > 1.6,
							'Low Value Customers', 'Lost Customers'))))))

print(rfm_df[['CustomerName', 'RFM_Score', 'Customer_segment']])

rfm_df.to_csv('BBW_PAM.csv', index=False)

plt.pie(rfm_df.Customer_segment.value_counts(),
		labels=rfm_df.Customer_segment.value_counts().index,
		autopct='%.0f%%')
plt.show()
