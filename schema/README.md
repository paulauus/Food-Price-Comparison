# Database Schema

## Setting Up the Database Locally

This guide will help you create and initialise the database with tables using the provided schema.sql and init_db.sh files.

### Prerequisites

- **PostgreSQL**: Ensure PostgreSQL is installed and running locally. Installation instructions.

- **Environment Variables**: Create a .env file with the following variables:
```
DB_USER=your_username      # PostgreSQL username
DB_NAME=food_prices_db     # Database name
```
Replace your_username with your PostgreSQL username, or update the script with your preferred settings.

### Instructions

1. **Edit the .env File**: Open the .env file and set your PostgreSQL user credentials and desired database name.

2. **Run the Setup Script**: The init_db.sh script will create the database if it doesn’t already exist and initialise the tables using schema.sql. Run the script with:
```
./init_db.sh
```

3. **Verify the Setup**:

- The script outputs whether the database was created or already existed.

- To confirm the tables were created, you can connect to the database and list tables:
```
psql -U "$DB_USER" -d "$DB_NAME" -c "\dt"
```
