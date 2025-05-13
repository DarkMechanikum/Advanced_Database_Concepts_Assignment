from flask import render_template, request
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
    )

def register_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        results, columns = [], []
        query = ""
        input_type = request.form.get("input_type")
        input_value = request.form.get("input_value")

        # Determine which predefined query to run
        if request.method == "POST":
            try:
                conn = get_connection()
                cur = conn.cursor()

                if request.form.get("custom_query"):
                    query = request.form["custom_query"]
                elif input_type == "customer_orders":
                    query = f'SELECT * FROM "Order" WHERE CustomerID = {int(input_value)}'
                elif input_type == "order_items":
                    query = f'SELECT * FROM "OrderItem" WHERE OrderID = {int(input_value)}'
                elif input_type == "customer_info":
                    query = f'SELECT * FROM "Customer" WHERE CustomerID = {int(input_value)}'
                elif input_type == "product_description":
                    query = f'SELECT Description FROM "Product" WHERE ProductID = {int(input_value)}'

                if query:
                    cur.execute(query)
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        results = cur.fetchall()

                conn.commit()
                cur.close()
                conn.close()

            except Exception as e:
                results = [["Error"], [str(e)]]

        return render_template("index.html", results=results, columns=columns, query=query)
