import pyodbc
import pandas as pd


print("About to insert Hagi:")
	#Add your own SQL Server IP address, PORT, UID, PWD and Database
conn = pyodbc.connect('DRIVER={FreeTDS};SERVER=10.2.0.211\C3AEOZL;PORT=44644;DATABASE=VSARGECOM;UID=icgadmin;PWD=masterkey', autocommit=True)
df = pd.read_sql_query("SELECT top 5 REFPROVEEDOR as reference, codbarras,  stock, minimo, fechastock, PNETO, PBRUTO  FROM vwstockTarifa", conn)
# cur = conn.cursor()
	#This is just an example
# cur.execute(f"select top 5 numpedido from pedventacab")
# conn.commit()
print(df)
# cur.close()
conn.close()