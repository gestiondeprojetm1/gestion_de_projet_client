-- Migration additive et idempotente pour les bases PostgreSQL existantes.
ALTER TABLE products
    ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 0;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'ck_products_stock_non_negative'
    ) THEN
        ALTER TABLE products
            ADD CONSTRAINT ck_products_stock_non_negative CHECK (stock >= 0);
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'ck_orders_quantity_positive'
    ) THEN
        ALTER TABLE orders
            ADD CONSTRAINT ck_orders_quantity_positive CHECK (quantity > 0);
    END IF;
END $$;
