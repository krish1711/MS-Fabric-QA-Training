# Day 3 Lakehouse update notebook
# Attach this notebook to the Lakehouse `lh_day3_contoso`
# before running the code.

spark.sql(
    """
    UPDATE lake_orders
    SET
        Quantity = 5,
        OrderAmount = 225.00,
        OrderStatus = 'Shipped'
    WHERE OrderID = 'SO30003'
    """
)

spark.sql(
    """
    INSERT INTO lake_orders
    VALUES ('SO30007', DATE '2026-03-15', 'C3001', 'P300', 2, 45.00, 90.00, 'Shipped')
    """
)

display(
    spark.sql(
        """
        SELECT OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus
        FROM lake_orders
        ORDER BY OrderID
        """
    )
)

display(
    spark.sql(
        """
        DESCRIBE HISTORY lake_orders
        """
    )
)
