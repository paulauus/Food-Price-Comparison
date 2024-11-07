#!/bin/bash
set -e

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Create the database if it does not exist
psql -U "$DB_USER" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    psql -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"

echo "Database '$DB_NAME' created or already exists."

# Initialize tables in the specified database
psql -U "$DB_USER" -d "$DB_NAME" -f schema.sql

echo "Database and tables have been initialized."
