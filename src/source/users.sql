create temporary table users (
    id INT,
    username STRING,
    PASSWORD STRING,
    PRIMARY KEY (id) NOT ENFORCED
) with (
    'connector' = '{{ connector }}',
    'url' = '{{ url }}',
    'table-name' = '{{ table_name }}',
    'username' = '{{ username }}',
    'password' = '{{ password }}',
    'driver' = '{{ driver }}'
);