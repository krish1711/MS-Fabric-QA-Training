INSERT INTO dbo.DimCustomer (CustomerID, CustomerName, Region, CustomerSegment, IsActive)
VALUES
('C5001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C5002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C5003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C5004', 'City Cycle House', 'East', 'SMB', 'Y'),
('C5005', 'Adventure Works Outlet', 'North', 'SMB', 'Y'),
('C5006', 'Fabrikam Trails', 'West', 'SMB', 'Y');

INSERT INTO dbo.DimProduct (ProductID, ProductName, Category, UnitPrice, IsActive)
VALUES
('P500', 'Trail Helmet', 'Accessories', 45.00, 'Y'),
('P501', 'Road Bike', 'Bikes', 1200.00, 'Y'),
('P502', 'Mountain Bike', 'Bikes', 1500.00, 'Y'),
('P503', 'Cycling Jersey', 'Apparel', 60.00, 'Y'),
('P504', 'Water Bottle', 'Accessories', 15.00, 'Y');

INSERT INTO dbo.FactSales (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
VALUES
('SO50001', '2026-04-01', 'C5001', 'P501', 1, 1200.00, 1200.00, 'Complete'),
('SO50002', '2026-04-01', 'C5002', 'P503', 4, 60.00, 240.00, 'Complete'),
('SO50003', '2026-04-02', 'C5003', 'P500', 2, 45.00, 90.00, 'Complete'),
('SO50004', '2026-04-02', 'C5004', 'P502', 1, 1500.00, 1500.00, 'Complete'),
('SO50005', '2026-04-03', 'C5005', 'P504', 10, 15.00, 150.00, 'Complete'),
('SO50006', '2026-04-03', 'C5006', 'P501', 1, 1200.00, 1200.00, 'Complete'),
('SO50007', '2026-04-04', 'C5001', 'P503', 3, 60.00, 180.00, 'Complete'),
('SO50008', '2026-04-04', 'C5002', 'P504', 8, 15.00, 120.00, 'Complete'),
('SO50009', '2026-04-05', 'C5003', 'P503', 5, 60.00, 300.00, 'Complete'),
('SO50010', '2026-04-05', 'C5004', 'P500', 2, 45.00, 90.00, 'Complete');
