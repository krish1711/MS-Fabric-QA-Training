DROP TABLE IF EXISTS dbo.RegionSalesCTAS;
DROP TABLE IF EXISTS dbo.OrderUpdates;
DROP TABLE IF EXISTS dbo.SalesOrders;
DROP TABLE IF EXISTS dbo.Products;
DROP TABLE IF EXISTS dbo.Customers;

CREATE TABLE dbo.Customers (
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(200) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    CustomerType VARCHAR(50) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

CREATE TABLE dbo.Products (
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    StandardPrice DECIMAL(18, 2) NOT NULL
);

CREATE TABLE dbo.SalesOrders (
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL,
    OrderStatus VARCHAR(30) NOT NULL
);

CREATE TABLE dbo.OrderUpdates (
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL,
    OrderStatus VARCHAR(30) NOT NULL,
    OperationType VARCHAR(20) NOT NULL
);
