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
In order to run the application, docker engine and docker compose plugin must be installed. To build and run the application, simply run the build.sh bash script. 

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


### I/O cost calculation

- Block size (B): 4096 bytes (4 KB)
- Estimated record size (R): 128 bytes
- Number of records (N): 1000


bfr = floor(4096 / 128) = 32 records per block
b = ceil(1000 / 32) = 32 blocks

A full scan of the `Customers` table requires **32 block accesses**.

---

#### Estimated Scan Costs for All Tables

| Table       | Est. Record Size (bytes) | # Records | Blocking Factor | # Blocks (Scan Cost) |
|-------------|---------------------------|-----------|------------------|-----------------------|
| Customers   | 128                       | 1000      | 32               | 32 blocks             |
| Products    | 160                       | 500       | 25               | 20 blocks             |
| Orders      | 96                        | 10,000    | 42               | 239 blocks            |
| OrderItems  | 48                        | 20,000    | 85               | 236 blocks            |

---

#### Indexed Lookup Cost (Rough Estimate)

**Query Example:**

```sql
SELECT * FROM "Customers" WHERE CustomerID = 42;
```

**Cost Breakdown:**

- B-tree/Hash index probe: ~2–3 I/Os
- Table fetch: 1 I/O
- **Total**: ~3–4 I/Os

Compared to 32 blocks for a full scan, this is a major efficiency gain.

---

### Spanned vs Unspanned data organisation

Since I am using PostgreSQL for my implementation, I use spanned data organisation. 
However, I can provide some assumptions and calculations, based on my specific database

Let's illustrate it with the Products table:

**Assumptions:**

- Block size: 4096 bytes
- Record size: 160 bytes (includes all columns)
- Total records: 500

---

#### Spanned File Organization

```text
bfr_spanned = floor(4096 / 160) = 25
blocks_spanned = ceil(500 / 25) = 20
```

**20 blocks** needed — minimal space wasted due to tight packing.

---

#### Unspanned File Organization

```text
bfr_unspanned = floor(4096 / 160) = 25
Each record must fully fit into one block.
blocks_unspanned = ceil(500 / 25) = 20 (same count, but more internal fragmentation)
```

But consider a case where `R = 205 bytes`:

```text
bfr_unspanned = floor(4096 / 205) = 19
blocks_unspanned = ceil(500 / 19) = 27 blocks
```

Unspanned org uses **more blocks** due to unused space at the end of blocks.

---

#### Effects of spanned and unspanned data organisation

| Feature                               | Spanned                             | Unspanned                       |
|---------------------------------------|-------------------------------------|---------------------------------|
| Record spans block?                   | Allowed                             | Not allowed                     |
| Space utilization                     | Higher                              | Lower                           |
| Simplicity of block access            | Harder (record split across blocks) | Simpler                         |
| Ideal for                             | Variable or large records           | Fixed-size, small records       |
| Overhead                              | Higher parsing complexity           | Higher block count and I/O cost |

---

- PostgreSQL uses **spanned heap files** by default for flexibility and efficiency.
- **Unspanned** files may result in **higher I/O** costs due to unused block space.
- Understanding record size and access patterns helps in designing optimal file storage formats.

---

### Application interface

![image](https://github.com/user-attachments/assets/b53baab7-0648-4725-85a4-7f84813e72c4)
![image](https://github.com/user-attachments/assets/d1e74c16-89b8-481d-998e-3ac3f62a9563)
![image](https://github.com/user-attachments/assets/57e7adb2-deea-43bc-9658-ee7471b0307e)
![image](https://github.com/user-attachments/assets/346de6ab-3f09-4846-9794-748416133548)
![image](https://github.com/user-attachments/assets/363f844f-1cab-453b-80fc-5bb4f7a3bd76)
![image](https://github.com/user-attachments/assets/c3c93385-be8f-47a0-8b0e-e781a33f3035)
![image](https://github.com/user-attachments/assets/62a42e7b-581b-4a5d-a362-8fa3d61f9ea4)
![image](https://github.com/user-attachments/assets/651ca6e6-fa29-467b-a7d5-613e9c79f9c3)

