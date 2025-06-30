from flask_pymongo import PyMongo

# literally just the start of a mongodb model file

def test_insert(mongo):
    """
    Function docs TBD

    Args:
        mongo: Flask-PyMongo instance

    Returns:
        None
    """
    
    # this creates a database if it doesn't exist,
    # otherwise it accesses the database
    test_database = mongo.db.test_database

    test_entries = [
        {"name": "harry", "workout": "workout 23", "time": 4215},
        {"name": "trican", "workout": "workout 2", "time": 3012},
        {"name": "trican2", "workout": "workout 2231", "time": 2512},
    ]

    # this inserts the rows into the database
    test_database.insert_many(test_entries)

def test_query(mongo):
    """
    Function docs TBD

    Args:
        mongo: Flask-PyMongo instance

    Returns:

    """
    
    # same as above
    test_database = mongo.db.test_database

    # returns all database entries 

    """
    SQL to NoSQL database translation

    SELECT name, time FROM test_database WHERE time > 3000
    ==
    {"time": {"$gt": 3000}},
    {"name": 1, "time": 1, "workout": 0}
    """
    retrieved_entries = test_database.find(
        {"time": {"$gt": 3000}},
        {"name": 1, "time": 1}
    )
    list_entries = list(retrieved_entries)
    return list_entries