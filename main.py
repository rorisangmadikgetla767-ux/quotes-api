from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database import get_connection
from models import Quote, LineItem
from datetime import datetime

app = FastAPI(title="Quotes API")

@app.get("/")
def root():
    return {"message": "Quotes API is running!"}

@app.get("/quotes")
def get_quotes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes")
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
        cursor.execute("SELECT * FROM quotes WHERE id = %s", (id,))
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
            "INSERT INTO quotes (quote_id, quote_number, customer_id, vehicle_id, description_q, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
            (quote.Quote_id, quote.Quote_number, quote.Customer_Id, quote.Vehicle_id, quote.description_Q, quote.created_by)
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
            "UPDATE quotes SET description_q = %s, created_by = %s WHERE id = %s",
            (quote.description_Q, quote.created_by, id)
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
        cursor.execute("DELETE FROM quotes WHERE id = %s", (id,))
        conn.commit()
        return {"message": "Quote deleted successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

    
# Steps in creating a line-item

# 1st: Initialize the client instance

# 2nd: Manage DB connection lifecycle

# 3rd: Create Pydantic validation schemas

# 4th: Implement route handlers

# Prisma queries fully asynchronous

# 5th Run the application : uvicorn main:app --reload

# app.get("/") registers a GET request endpoint
# ("/api/quotes/{id}/line-items")-> It is the URL path. {id}-> is a variable for the quote ID
@app.get("/api/quotes/{id}/line-items")
def get_line_items(id: int):
    try:
        # conn stores the database connection
        # get_connection()-> calls my function from database.py to connect to Render
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM line_items WHERE quote_id = %s", (id,))
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return JSONResponse(status_code = 500, content={"error": str(e)})

# POST - Add a line item to a quote 
@app.post("/api/quotes/{id}/line-items", status_code=201)        
def create_line_item(id: int, item: LineItem):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        total = int(item.quantity) * float(item.unit_price)
        cursor.execute(
            "INSERT INTO line_items(quote_id, description, quantity, unit_price, total) VALUES (%s, %s, %s, %s, %s)",
            (id, item.description, item.quantity, float(item.unit_price), float(total))
            
        ) 
        conn.commit()
        return {"message":"Line item has been created"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
      
@app.post("/api/quotes/{id}/approve")
def approve_quote(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Check if the quote exists
        cursor.execute("SELECT * FROM quotes WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Quote not found")
        
        columns = [col[0] for col in cursor.description]
        quote = dict(zip(columns, row))
        
        # 2. Check for the current status 
        if quote["status"] == "approved":
            raise HTTPException(status_code=400, detail="Quote already approved")
        if quote["status"] == "rejected":
            raise HTTPException(status_code=400, detail="Rejected quotes must be resubmitted")
        # 4. Update status, approved_by, approved_at
        approved_by = 1
        cursor.execute(
            """
            UPDATE quotes
            SET status = 'approved', approved_by = %s, approved_at = %s
            WHERE id = %s
            """,
            (approved_by, datetime.now(), id)
        )
        conn.commit()

        # 5. Return the updated quote
        cursor.execute("SELECT * FROM quotes WHERE id = %s", (id,))
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



# REJECT a quote

@app.post("/api/quotes/{id}/reject")
def reject_quote(id: int, body: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Check if the quote exists
        cursor.execute("SELECT * FROM quotes WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Quote not found")

        columns = [col[0] for col in cursor.description]
        quote = dict(zip(columns, row))

        # 2. Check current status
        if quote["status"] == "approved":
            raise HTTPException(status_code=400, detail="Quote already approved")
        if quote["status"] == "rejected":
            raise HTTPException(status_code=400, detail="rejected quotes must be resubmitted")
        
        
        # 3 Get rejection_reason from 
        rejection_reason = body.get("rejection_reason")
        if not rejection_reason:
            raise HTTPException(status_code=400, detail="Rejection reason required")
        
        #4. Update status and rejection_reason
        cursor.execute("""
                       
            UPDATE quotes 
            SET status = 'rejected', rejection_reason = %s
            WHERE id = %s 
            
            """,
            (rejection_reason, id)
        )
        conn.commit()
        
        #5 Return the updated quote
        cursor.execute("SELECT * FROM quotes WHERE id = %s", (id,))
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        
           


