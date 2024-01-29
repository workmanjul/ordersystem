ALTER TABLE orders
ALTER COLUMN payment_status SET DEFAULT 'processing';

UPDATE orders
SET payment_status = 'processing'
WHERE payment_status = 0;
