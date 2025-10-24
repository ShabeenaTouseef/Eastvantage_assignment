import sqlite3
import pandas as pd 

def sql_solution(db_path: str, out_path: str, min_age: int = 18, max_age: int = 35):
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT c.CustomerID AS Customer, c.Age AS Age, i.ItemName AS Item,
           SUM(COALESCE(si.Quantity, 0)) AS Quantity
    FROM Customers c
    JOIN Sales s ON c.CustomerID = s.CustomerID
    JOIN SalesItems si ON s.SaleID = si.SaleID
    JOIN Items i ON si.ItemID = i.ItemID
    WHERE c.Age BETWEEN {min_age} AND {max_age}
    GROUP BY c.CustomerID, c.Age, i.ItemName
    HAVING Quantity > 0
    ORDER BY c.CustomerID, i.ItemName;
    """
    df = pd.read_sql_query(query, conn)
    if not df.empty:
        df["Quantity"] = df["Quantity"].astype(int)
    df.to_csv(out_path, sep=";", index=False)
    conn.close()
    print(f"✅ SQL solution: wrote {len(df)} rows to {out_path}")
