import sqlite3


# Decorator for connect to Database
def connectDB(func):
    def wrapper():
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        result = func(cursor)
        connect.commit()
        connect.close()
        return result

    return wrapper


# Function for create new table
# Values example ['price', 'catalog', 'name']
def createNewTable(name, values):
    newValues = []
    for valueName in values:
        newValues.append(f'{valueName} TEXT')

    newValues = ", ".join(newValues)

    @connectDB
    def createNewTableDB(cursor=None):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name}({newValues})
        """)

    createNewTableDB()


# Name, Category, Perishable, Stock, Price
def insertNewInfo(data):
    values = tuple(data)

    @connectDB
    def insertNewInfoDB(cursor=None):
        cursor.execute(f"""
            INSERT INTO items VALUES (?, ?, ?, ?, ?)
        """, values)

    insertNewInfoDB()


# Funtion for get items list
def getInfo():

    @connectDB
    def getTableInfoDB(cursor=None):
        cursor.execute(f"""
            SELECT * FROM items
        """)
        record = cursor.fetchall()
        return record

    data = getTableInfoDB()
    getTableInfoDB()
    values = {}
    if data:
        for element in data:
            values[element[0].lower()] = {
                'category': element[1],
                'perishable': bool(element[2]),
                'stock': int(element[3]),
                'price': int(element[4])
            }
    return values


# Function for clear the table
def clearTable():
    @connectDB
    def clearTableDB(cursor=None):
        cursor.execute("""
            DELETE FROM items
        """)

    clearTableDB()


# Function for delete the row
def deleteRow(itemName):
    @connectDB
    def deleteRowDB(cursor=None):
        cursor.execute(f"""
            DELETE FROM items WHERE name='{itemName}'
        """)
    deleteRowDB()


# Funtion for edit the row
def editRow(itemName, editingColumn, data):
    @connectDB
    def editRowDB(cursor=None):
        cursor.execute(f"""
            UPDATE items SET {editingColumn}='{data}' WHERE name='{itemName}'
        """)
    editRowDB()


# Creating new table for items
itemsValue = ['name', 'category', 'perishable', 'stock', 'price']
createNewTable('items', itemsValue)

