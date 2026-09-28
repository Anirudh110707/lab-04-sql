"""Read, clean, and upload mock CSV data to MySQL."""

import logging
import os

import mysql.connector
import pandas as pd


# Configure logging so the program reports its progress.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def read_data(filename):
    """Read a CSV file and return a pandas DataFrame."""
    logging.info("Reading data from %s", filename)

    data = pd.read_csv(filename)

    # Standardize column names to lowercase.
    data.columns = data.columns.str.strip().str.lower()

    logging.info("Read %d rows", len(data))

    return data


def clean_data(data):
    """Remove rows with missing values and prepare data for MySQL."""
    logging.info("Cleaning data")

    # Remove rows that contain missing values.
    cleaned = data.dropna().copy()

    # Make sure numeric columns contain integers.
    cleaned["id"] = cleaned["id"].astype(int)
    cleaned["age"] = cleaned["age"].astype(int)
    cleaned["group"] = cleaned["group"].astype(int).astype(str)

    # Convert the time column into Python time values.
    cleaned["time"] = pd.to_datetime(
        cleaned["time"],
        format="mixed",
        errors="coerce",
    ).dt.time

    # Remove rows where the time value could not be converted.
    cleaned = cleaned.dropna().copy()

    logging.info(
        "Cleaning complete: %d rows remain",
        len(cleaned),
    )

    return cleaned


def load_data(data, table):
    """Create the mock table and upload the cleaned DataFrame to MySQL."""
    if table != "mock":
        raise ValueError("The table name must be 'mock'.")

    logging.info("Connecting to MySQL")

    connection = None
    cursor = None

    try:
        # Get database information from environment variables.
        connection = mysql.connector.connect(
            host=os.environ["DBHOST"],
            user=os.environ["DBUSER"],
            password=os.environ["DBPASS"],
            database=os.environ["DBNAME"],
        )

        cursor = connection.cursor()

        # Create the table if it does not already exist.
        create_query = """
        CREATE TABLE IF NOT EXISTS mock (
            id BIGINT PRIMARY KEY,
            `group` VARCHAR(255),
            email VARCHAR(255),
            age INT,
            city VARCHAR(255),
            time TIME
        )
        """

        cursor.execute(create_query)

        # Remove old data so the program can safely be rerun.
        cursor.execute("DELETE FROM mock")

        # Parameterized INSERT query.
        insert_query = """
        INSERT INTO mock (
            id,
            `group`,
            email,
            age,
            city,
            time
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Insert each cleaned DataFrame row into MySQL.
        for _, row in data.iterrows():
            values = (
                int(row["id"]),
                str(row["group"]),
                str(row["email"]),
                int(row["age"]),
                str(row["city"]),
                row["time"],
            )

            cursor.execute(insert_query, values)

        # Save changes to the database.
        connection.commit()

        logging.info(
            "Successfully uploaded %d rows",
            len(data),
        )

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)

        if connection is not None:
            connection.rollback()

        raise

    finally:
        # Always close database resources.
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        logging.info("Database connection closed")


def main():
    """Run the full read, clean, and upload pipeline."""
    logging.info("Starting data pipeline")

    data = read_data("MOCK_DATA.csv")

    cleaned_data = clean_data(data)

    load_data(cleaned_data, "mock")

    logging.info("Pipeline finished")


if __name__ == "__main__":
    main()