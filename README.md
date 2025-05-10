# Advanced_Database_Concepts_Assignment

# Phase 1
## Domain
E-commerse database service
## Main Entities & Relationships
1. Customer (CustomerID, Name, Email, Phone, Address)
2. Product (ProductID, Name, Category, Price, Stock)
3. Order (OrderID, CustomerID, OrderDate, Status)
4. OrderItem (OrderID, ProductID, Quantity, Price)
5. Payment (PaymentID, OrderID, Amount, Method, PaymentDate)
6. Shipment (ShipmentID, OrderID, ShipmentDate, Carrier, TrackingNumber)
## Constraints
1. Every order is linked to one customer.
2. Each order may have multiple products.
3. Each product can appear in many orders.
4. Every order has one payment and one shipment.
## Sample data
For sample data creation I am going to use https://mockaroo.com/
## ER model
### Entities and Attributes

#### 1. Customer
- **CustomerID** *(Primary Key)*
- Name
- Email *(Unique)*
- Phone
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
| Places        | Customer – Order                | 1:N         | A customer can place multiple orders.            |
| Contains      | Order – Product (via OrderItem) | M:N         | Orders can contain many products and vice versa. |
| PaidWith      | Order – Payment                 | 1:1         | Each order has exactly one payment.              |
| ShippedWith   | Order – Shipment                | 1:1         | Each order has exactly one shipment.             |

---

#### Constraints
- **Email** in `Customer` must be unique.
- **Stock** in `Product` must be ≥ 0.
- **OrderItem** must reference valid `OrderID` and `ProductID`.
- **Payment** and **Shipment** are optional at creation but required for fulfillment.

---

#### Relationships:
- `Customer (1) — (N) Order`
- `Order (1) — (M) OrderItem — (M) Product`
- `Order (1) — (1) Payment`
- `Order (1) — (1) Shipment`


# Phase 2
## ER Model
## Normalized Relational Schema (up to 3NF)
