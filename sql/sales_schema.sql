create table if not exists public.sales_records (
    id bigint generated always as identity primary key,
    order_id text not null unique,
    customer_name text not null,
    customer_email text not null,
    product_name text not null,
    category text not null,
    quantity integer not null,
    unit_price numeric(12,2) not null,
    total_amount numeric(12,2) not null,
    order_date timestamptz not null,
    region text not null,
    sales_rep text not null,
    status text not null
);
