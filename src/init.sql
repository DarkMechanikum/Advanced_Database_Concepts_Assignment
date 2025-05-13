-- Schema setup for ecommerce_db

CREATE TABLE "Customers" (
  CustomerID INT PRIMARY KEY,
  Name VARCHAR,
  Email VARCHAR UNIQUE,
  Phone VARCHAR UNIQUE,
  Address VARCHAR
);

CREATE TABLE "Products" (
  ProductID INT PRIMARY KEY,
  Name VARCHAR,
  Category VARCHAR,
  Description VARCHAR,
  Price DECIMAL CHECK (Price >= 0),
  Stock INT CHECK (Stock >= 0)
);

CREATE TABLE "Orders" (
  OrderID INT PRIMARY KEY,
  CustomerID INT REFERENCES "Customers"(CustomerID),
  OrderDate DATE, 
  Status VARCHAR CHECK (Status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled'))
);

CREATE TABLE "OrderItems" (
  OrderID INT REFERENCES "Orders"(OrderID),
  ProductID INT REFERENCES "Products"(ProductID),
  Quantity INT CHECK (Quantity >= 0),
  Price DECIMAL CHECK (Price >= 0),
  PRIMARY KEY (OrderID, ProductID)
);

-- Indexes using HASH
CREATE INDEX idx_customers_id_hash ON "Customers" USING HASH (CustomerID);
CREATE INDEX idx_customers_email_hash ON "Customers" USING HASH (Email);
CREATE INDEX idx_customers_phone_hash ON "Customers" USING HASH (Phone);

CREATE INDEX idx_products_id_hash ON "Products" USING HASH (ProductID);
CREATE INDEX idx_products_category_hash ON "Products" USING HASH (Category);

CREATE INDEX idx_orders_id_hash ON "Orders" USING HASH (OrderID);
CREATE INDEX idx_orders_customerid_hash ON "Orders" USING HASH (CustomerID);

CREATE INDEX idx_orderitems_productid_hash ON "OrderItems" USING HASH (ProductID);
CREATE INDEX idx_orders_orderdate_btree ON "Orders"(OrderDate);
-- Data loading
\COPY "Customers" FROM '/data/Customers.csv' CSV HEADER;
\COPY "Products" FROM '/data/Products.csv' CSV HEADER;
\COPY "Orders" FROM '/data/Orders.csv' CSV HEADER;
\COPY "OrderItems" FROM '/data/OrderItems.csv' CSV HEADER;
