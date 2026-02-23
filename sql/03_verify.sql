\dt

SELECT COUNT(*) AS customers FROM customers;
SELECT COUNT(*) AS sellers FROM sellers;
SELECT COUNT(*) AS products FROM products;
SELECT COUNT(*) AS orders FROM orders;
SELECT COUNT(*) AS order_items FROM order_items;
SELECT COUNT(*) AS payments FROM payments;
SELECT COUNT(*) AS reviews FROM reviews;
SELECT COUNT(*) AS geolocation FROM geolocation;
SELECT COUNT(*) AS category_translation FROM category_translation;

SELECT * FROM customers LIMIT 5;
SELECT * FROM orders LIMIT 5;
SELECT * FROM order_items LIMIT 5;