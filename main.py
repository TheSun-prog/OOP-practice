import sys
import database


class User:
    def __init__(self):
        self.isMember = False
        self.isAdmin = False
        self.customerStep = 0
        self.adminStep = 0
        self.itemsList = database.getInfo()
        self.cart = []

    def authorization(self):
        authorization = input("Select the user's level\n"
                              "1 - Customer\n"
                              "2 - Member\n"
                              "3 - Admin\n")

        while True:
            if authorization in ['1', '2', '3']:
                break

            authorization = input("Select the user's level\n"
                                  "1 - Customer\n"
                                  "2 - Member\n"
                                  "3 - Admin\n")

        match authorization:
            case '1':
                self.isMember = False
                self.isAdmin = False
            case '2':
                self.isMember = True
                self.isAdmin = False
            case '3':
                self.isMember = False
                self.isAdmin = True

    # User Interface
    def customerMenu(self):
        self.customerStep = input("\nCustomer Menu:\n\n"
                                  "0 - Main Menu\n"
                                  "1 - Authorization\n"
                                  "2 - Items List\n"
                                  "3 - Add Item into Cart\n"
                                  "4 - Check Cart\n"
                                  "5 - Clear Cart\n"
                                  "6 - Buy Items in the Cart\n"
                                  "7 - Search item\n"
                                  "8 - Admin Menu\n"
                                  "9 - Exit\n\n")
        self.nextCustomerStep()

    def nextCustomerStep(self):
        match self.customerStep:
            case '0':
                self.customerMenu()
            case '1':
                self.authorization()
            case '2':
                self.getItemsList()
            case '3':
                self.addItemToCart()
            case '4':
                self.checkCart()
            case '5':
                self.clearCart()
            case '6':
                self.buyItems()
            case '7':
                self.searchItem()
            case '8':
                self.adminMenu()
            case '9':
                self.saveData()
                sys.exit()
            case _:
                print("Error")
                self.customerMenu()

        if self.customerStep != '8':
            self.customerMenu()

    def adminMenu(self):
        if self.isAdmin:
            self.adminStep = input("\nAdmin menu\n\n"
                                   "0 - Main Menu\n"
                                   "1 - Add New Item\n"
                                   "2 - Items List\n"
                                   "3 - Edit Item\n"
                                   "4 - Delete Item\n"
                                   "9 - Exit\n\n")
            self.nextAdminStep()
        else:
            print('You have no permission')
            self.customerMenu()

    def nextAdminStep(self):
        match self.adminStep:
            case '0':
                self.customerMenu()
            case '1':
                self.addNewItem()
            case '2':
                self.getItemsList()
            case '3':
                self.editItem()
            case '4':
                self.deleteItem()
            case '9':
                self.saveData()
                sys.exit()
            case _:
                self.adminMenu()

        if self.adminStep != '0':
            self.adminMenu()

    # Admin Functions

    def editItem(self):
        editingItemName = input("Editing item's name\n").lower()
        if editingItemName not in self.itemsList.keys():
            print("There is no item with this name\n")
            return
        editingColumn = input("Edit what thing\n"
                              "1 - Category\n"
                              "2 - Perishable\n"
                              "3 - Stock\n"
                              "4 - Price\n\n")
        while editingColumn not in ['1', '2', '3', '4']:
            editingColumn = input("Edit what thing\n"
                                  "1 - Category\n"
                                  "2 - Perishable\n"
                                  "3 - Stock\n"
                                  "4 - Price\n\n")
        match editingColumn:
            case '1':
                editingColumn = 'category'
            case '2':
                editingColumn = 'perishable'
            case '3':
                editingColumn = 'stock'
            case '4':
                editingColumn = 'price'

        editingData = input(f"Editing data for {editingColumn}:\n")
        if editingColumn in ['stock', 'price']:
            while True:
                try:
                    editingData = int(editingData)
                    break
                except:
                    print('Error')
                    editingData = int(input(f"Editing data for {editingColumn}:\n"))
        if editingColumn in ['perishable']:
            while True:
                try:
                    editingData = bool(editingData)
                    break
                except:
                    print('Error')
                    editingData = bool(input(f"Editing data for {editingColumn}:\n"))

        database.editRow(editingItemName, editingColumn, editingData)
        self.updateItemsList()

    def deleteItem(self):
        deletingItemName = input("Deleting item's name\n")
        if deletingItemName not in self.itemsList.keys():
            print("There is no item with this name\n")
            return
        database.deleteRow(deletingItemName)
        self.updateItemsList()

    def addNewItem(self):
        # Name, Category, Perishable, Stock, Price

        name = input("Item's Name\nMilk\n")

        category = input("Item's Category\nFood\n")

        perishable = input("Item's Perishable\nTrue/False or +/- or 0/1\n")
        match perishable.lower():
            case '0':
                perishable = False
            case '-':
                perishable = False
            case 'false':
                perishable = False
            case '1':
                perishable = True
            case '+':
                perishable = True
            case 'true':
                perishable = True

        while True:
            if type(perishable) != bool:
                print('Error')
                perishable = input("Item's Perishable\nTrue/False or +/- or 1/0\n")
                match perishable.lower():
                    case '0':
                        perishable = False
                    case '-':
                        perishable = False
                    case 'false':
                        perishable = False
                    case '1':
                        perishable = True
                    case '+':
                        perishable = True
                    case 'true':
                        perishable = True
            else:
                break

        stock = input("Item's Stock\n8\n")
        while True:
            try:
                stock = int(stock)
                break
            except:
                print('Error')
                stock = int(input("Item's Stock\n8\n"))

        price = input("Item's Price in euro\n5\n")
        while True:
            try:
                price = int(price)
                break
            except:
                print('Error')
                price = input("Item's Stock\n8\n")

        newItemData = [name,
                       category,
                       perishable,
                       stock,
                       price]
        database.insertNewInfo(newItemData)
        self.updateItemsList()
        self.adminMenu()

    def saveData(self):
        itemNames = self.itemsList.keys()
        database.clearTable()
        singleData = []
        for name in itemNames:
            singleData.append(name)
            singleData.append(self.itemsList[name]['category'])
            singleData.append(self.itemsList[name]['perishable'])
            singleData.append(self.itemsList[name]['stock'])
            singleData.append(self.itemsList[name]['price'])
            database.insertNewInfo(singleData)
            singleData = []

    def updateItemsList(self):
        self.itemsList = database.getInfo()

    # Customer functions
    def addItemToCart(self):
        selectedItemName = input("Enter the item's name for cart\n").lower()
        if selectedItemName not in self.itemsList.keys():
            print("There is no item with this name")
            return
        buyCount = input("How much you wanna buy\n")
        while True:
            try:
                buyCount = int(buyCount)
                break
            except:
                print("Error")
                buyCount = input("How much you wanna buy\n")
        if buyCount > self.itemsList[selectedItemName]['stock']:
            print("There is no more this item")
            return

        status = 1

        for item in self.cart:
            if item[0] != selectedItemName:
                continue

            newBuyCount = buyCount + item[1]
            if newBuyCount > self.itemsList[selectedItemName]['stock']:
                print("There is no more this item")
                return

            newItem = [item[0], newBuyCount]

            self.cart.pop(item)
            self.cart.append(newItem)
            status = 0
            break

        if status:
            self.cart.append([selectedItemName, buyCount])

    def clearCart(self):
        self.cart = []

    def checkCart(self):
        totalPrice = 0
        receipt = 'Checking cart\n'

        for item in self.cart:
            itemName = item[0]
            itemPrice = self.itemsList[itemName]['price']
            itemCount = item[1]

            receipt += f"Name: {itemName} | Price: {itemPrice}€ | Quantity: {itemCount}\n"
            totalPrice += itemPrice * itemCount

        if self.isMember:
            if totalPrice > 50:
                discount = totalPrice / 100 * 10
                totalPrice -= discount
            else:
                discount = totalPrice / 100 * 5
                totalPrice -= discount

            receipt += f"Your discount: {discount}€\n"

        receipt += f"Total: {totalPrice}€"
        print(receipt)

    def buyItems(self):
        if not self.cart:
            print("Your cart is empty")
            return

        receipt = 'Receipt for transaction\n'
        totalPrice = 0

        for item in self.cart:
            itemName = item[0]
            itemCount = item[1]
            itemPrice = self.itemsList[itemName]['price']

            self.itemsList[itemName]['stock'] -= itemCount

            receipt += f"Name: {itemName} | Price: {itemPrice}€ | Quantity: {itemCount}\n"
            totalPrice += itemPrice * itemCount

        if self.isMember:
            if totalPrice > 50:
                discount = totalPrice / 100 * 10
                totalPrice -= discount
            else:
                discount = totalPrice / 100 * 5
                totalPrice -= discount

            receipt += f"Your discount: {discount}€\n"

        self.saveData()
        self.clearCart()
        receipt += f"Total: {totalPrice}€"
        print(receipt)

    def getItemsList(self):
        print('\n')
        for name in self.itemsList.keys():
            category = self.itemsList[name]["category"]
            perishable = self.itemsList[name]["perishable"]
            stock = self.itemsList[name]["stock"]
            price = self.itemsList[name]["price"]
            print(f'Name: {name} | Category: {category} | Perishable: {perishable} | Stock: {stock} | Price: {price}€')
        print('\n')

    def searchItem(self):
        filterType = input("Select item type\n"
                           "1 - Name\n"
                           "2 - Categories\n"
                           "3 - Perishable\n"
                           "4 - Price\n")
        while True:
            if filterType in ['1', '2', '3', '4']:
                break
            filterType = input("Select item type\n"
                               "1 - Name\n"
                               "2 - Category\n")
        filterList = {
            'names': [],
            'categories': [],
            'perishable': [],
            'price': [],
        }
        for itemName in self.itemsList.keys():
            itemCategory = self.itemsList[itemName]['category']
            itemPerishable = self.itemsList[itemName]['perishable']
            itemPrice = self.itemsList[itemName]['price']
            filterList['names'].append(itemName)
            filterList['categories'].append(itemCategory)
            filterList['perishable'].append(itemPerishable)
            filterList['price'].append(itemPrice)

        match filterType:
            case '1':
                filterType = 'names'
            case '2':
                filterType = 'categories'
            case '3':
                filterType = 'perishable'
            case '4':
                filterType = 'price'

        filterWord = input("Enter the filter\n")

        index = 0

        for element in filterList[filterType]:
            if filterWord.lower() == str(element).lower():

                itemName = filterList['names'][index]
                filterItem = self.itemsList[itemName]
                itemCategory = filterItem["category"]
                itemPerishable = filterItem["perishable"]
                itemStock = filterItem["stock"]
                itemPrice = filterItem["price"]

                print(f'Name: {itemName} | Category: {itemCategory} | Perishable: {itemPerishable} | Stock: {itemStock} | Price: {itemPrice}€')

            index += 1


start = User()
start.customerMenu()
