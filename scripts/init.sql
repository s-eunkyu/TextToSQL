drop table if exists orders;
drop table if exists customers;

create table customers (
  customer_id serial primary key,
  name text not null,
  created_at timestamp not null default now()
);

create table orders (
  order_id serial primary key,
  customer_id int not null references customers(customer_id),
  ordered_at timestamp not null,
  amount numeric(12,2) not null,
  status text not null
);

insert into customers (name, created_at) values
('Kim', now() - interval '40 days'),
('Lee', now() - interval '20 days'),
('Park', now() - interval '10 days');

insert into orders (customer_id, ordered_at, amount, status) values
(1, now() - interval '35 days', 12000, 'completed'),
(1, now() - interval '5 days',  34000, 'completed'),
(2, now() - interval '15 days', 18000, 'completed'),
(2, now() - interval '2 days',  22000, 'refunded'),
(3, now() - interval '1 days',  56000, 'completed');