-- Adminer 5.0.6 PostgreSQL 17.4 (Debian 17.4-1.pgdg120+2) dump
-- connect "crypto_prices";

DROP TABLE IF EXISTS "price_book";
DROP SEQUENCE IF EXISTS price_book_id_seq;
CREATE SEQUENCE price_book_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1;

CREATE TABLE "public"."price_book" (
                                       "id" smallint DEFAULT nextval('price_book_id_seq') NOT NULL,
                                       "name" text NOT NULL,
                                       "price" numeric NOT NULL,
                                       "created_at" timestamp NOT NULL
) WITH (oids = false);


-- 2025-03-23 19:26:33 UTC