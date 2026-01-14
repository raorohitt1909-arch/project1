CREATE DATABASE sales_dbb;
USE sales_dbb;

CREATE TABLE sales_data (
    order_id INT,
    order_date DATE,
    customer_id INT,
    customer_name VARCHAR(100),
    product VARCHAR(50),
    category VARCHAR(50),
    quantity INT,
    price FLOAT,
    region VARCHAR(50),
    total_sales FLOAT,
    month INT,
    year INT
);

select * from sales_data;

SELECT product, SUM(total_sales) AS revenue
FROM sales_data
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

SELECT year, month, SUM(total_sales) AS monthly_sales
FROM sales_data
GROUP BY year, month
ORDER BY year, month;


SELECT region, SUM(total_sales) AS revenue
FROM sales_data
GROUP BY region
ORDER BY revenue DESC;


SELECT customer_name, SUM(total_sales) AS spending
FROM sales_data
GROUP BY customer_name
ORDER BY spending DESC
LIMIT 10;








