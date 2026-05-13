IF OBJECT_ID('dbo.FactSales', 'U') IS NOT NULL
    DROP TABLE dbo.FactSales;

IF OBJECT_ID('dbo.DimProduct', 'U') IS NOT NULL
    DROP TABLE dbo.DimProduct;

IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL
    DROP TABLE dbo.DimCustomer;

CREATE TABLE dbo.DimCustomer
(
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    Region VARCHAR(20) NOT NULL,
    CustomerSegment VARCHAR(30) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

CREATE TABLE dbo.DimProduct
(
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(30) NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

CREATE TABLE dbo.FactSales
(
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL,
    OrderAmount DECIMAL(18,2) NOT NULL,
    OrderStatus VARCHAR(20) NOT NULL
);
