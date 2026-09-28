"""Query the mock MySQL database for Lab 04."""

import logging
import os

import mysql.connector


# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def get_connection():
    """Create and return a connection to the MySQL database."""
    return mysql.connector.connect(
        host=os.environ["DBHOST"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"],
        database=os.environ["DBNAME"],
    )


def get_data_by_group(value):
    """Return rows where the `group` column equals the supplied value."""
    logging.info(
        "Finding rows where group equals %s",
        value,
    )

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        # Parameterized query for the group value.
        query = """
        SELECT
            id,
            `group`,
            email,
            age,
            city,
            time
        FROM mock
        WHERE `group` = %s
        ORDER BY id
        """

        cursor.execute(query, (value,))

        rows = cursor.fetchall()

        logging.info(
            "Found %d matching rows",
            len(rows),
        )

        return rows

    except mysql.connector.Error as error:
        logging.error(
            "Database error: %s",
            error,
        )
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def plot_counts(groupby):
    """Return counts of records grouped by a selected column."""
    logging.info(
        "Counting rows grouped by %s",
        groupby,
    )

    # Only allow known column names.
    queries = {
        "group": """
            SELECT `group` AS value, COUNT(*) AS count
            FROM mock
            GROUP BY `group`
            ORDER BY count DESC
        """,
        "city": """
            SELECT city AS value, COUNT(*) AS count
            FROM mock
            GROUP BY city
            ORDER BY count DESC
        """,
        "age": """
            SELECT age AS value, COUNT(*) AS count
            FROM mock
            GROUP BY age
            ORDER BY count DESC
        """,
        "time": """
            SELECT time AS value, COUNT(*) AS count
            FROM mock
            GROUP BY time
            ORDER BY count DESC
        """,
    }

    if groupby not in queries:
        raise ValueError(
            "groupby must be group, city, age, or time"
        )

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(queries[groupby])

        counts = cursor.fetchall()

        logging.info(
            "Created %d grouped results",
            len(counts),
        )

        return counts

    except mysql.connector.Error as error:
        logging.error(
            "Database error: %s",
            error,
        )
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def main():
    """Demonstrate the database query functions."""
    group_1_rows = get_data_by_group("1")

    print("\nFirst five rows from group 1:")

    for row in group_1_rows[:5]:
        print(row)

    counts = plot_counts("group")

    print("\nNumber of rows in each group:")

    for row in counts:
        print(row)


if __name__ == "__main__":
    main()