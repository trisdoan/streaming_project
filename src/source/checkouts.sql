create table checkouts (
    checkout_id STRING,
    user_id INT,
    product_id STRING,
    payment_method STRING,
    total_amount DECIMAL(5,2),
    shipping_address STRING,
    billing_address STRING,
    user_agent STRING,
    ip_address STRING,
    datetime_occured TIMESTAMP(3),
    processing_time as PROCTIME(),
    
    watermark for datetime_occured as datetime_occured - interval '15' second

)
with (
    'connector' = '{{ connector}}',
    'topic' = '{{ topic }}',
    'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
    'properties.group.id' = '{{ consumer_group_id}}' , 
    'scan.startup.mode' = '{{ scan_startup_mode }}',
    'format' = '{{ format }}'
);