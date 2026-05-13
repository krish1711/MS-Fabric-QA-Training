INSERT INTO dbo.Customers (CustomerID, CustomerName, Region, CustomerType, IsActive) VALUES
('C3001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C3002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C3003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C3004', 'City Cycle House', 'East', 'SMB', 'Y');

INSERT INTO dbo.Products (ProductID, ProductName, Category, StandardPrice) VALUES
('P300', 'Trail Helmet', 'Accessories', 45.00),
('P301', 'Road Bike', 'Bikes', 1200.00),
('P302', 'Mountain Bike', 'Bikes', 1500.00),
('P303', 'Cycling Jersey', 'Apparel', 60.00);

INSERT INTO dbo.SalesOrders (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus) VALUES
('SO30001', '2026-03-05', 'C3001', 'P301', 2, 1200.00, 2400.00, 'Shipped'),
('SO30002', '2026-03-06', 'C3002', 'P303', 5, 60.00, 300.00, 'Shipped'),
('SO30003', '2026-03-08', 'C3003', 'P300', 4, 45.00, 180.00, 'Processing'),
('SO30004', '2026-03-10', 'C3004', 'P302', 1, 1500.00, 1500.00, 'Shipped'),
('SO30005', '2026-03-11', 'C3001', 'P303', 3, 58.00, 174.00, 'Processing'),
('SO30006', '2026-03-12', 'C3002', 'P300', 6, 45.00, 270.00, 'Shipped');

INSERT INTO dbo.OrderUpdates (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus, OperationType) VALUES
('SO30003', '2026-03-08', 'C3003', 'P300', 5, 45.00, 225.00, 'Shipped', 'UPDATE'),
('SO30007', '2026-03-15', 'C3001', 'P300', 2, 45.00, 90.00, 'Shipped', 'INSERT');
