from flask import Flask, request, jsonify
import dbconnection as dbc
import pandas as pd
import json
import os
from pandas import json_normalize
from matplotlib import pyplot as plt
import numpy as np
import _request as rq

reportAPI = Flask(__name__)
global df_config

@reportAPI.route('/customers/<string:marca>/<string:pais>', methods=["GET"])
def get_customers(marca:str,pais:str):
    # global df_config
       
    try:
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'ipserver']
        servername = df.iat[0]
        
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'database']
        dbname =  df.iat[0]

        conn = dbc.db_connect(servername, dbname,'icgadmin','masterkey')
        dfcustomers = dbc.db_datosclientes(conn, 2022)
        print(dfcustomers)
        js = dfcustomers.to_json(orient = 'records')
        parsed = json.loads(js)
        
    except Exception as e:
        print("Error de URL : ", e)
    else:
        return (json.dumps(parsed, indent=4)), 201

@reportAPI.route('/RFM/<string:marca>/<string:pais>', methods=["GET"])
def get_rfm(marca:str,pais:str):
    # global df_config
       
    try:
                
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'ipserver']
        servername = df.iat[0]
        
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'database']
        dbname =  df.iat[0]
        
        conn = dbc.db_connect(servername, dbname,'icgadmin','masterkey')
        dfcustomers = dbc.db_rfmdata(conn)
        df= dfcustomers
        df = df.astype({"orderdate": 'M'})
        df_recency = df.groupby(by='customername', as_index=False)['orderdate'].max()
        df_recency.columns = ['CustomerName', 'LastPurchaseDate']
        recent_date =  df_recency['LastPurchaseDate'].max()
        
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
        rfm_df[['CustomerName', 'RFM_Score', 'Customer_segment']].head(20)

        rfm_df.to_csv(marca + '_' + pais + '.csv', index=False)
       
        # plt.pie(rfm_df.Customer_segment.value_counts(),
        #         labels=rfm_df.Customer_segment.value_counts().index,
        #         autopct='%.0f%%')
        # plt.show()
        js = rfm_df.to_json(orient = 'records')
        parsed = json.loads(js)

    except Exception as e:
        print("Error de URL : ", e)
    else:
        return (json.dumps(parsed, indent=4)), 201

def get_rfm_data(marca:str,pais:str):
      
    try:
                
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'ipserver']
        servername = df.iat[0]
        
        df = df_config.loc[df_config['pais'].eq(pais) & df_config['marca'].eq(marca), 'database']
        dbname =  df.iat[0]
        
        jsondata  = rq.get_sales_db(servername, dbname)  

        dict = json.loads(jsondata)
        print(dict)
        df2 = json_normalize(dict['technologies']) 
        
        df= pd.read_json(jsondata, orient='index')
        df = df.astype({"orderdate": 'M'})

        df_recency = df.groupby(by='customername', as_index=False)['orderdate'].max()
        df_recency.columns = ['CustomerName', 'LastPurchaseDate']
        recent_date =  df_recency['LastPurchaseDate'].max()
        
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
        rfm_df[['CustomerName', 'RFM_Score', 'Customer_segment']].head(20)

        rfm_df.to_csv(marca + '_' + pais + '.csv', index=False)
       
        # plt.pie(rfm_df.Customer_segment.value_counts(),
        #         labels=rfm_df.Customer_segment.value_counts().index,
        #         autopct='%.0f%%')
        # plt.show()
        js = rfm_df.to_json(orient = 'records')
        parsed = json.loads(js)

    except Exception as e:
        print("Error de URL : ", e)
    else:
        return (json.dumps(parsed, indent=4)), 201


if __name__ == '__main__':
    try:
        pathuser = os.environ['USERPROFILE'] ##carpeta de usuario
        folderapp = os.getcwd() ##carpeta de ejecución de la app
        pathapp = folderapp + '\config.json'
        with open(pathapp, 'r') as file:
            data = json.load(file)
                
        df_config = json_normalize(data['Data'])
        # print(df_config)
    except IOError as e:
        ferror = open( pathuser + '/' + 'error.log', 'w')
        ferror.write(str(e))
        ferror.close()
    else: 
        #ejecutar principal
        # get_rfm_data('VS','col')
        reportAPI.run(debug=True)
        # print(rfm_df)
        