INSERT INTO dbo.DimCustomer (CustomerID, CustomerName, Region, CustomerSegment, IsActive)
VALUES
('C4001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C4002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C4003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C4004', 'City Cycle House', 'East', 'SMB', 'Y'),
('C4005', 'Adventure Works Outlet', 'North', 'SMB', 'Y'),
('C4006', 'Fabrikam Trails', 'West', 'SMB', 'Y');

INSERT INTO dbo.DimProduct (ProductID, ProductName, Category, UnitPrice, IsActive)
VALUES
('P400', 'Trail Helmet', 'Accessories', 45.00, 'Y'),
('P401', 'Road Bike', 'Bikes', 1200.00, 'Y'),
('P402', 'Mountain Bike', 'Bikes', 1500.00, 'Y'),
('P403', 'Cycling Jersey', 'Apparel', 60.00, 'Y'),
('P404', 'Water Bottle', 'Accessories', 15.00, 'Y');

INSERT INTO dbo.FactSales (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
VALUES
('SO40001', '2026-04-01', 'C4001', 'P401', 1, 1200.00, 1200.00, 'Complete'),
('SO40002', '2026-04-01', 'C4002', 'P403', 4, 60.00, 240.00, 'Complete'),
('SO40003', '2026-04-02', 'C4003', 'P400', 2, 45.00, 90.00, 'Complete'),
('SO40004', '2026-04-02', 'C4004', 'P402', 1, 1500.00, 1500.00, 'Complete'),
('SO40005', '2026-04-03', 'C4005', 'P404', 10, 15.00, 150.00, 'Complete'),
('SO40006', '2026-04-03', 'C4006', 'P401', 1, 1200.00, 1200.00, 'Complete'),
('SO40007', '2026-04-04', 'C4001', 'P403', 3, 60.00, 180.00, 'Complete'),
('SO40008', '2026-04-04', 'C4002', 'P404', 8, 15.00, 120.00, 'Complete');
