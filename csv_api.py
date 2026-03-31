from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="CSV-to-API Service")

@app.on_event("startup")
def load_data():
    try:
        df = pd.read_csv("csv_input.csv")
        if "id" not in df.columns:
            raise ValueError("CSV must contain an 'id' column")
        df.set_index("id", inplace=True)  # optimize lookups
        app.state.df = df
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")

@app.get("/items")
def get_items():
    return app.state.df.reset_index().to_dict(orient="records")

@app.get("/items/{item_id}")
def get_item(item_id: int):
    try:
        record = app.state.df.loc[item_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
    return record.to_dict()