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
- Category
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
- Quantity
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
| Contains      | Order – Product (via OrderItem) | M:M         | Orders can contain many products and vice versa. |
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
- **OrderItem** must reference valid `OrderID` and `ProductID`.
- **Payment** and **Shipment** are optional at creation but required for fulfillment.

# Phase 2
## ER Diagram
![ER](https://github.com/user-attachments/assets/4af3a77b-00ae-4b88-bfc8-2870d2cf62e9)

## Normalized Relational Schema (up to 3NF)
