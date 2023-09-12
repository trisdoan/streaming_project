create table clicks (
    click_id STRING,
    user_id INT,
    product_id STRING,
    product STRING,
    price DOUBLE,
    url STRING,
    user_agent STRING,
    ip_address STRING,
    datetime_occured TIMESTAMP(3),
    processing_time AS PROCTIME(),
    watermark for datetime_occured as datetime_occured - interval '15' second
) with (
    'connector' = '{{ connector }}',
    'topic' = '{{ topic }}',
    'properties.bootstrap.servers' = '{{ bootstrap_servers }}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_stratup_mode }}',
    'format' = '{{ format }}'
);