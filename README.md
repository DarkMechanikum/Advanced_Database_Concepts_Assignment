# Advanced Database Concepts Assignment by Vladimir Shtarev

# Phase 1
## Domain
E-commerse database service
## ER model
### Entities and Attributes

#### 1. Customer
- **CustomerID** *(Primary Key)*
- Name
- Email *(Unique)*
- Phone *(Unique)*
- Address

#### 2. Product
- **ProductID** *(Primary Key)*
- Name
- Category *(Secondary Key)*
- Description
- Price *(Non-negative)*
- Stock *(Non-negative)*

#### 3. Order
- **OrderID** *(Primary Key)*
- CustomerID *(Foreign Key → Customer)*
- OrderDate *(Secondary key for clustered index)*
- Status *(e.g., Pending, Shipped, Delivered)*

#### 4. OrderItem *(Associative Entity)*
- **OrderID** *(Foreign Key → Order)*
- **ProductID** *(Foreign Key → Product)*
- Quantity *(Non-negative)*
- Price *(at time of purchase, Non-negative)*
- **Primary Key**: *(OrderID, ProductID)*

#### 5. Payment
- **PaymentID** *(Primary Key)*
- OrderID *(Foreign Key → Order)*
- Amount *(Non-negative)*
- Method *(e.g., Card, PayPal)*
- PaymentDate *(Secondary Key)*

#### 6. Shipment
- **ShipmentID** *(Primary Key)*
- OrderID *(Foreign Key → Order)*
- ShipmentDate
- Carrier
- TrackingNumber

---

### Relationships

| Relationship  | Entities Involved               | Cardinality | Description                                      |
|---------------|---------------------------------|-------------|--------------------------------------------------|
| Placed        | Customer – Order                | 1:M         | A customer can place multiple orders.            |
| Contains      | Order – Product (via OrderItem) | 1:M         | Order can contain many products.                 |
| PaidWith      | Order – Payment                 | 1:1         | Each order has exactly one payment.              |
| ShippedWith   | Order – Shipment                | 1:1         | Each order has exactly one shipment.             |

---
- `Customer (1) — (M) Order`
- `Order (1) — (M) OrderItem`
- `OrderItem (1) — (1) Product`
- `Order (1) — (1) Payment`
- `Order (1) — (1) Shipment`

---

#### Constraints
- **Email** in `Customer` must be unique.
- **Phone** in `Customer` must be unique.
- **Stock** in `Product` must be ≥ 0.
- **Price** in `Product` must be ≥ 0.
- **Quantity** in `OrderItem` must be ≥ 0.
- **Amount** in `Payment` must be ≥ 0.
- **OrderItem** must reference valid `OrderID` and `ProductID`.
- **Payment** and **Shipment** are optional at creation but required for fulfillment.

# Phase 2
## ER Diagram
![Untitled](https://github.com/user-attachments/assets/48ef3a94-464a-41c2-9ff4-b7cf0a2a5a4c)

## Normalized Relational Schema (up to 3NF)
### Schema
Customer(CustomerID, Name, Email, Phone, Address)
Product(ProductID, Name, Category, Price, Stock, Description)
Order(OrderID, CustomerID, OrderDate, Status)
OrderItem(OrderID, ProductID, Quantity, Price)
Payment(PaymentID, OrderID, Amount, Method, PaymentDate)
Shipment(ShipmentID, OrderID, ShipmentDate, Carrier, TrackingNumber)

### Keys:
#### Primary Keys:
- CustomerID, ProductID, OrderID, PaymentID, ShipmentID
- (OrderID, ProductID) for OrderItem
#### Foreign Keys:
- Order.CustomerID → Customer.CustomerID
- OrderItem.OrderID → Order.OrderID
- OrderItem.ProductID → Product.ProductID
- Payment.OrderID → Order.OrderID
- Shipment.OrderID → Order.OrderID

## File Organization
- Heap for everything, since PostgreSQL does not support Hash-based data storage. Every usecase suggests retrieval by ID as quick as possible, so I am using hash-based indexing to achieve similar performance. 
I also use clustered data organisation for orders, for them to be sorted by date, this improves performance for fetching ranges of orders for statistical purposes.

## Indexing Strategy
- Primary Index: On ID of each entity, since most usecases suggest retrieval of a certain entity by it's ID.
- Secondary Index: On Product.Category, Customer.Email, Customer.Phone, Order.Status, Order.Date.
Since at login user uses his email/phone, not his ID, secondary keys are necessary.
Secondary index of products by category is necessary for browsing a category of items, so we must support retrieval of all products of a certain category.
Secondary composite key of Orderes by status with filtering by userID is needed for displaying all orders of a certain status for a certain user.
Secondary index of Orders by date (cluster index) is used for fast statistical data fetching.
# Phase 3 

## The results of the development are present in this repository, please see the /src directory for source files

# Phase 4

## Performance evaluation
Since In my project I only use a thousand rows in each table, there is no great difference in time for fetching data with and without hash-based indexes.
However, it is significant enough to clearly see the difference even at such small scale. It is important to keep in mind, that as size of the database grows, the data fetching algorithm start playing way more important role.

### Example queries without indexing: 
- Index Scan using "Customers_pkey" on "Customers" (cost=0.28..8.29 rows=1 width=72) (actual time=0.121..0.135 rows=1 loops=1)
  Index Cond: (customerid = 981)
  Planning Time: 0.889 ms
  Execution Time: 0.232 ms

- Seq Scan on "Orders" (cost=0.00..19.50 rows=1 width=20) (actual time=0.110..0.222 rows=2 loops=1)
  Filter: (customerid = 981)
  Rows Removed by Filter: 998
  Planning Time: 0.655 ms
  Execution Time: 0.399 ms

- Seq Scan on "Products" (cost=0.00..32.00 rows=5 width=101) (actual time=0.687..1.004 rows=1 loops=1)
  Filter: (lower((category)::text) = 'tools'::text)
  Rows Removed by Filter: 999
  Planning Time: 1.119 ms
  Execution Time: 1.068 ms
  
- Seq Scan on "Orders" (cost=0.00..22.00 rows=285 width=20) (actual time=0.016..0.765 rows=282 loops=1)
  Filter: ((orderdate >= '2025-01-01'::date) AND (orderdate <= '2025-03-31'::date))
  Rows Removed by Filter: 718
  Planning Time: 0.556 ms
  Execution Time: 1.516 ms
### Example queries with indexing: 
- Index Scan using idx_customers_id_hash on "Customers" (cost=0.00..8.02 rows=1 width=72) (actual time=0.020..0.021 rows=1 loops=1)
  Index Cond: (customerid = 981)
  Planning Time: 0.597 ms
  Execution Time: 0.058 ms
  
- Index Scan using idx_orders_customerid_hash on "Orders" (cost=0.00..8.02 rows=1 width=20) (actual time=0.070..0.072 rows=2 loops=1)
  Index Cond: (customerid = 981)
  Planning Time: 0.390 ms
  Execution Time: 0.125 ms
  
- Seq Scan on "Products" (cost=0.00..32.00 rows=5 width=101) (actual time=0.325..0.486 rows=1 loops=1)
  Filter: (lower((category)::text) = 'tools'::text)
  Rows Removed by Filter: 999
  Planning Time: 0.629 ms
  Execution Time: 0.516 ms
  
- Seq Scan on "Orders" (cost=0.00..22.00 rows=285 width=20) (actual time=0.007..0.116 rows=282 loops=1)
  Filter: ((orderdate >= '2025-01-01'::date) AND (orderdate <= '2025-03-31'::date))
  Rows Removed by Filter: 718
  Planning Time: 0.426 ms
  Execution Time: 0.185 ms
