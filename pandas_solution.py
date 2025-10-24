import sqlite3
import pandas as pd 

def pandas_solution(db_path: str, out_path: str, min_age: int = 18, max_age: int = 35):
    conn = sqlite3.connect(db_path)

    customers = pd.read_sql_query(
        "SELECT CustomerID, Age FROM Customers WHERE Age BETWEEN ? AND ?",
        conn, params=(min_age, max_age)
    )
    sales = pd.read_sql_query("SELECT SaleID, CustomerID FROM Sales", conn)
    sales_items = pd.read_sql_query("SELECT SaleID, ItemID, Quantity FROM SalesItems", conn)
    items = pd.read_sql_query("SELECT ItemID, ItemName FROM Items", conn)

    df = (
        sales.merge(customers, on="CustomerID")
             .merge(sales_items, on="SaleID")
             .merge(items, on="ItemID")
    )

    df["Quantity"] = df["Quantity"].fillna(0).astype(int)
    grouped = (
        df.groupby(["CustomerID", "Age", "ItemName"], as_index=False)["Quantity"]
          .sum()
          .query("Quantity > 0")
          .sort_values(["CustomerID", "ItemName"])
    )

    grouped.rename(columns={"CustomerID": "Customer", "ItemName": "Item"}, inplace=True)
    grouped.to_csv(out_path, sep=";", index=False)
    conn.close()
    print(f"✅ Pandas solution: wrote {len(grouped)} rows to {out_path}")
