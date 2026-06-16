from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import get_connection
from models import Quote

app = FastAPI(title="Quotes API")

@app.get("/")
def root():
    return {"message": "Quotes API is running!"}

@app.get("/quotes")
def get_quotes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[QUOTES]")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/quotes/{id}")
def get_quote(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[QUOTES] WHERE Id = ?", id)
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Quote not found")
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/quotes", status_code=201)
def create_quote(quote: Quote):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO [dbo].[QUOTES] 
            (Quote_id, Quote_number, Customer_Id, Vehicle_id, description_Q, created_by)
            VALUES (?, ?, ?, ?, ?, ?)""",
            quote.Quote_id, quote.Quote_number, quote.Customer_Id,
            quote.Vehicle_id, quote.description_Q, quote.created_by
        )
        conn.commit()
        return {"message": "Quote created successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.put("/quotes/{id}")
def update_quote(id: int, quote: Quote):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE [dbo].[QUOTES] SET
            description_Q = ?, created_by = ?
            WHERE Id = ?""",
            quote.description_Q, quote.created_by, id
        )
        conn.commit()
        return {"message": "Quote updated successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/quotes/{id}")
def delete_quote(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM [dbo].[QUOTES] WHERE Id = ?", id)
        conn.commit()
        return {"message": "Quote deleted successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})