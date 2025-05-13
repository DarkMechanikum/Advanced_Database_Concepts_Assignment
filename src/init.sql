-- Schema setup for ecommerce_db

CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY,
  Name VARCHAR,
  Email VARCHAR UNIQUE,
  Phone VARCHAR UNIQUE,
  Address VARCHAR
);

CREATE TABLE Products (
  ProductID INT PRIMARY KEY,
  Name VARCHAR,
  Category VARCHAR,
  Description VARCHAR,
  Price DECIMAL CHECK (Price >= 0),
  Stock INT CHECK (Stock >= 0)
);

CREATE TABLE Orders (
  OrderID INT PRIMARY KEY,
  CustomerID INT REFERENCES Customers(CustomerID),
  OrderDate DATE,
  Status VARCHAR CHECK (Status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled'))
);

CREATE TABLE OrderItems (
  OrderID INT REFERENCES Orders(OrderID),
  ProductID INT REFERENCES Products(ProductID),
  Quantity INT CHECK (Quantity >= 0),
  Price DECIMAL CHECK (Price >= 0),
  PRIMARY KEY (OrderID, ProductID)
);

\COPY Customers FROM '/data/Customers.csv' CSV HEADER;
\COPY Products FROM '/data/Products.csv' CSV HEADER;
\COPY Orders FROM '/data/Orders.csv' CSV HEADER;
\COPY OrderItems FROM '/data/OrderItems.csv' CSV HEADER;
