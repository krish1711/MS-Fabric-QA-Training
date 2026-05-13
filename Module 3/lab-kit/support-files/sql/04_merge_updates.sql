MERGE dbo.SalesOrders AS target
USING dbo.OrderUpdates AS source
    ON target.OrderID = source.OrderID
WHEN MATCHED AND source.OperationType = 'UPDATE' THEN
    UPDATE SET
        target.OrderDate = source.OrderDate,
        target.CustomerID = source.CustomerID,
        target.ProductID = source.ProductID,
        target.Quantity = source.Quantity,
        target.UnitPrice = source.UnitPrice,
        target.OrderAmount = source.OrderAmount,
        target.OrderStatus = source.OrderStatus
WHEN NOT MATCHED AND source.OperationType = 'INSERT' THEN
    INSERT (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
    VALUES (source.OrderID, source.OrderDate, source.CustomerID, source.ProductID, source.Quantity, source.UnitPrice, source.OrderAmount, source.OrderStatus);
