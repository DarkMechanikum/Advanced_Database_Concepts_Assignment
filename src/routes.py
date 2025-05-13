from flask import render_template, request, redirect
from src.database import get_connection

def register_routes(app):
    @app.route('/')
    def dashboard():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM \"Customers\"")
        total_customers = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM \"Orders\"")
        total_orders = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM \"Products\"")
        total_products = cur.fetchone()[0]

        cur.execute("""
            SELECT c.CustomerID, c.Name, COUNT(o.OrderID) AS OrderCount
            FROM "Customers" c
            JOIN "Orders" o ON c.CustomerID = o.CustomerID
            GROUP BY c.CustomerID, c.Name
            ORDER BY OrderCount DESC
            LIMIT 5
        """)
        top_customers = cur.fetchall()

        cur.execute("""
            SELECT p.ProductID, p.Name, SUM(oi.Quantity) AS TotalSold
            FROM "Products" p
            JOIN "OrderItems" oi ON p.ProductID = oi.ProductID
            GROUP BY p.ProductID, p.Name
            ORDER BY TotalSold DESC
            LIMIT 5
        """)
        top_products = cur.fetchall()

        cur.execute("""
            SELECT o.OrderID, o.CustomerID, SUM(oi.Quantity * oi.Price) AS Total
            FROM "Orders" o
            JOIN "OrderItems" oi ON o.OrderID = oi.OrderID
            GROUP BY o.OrderID, o.CustomerID
            ORDER BY Total DESC
            LIMIT 5
        """)
        biggest_orders = cur.fetchall()

        conn.close()

        return render_template("dashboard.html",
                               total_customers=total_customers,
                               total_orders=total_orders,
                               total_products=total_products,
                               top_customers=top_customers,
                               top_products=top_products,
                               biggest_orders=biggest_orders)

    @app.route('/customer', methods=['GET', 'POST'])
    def customer():
        conn = get_connection()
        cur = conn.cursor()
        customer = None
        message = None

        if request.method == 'POST':
            if 'create' in request.form:
                try:
                    cur.execute("""
                        INSERT INTO "Customers" (CustomerID, Name, Email, Phone, Address)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        request.form['new_id'],
                        request.form['new_name'],
                        request.form['new_email'],
                        request.form['new_phone'],
                        request.form['new_address']
                    ))
                    conn.commit()
                    message = "Customer created successfully."
                except Exception as e:
                    conn.rollback()
                    message = f"Error: {e}"

            elif 'update' in request.form:
                try:
                    cur.execute("""
                        UPDATE "Customers"
                        SET Name = %s, Email = %s, Phone = %s, Address = %s
                        WHERE CustomerID = %s
                    """, (
                        request.form['name'],
                        request.form['email'],
                        request.form['phone'],
                        request.form['address'],
                        request.form['id']
                    ))
                    conn.commit()
                    message = "Customer updated successfully."
                except Exception as e:
                    conn.rollback()
                    message = f"Error: {e}"

            elif 'search' in request.form:
                customer_id = request.form['search_id']
                cur.execute("SELECT * FROM \"Customers\" WHERE CustomerID = %s", (customer_id,))
                customer = cur.fetchone()

        conn.close()
        return render_template('customer.html', customer=customer, message=message)


    @app.route('/order', methods=['GET', 'POST'])
    def order():
        conn = get_connection()
        cur = conn.cursor()
        message = None
        order = None
        order_items = []

        try:
            if request.method == 'POST':
                if 'search' in request.form:
                    order_id = request.form['search_id']
                    cur.execute('SELECT * FROM "Orders" WHERE OrderID = %s', (order_id,))
                    order = cur.fetchone()
                    cur.execute('SELECT ProductID, Quantity, Price FROM "OrderItems" WHERE OrderID = %s', (order_id,))
                    order_items = cur.fetchall()

                elif 'update' in request.form:
                    cur.execute('''
                        UPDATE "Orders" SET CustomerID = %s, OrderDate = %s, Status = %s
                        WHERE OrderID = %s
                    ''', (
                        request.form['customer_id'],
                        request.form['order_date'],
                        request.form['status'],
                        request.form['id']
                    ))
                    conn.commit()
                    message = "Order updated."

                elif 'create' in request.form:
                    cur.execute('''
                        INSERT INTO "Orders" (OrderID, CustomerID, OrderDate, Status)
                        VALUES (%s, %s, %s, %s)
                    ''', (
                        request.form['new_id'],
                        request.form['new_customer_id'],
                        request.form['new_order_date'],
                        request.form['new_status']
                    ))
                    conn.commit()
                    message = "Order created."

                elif 'add_item' in request.form:
                    cur.execute('''
                        INSERT INTO "OrderItems" (OrderID, ProductID, Quantity, Price)
                        VALUES (%s, %s, %s, %s)
                    ''', (
                        request.form['order_id'],
                        request.form['product_id'],
                        request.form['quantity'],
                        request.form['price']
                    ))
                    conn.commit()
                    message = "Item added to order."

                elif 'delete_item' in request.form:
                    cur.execute('''
                        DELETE FROM "OrderItems" WHERE OrderID = %s AND ProductID = %s
                    ''', (
                        request.form['order_id'],
                        request.form['product_id']
                    ))
                    conn.commit()
                    message = "Item removed."

        except Exception as e:
            conn.rollback()
            message = f"Error: {e}"

        if order and not order_items:
            cur.execute('SELECT ProductID, Quantity, Price FROM "OrderItems" WHERE OrderID = %s', (order[0],))
            order_items = cur.fetchall()

        cur.close()
        conn.close()
        return render_template("order.html", message=message, order=order, order_items=order_items)


    @app.route('/product', methods=['GET', 'POST'])
    def product():
        conn = get_connection()
        cur = conn.cursor()
        message = None
        product = None
        total_sold = 0

        try:
            if request.method == 'POST':
                if 'search' in request.form:
                    pid = request.form['search_id']
                    cur.execute('SELECT * FROM "Products" WHERE ProductID = %s', (pid,))
                    product = cur.fetchone()

                    cur.execute('''
                        SELECT SUM(Quantity) FROM "OrderItems"
                        WHERE ProductID = %s
                    ''', (pid,))
                    total_sold = cur.fetchone()[0] or 0

                elif 'update' in request.form:
                    cur.execute('''
                        UPDATE "Products"
                        SET Name = %s, Category = %s, Description = %s, Price = %s, Stock = %s
                        WHERE ProductID = %s
                    ''', (
                        request.form['name'],
                        request.form['category'],
                        request.form['description'],
                        request.form['price'],
                        request.form['stock'],
                        request.form['id']
                    ))
                    conn.commit()
                    message = "Product updated."

                elif 'create' in request.form:
                    cur.execute('''
                        INSERT INTO "Products" (ProductID, Name, Category, Description, Price, Stock)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        request.form['new_id'],
                        request.form['new_name'],
                        request.form['new_category'],
                        request.form['new_description'],
                        request.form['new_price'],
                        request.form['new_stock']
                    ))
                    conn.commit()
                    message = "Product created."

        except Exception as e:
            conn.rollback()
            message = f"Error: {e}"

        cur.close()
        conn.close()
        return render_template("product.html", product=product, total_sold=total_sold, message=message)


    @app.route('/category', methods=['GET', 'POST'])
    def category():
        conn = get_connection()
        cur = conn.cursor()
        message = None
        products = []
        searched_category = None
        categories = []

        try:
            # Always load category list
            cur.execute('SELECT DISTINCT Category FROM "Products" ORDER BY Category')
            categories = [row[0] for row in cur.fetchall()]

            if request.method == 'POST':
                searched_category = request.form['category']
                cur.execute('''
                    SELECT ProductID, Name, Description, Price, Stock
                    FROM "Products"
                    WHERE LOWER(Category) = LOWER(%s)
                ''', (searched_category,))
                products = cur.fetchall()
                if not products:
                    message = f"No products found in category: {searched_category}"
        except Exception as e:
            message = f"Error: {e}"

        cur.close()
        conn.close()
        return render_template("category.html",
                               products=products,
                               searched_category=searched_category,
                               categories=categories,
                               message=message)

    @app.route('/stock', methods=['GET', 'POST'])
    def stock():
        conn = get_connection()
        cur = conn.cursor()
        products = []
        threshold = None
        message = None

        if request.method == 'POST':
            try:
                threshold = int(request.form['threshold'])
                cur.execute('''
                    SELECT ProductID, Name, Category, Stock, Price
                    FROM "Products"
                    WHERE Stock < %s
                    ORDER BY Stock ASC
                ''', (threshold,))
                products = cur.fetchall()
                if not products:
                    message = f"No products found with stock below {threshold}."
            except Exception as e:
                message = f"Error: {e}"

        cur.close()
        conn.close()
        return render_template("stock.html", products=products, threshold=threshold, message=message)



    @app.route('/cli', methods=['GET', 'POST'])
    def cli():
        conn = get_connection()
        cur = conn.cursor()
        query = ""
        message = None
        results = []
        columns = []

        if request.method == 'POST':
            try:
                query = request.form['query']
                cur.execute(query)
                if cur.description:  # SELECT or similar
                    columns = [desc[0] for desc in cur.description]
                    results = cur.fetchall()
                    message = "Query executed successfully."
                else:
                    conn.commit()
                    message = "Query executed successfully (no results)."
            except Exception as e:
                conn.rollback()
                message = f"Error: {e}"

        cur.close()
        conn.close()
        return render_template("cli.html", query=query, message=message, results=results, columns=columns)

    @app.route('/statistics', methods=['GET', 'POST'])
    def statistics():
        conn = get_connection()
        cur = conn.cursor()
        orders = []
        message = None
        total_revenue = 0
        order_count = 0
        start_date = end_date = ""

        if request.method == 'POST':
            try:
                start_date = request.form['start_date']
                end_date = request.form['end_date']

                cur.execute('''
                    SELECT o.OrderID, o.CustomerID, o.OrderDate, o.Status,
                           SUM(oi.Quantity * oi.Price) as Total
                    FROM "Orders" o
                    JOIN "OrderItems" oi ON o.OrderID = oi.OrderID
                    WHERE o.OrderDate BETWEEN %s AND %s
                    GROUP BY o.OrderID, o.CustomerID, o.OrderDate, o.Status
                    ORDER BY o.OrderDate
                ''', (start_date, end_date))
                orders = cur.fetchall()

                order_count = len(orders)
                total_revenue = sum(o[4] for o in orders)

            except Exception as e:
                message = f"Error: {e}"

        cur.close()
        conn.close()
        return render_template("statistics.html",
                               orders=orders,
                               message=message,
                               order_count=order_count,
                               total_revenue=round(total_revenue, 2),
                               start_date=start_date,
                               end_date=end_date)

    
    
