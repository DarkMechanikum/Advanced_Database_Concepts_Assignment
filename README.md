# Advanced_Database_Concepts_Assignment

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
- Price
- Stock *(Non-negative)*

#### 3. Order
- **OrderID** *(Primary Key)*
- CustomerID *(Foreign Key → Customer)*
- OrderDate
- Status *(e.g., Pending, Shipped, Delivered)*

#### 4. OrderItem *(Associative Entity)*
- **OrderID** *(Foreign Key → Order)*
- **ProductID** *(Foreign Key → Product)*
- Quantity *(Non-negative)*
- Price *(at time of purchase)*
- **Primary Key**: *(OrderID, ProductID)*

#### 5. Payment
- **PaymentID** *(Primary Key)*
- OrderID *(Foreign Key → Order)*
- Amount
- Method *(e.g., Card, PayPal)*
- PaymentDate

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
- **Email** in `Customer` must be unique.
- **Stock** in `Product` must be ≥ 0.
- **Quantity** in `OrderItem` must be ≥ 0. 
- **OrderItem** must reference valid `OrderID` and `ProductID`.
- **Payment** and **Shipment** are optional at creation but required for fulfillment.

# Phase 2
## ER Diagram
![ER](https://github.com/user-attachments/assets/4af3a77b-00ae-4b88-bfc8-2870d2cf62e9)

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
- Hashed for Customers and Products (fast retrieval by ID)
- Sorted for Orders (often queried by date)
- Hashed for Payments and Shipments (fast retrieval by ID)

## Indexing Strategy
- Primary Index: On OrderID, CustomerID, ProductID
- Secondary Index: On Product.Category, Customer.Email, Customer.Phone, Order.Status

## Justification:

- Clustered index speeds up chronological order queries.
- Secondary index on Product.Category helps with category-based reports.
