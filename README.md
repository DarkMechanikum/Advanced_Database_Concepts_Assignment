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
- OrderDate
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
- Hashed for everything, since every usecase suggests retrieval by ID as quick as possible. 
Though clustered index may be useful for some usecases we can use secondary indexes and some backend logic for this, while it is much more important to provide fast retrieval of a certain entity at any given moment, since those operations are more frequent.
## Indexing Strategy
- Primary Index: On ID of each entity, since most usecases suggest retrieval of a certain entity by it's ID.
- Secondary Index: On Product.Category, Customer.Email, Customer.Phone, Order.Status.
Since at login user uses his email/phone, not his ID, secondary keys are necessary.
Secondary index of products by category is necessary for browsing a category of items, so we must support retrieval of all products of a certain category.
Secondary composite key of Orderes by status with filtering by userID is needed for displaying all orders of a certain status for a certain user.
Secondary index of Payments by PaymentDate is useful for statistics of the platform as a whole.


