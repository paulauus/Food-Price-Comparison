-- Creates the tables in the database.

DROP TABLE IF EXISTS retailer, unit, product, price;

CREATE TABLE retailer (
    retailer_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    retailer_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (retailer_id)
);

CREATE TABLE unit (
    unit_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    unit_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (unit_id)
);

CREATE TABLE product (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY,
    product_name VARCHAR(255) NOT NULL,
    retailer_id SMALLINT NOT NULL,
    product_image_url TEXT,
    PRIMARY KEY (product_id),
    FOREIGN KEY (retailer_id) REFERENCES retailer(retailer_id)
);

CREATE TABLE price (
    price_id BIGINT GENERATED ALWAYS AS IDENTITY,
    product_id BIGINT NOT NULL,
    item_price NUMERIC(8, 2),
    loyalty_item_price NUMERIC(8, 2),
    unit_price NUMERIC(8, 2),
    loyalty_unit_price NUMERIC(8, 2),
    unit_id SMALLINT,
    price_date TIMESTAMP NOT NULL,
    out_of_stock BOOLEAN NOT NULL,
    PRIMARY KEY (price_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (unit_id) REFERENCES unit(unit_id)
);
