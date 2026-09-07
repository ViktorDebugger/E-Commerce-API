SELECT 'CREATE DATABASE ecommerce_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ecommerce_test')\gexec
