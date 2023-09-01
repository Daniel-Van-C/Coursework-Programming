# shopping.py: Main classes used in Activity 1.
#
# Written by Daniel Van Cuylenburg
# 7CCSMCMP
#

# Imports.
# The Python Standard Library.
from json import dumps
from pprint import pprint
from datetime import datetime


class Product:
    """Class that represents a supermarket product.
    
    Attributes:
        name (string): Name of the product.
        price (float): Price of the product.
        quantity (integer): Quantity of the product.
        id (13-digit integer): EAN code for the product.
        brand (string): Brand of the product.
    """

    def __init__(self, name, price, quantity, id, brand):
        """Inits Product class with its attributes."""
        self.name = name
        self.price = price
        self.quantity = quantity
        self.id = id
        self.brand = brand

    def to_json(self):
        """Returns json representation of objects attributes."""
        return dumps(self.__dict__)

    def return_attributes(self):
        """Returns attributes of products as a dictionary."""
        return self.__dict__

    def get_id(self):
        """Returns ID (EAN code) of product."""
        return self.id

    def get_name(self):
        """Returns name of product."""
        return self.name

    def set_quantity(self, quantity):
        """Sets the quantity of the product."""
        self.quantity = quantity


class Clothing(Product):
    """Class that represents a clothing product. 
    
    Attributes:
        name (string): Name of the product.
        price (float): Price of the product.
        quantity (integer): Quantity of the product.
        id (13-digit integer): EAN code for the product.
        brand (string): Brand of the product.
        size (string): Size of the product.
        material (string): Material of the product.
    """

    def __init__(self, name, price, quantity, id, brand, size, material):
        """Inits Clothing class with its attributes."""
        super().__init__(name, price, quantity, id, brand)
        self.size = size
        self.material = material


class Food(Product):
    """Class that represents a food product.
    
    Attributes:
        name (string): Name of the product.
        price (float): Price of the product.
        quantity (integer): Quantity of the product.
        id (13-digit integer): EAN code for the product.
        brand (string): Brand of the product.
        expiry_date (string) Expiry date of the product.
        gluten_free (string): Whether the product is gluten free; 'y' for Yes, 'n' for no.
        suitable_for_vegetarians (string) Whether the product is suitable for vegetarians
            'y' for Yes, 'n' for no.
    """

    def __init__(self, name, price, quantity, id, brand, expiry_date,
                 gluten_free, suitable_for_vegetarians):
        """Inits Food class with its attributes."""
        super().__init__(name, price, quantity, id, brand)
        self.expiry_date = expiry_date
        self.gluten_free = gluten_free
        self.suitable_for_vegetarians = suitable_for_vegetarians


class Medicine(Product):
    """Class that represents a medicine product.
    
    Attributes:
        name (string): Name of the product.
        price (float): Price of the product.
        quantity (integer): Quantity of the product.
        id (13-digit integer): EAN code for the product.
        brand (string): Brand of the product.
        expiry_date (string) Expiry date of the product.
        tablet_or_capsule (string): Whether the medicine is in tablet or capsule form;
            't' for tablet, 'c' for capsule.
        size (string): Size of the product (the tablets).
    """

    def __init__(self, name, price, quantity, id, brand, expiry_date,
                 tablet_or_capsule, size):
        """Inits Medicine class with its attributes."""
        super().__init__(name, price, quantity, id, brand)
        self.expiry_date = expiry_date
        self.tablet_or_capsule = tablet_or_capsule
        self.size = size


class ShoppingCart:
    """Class that represents a shopping cart.
    
    Attributes:
        contents (list): What is currently inside the shopping cart.
    """

    def __init__(self):
        """Inits ShoppingCart class."""
        self.__contents = []

    def addProduct(self, p):
        """Add a product p to the shopping cart list."""
        if p != None:
            self.__contents.append(p)

    def removeProduct(self, p):
        """Removes a product p from the shopping cart list."""
        if p in self.__contents:
            self.__contents.remove(p)
            print("Product Successfully Removed")
        else:
            print("Product Not Found in Cart")

    def getContents(self):
        """Returns the contents of the shopping cart list.
        
        Returns:
            tuple : (The items name, the items attributes as a dictionary,
                and the item as an object.)
        """
        item_list = []
        for item in self.__contents:
            item_list.append((item.get_name(), item.return_attributes(), item))

        sorted_item_list = sorted(item_list, key=lambda x: x[0])
        return sorted_item_list

    def changeProductQuantity(self, p, q):
        """Changes products p quantity to q."""
        if p in self.__contents:
            p.set_quantity(q)
            print("Product's Quantity Successfully Changed")
        else:
            print("Product Not Found in Cart")


class Main():
    """Main class.
    
    Attributes:
        cart (ShoppingCart): Object that represents the shopping cart.
        ean_codes (list): List of EAN codes already in use,
            to make sure each new EAN code is unique.
    """

    def __init__(self):
        """Inits Main class, begins the main command line loop."""
        self.cart = ShoppingCart()
        self.ean_codes = []
        print("The program has started.")
        while True:
            c = input("Insert your next command (H for help): ")
            self.execute_command(c)
            if c == "T":
                break  # If the user wants to terminate the program, break the loop.
        print("Goodbye.")

    def execute_command(self, c):
        """Executes a command based on the user's input c.
        
        Args:
            comment (str): A single comment from the dataset.
        """
        if c == "A":
            self.cart.addProduct(self.input_product())
        elif c == "R":
            # As the EAN codes are unique, we only need to ask the user
            # for the EAN code of the product to be removed.
            while True:
                id = input(
                    "Insert its EAN code (must be a 13 digit sequence): ")
                try:  # While loop with try statement forces the user to enter an integer.
                    id = int(id)
                    if len(str(
                            id)) == 13:  # If the EAN code is 13 digits long.
                        self.ean_codes.append(str(id))
                        break
                except:
                    pass
            # Loops through all items in the cart removing the correct one.
            for item in self.cart.getContents():
                current_item_id = item[1]["id"]
                if current_item_id == id:
                    self.cart.removeProduct(item[2])
                    self.ean_codes.remove(str(current_item_id))
        elif c == "S":
            print("This is the total of the expenses: ")
            counter = 0
            total = 0
            # For each item in the cart, print its details,
            # summing the total cost to print at the end.
            for item in self.cart.getContents():
                current_item = item[1:2][0]
                counter += 1
                partial_sum = int(current_item["quantity"]) * int(
                    current_item["price"])
                total += partial_sum
                print("  ", counter, "-", current_item["quantity"], "*",
                      current_item["price"], "=", partial_sum)
            print("  Total =", total)
        elif c == "Q":
            while True:
                id = input(
                    "Insert its EAN code (must be a 13 digit sequence): ")
                try:  # While loop with try statement forces the user to enter an integer.
                    id = int(id)
                    if len(str(
                            id)) == 13:  # If the EAN code is 13 digits long.
                        self.ean_codes.append(str(id))
                        break
                except:
                    pass
            # Loops through all items in the cart until the correct one is found;
            # it's quantity is changed.
            for item in self.cart.getContents():
                current_item_id = item[1]["id"]
                if current_item_id == id:
                    while True:
                        try:  # While loop with try statement forces the user to enter an integer.
                            new_quantity = int(
                                input("Enter quantity (must be an integer)"))
                            break
                        except:
                            pass
                    item[2].set_quantity(new_quantity)
        elif c == "E":
            for item in self.cart.getContents():
                print(item[2].to_json())
        elif c == "T":
            pass
        elif c == "H":
            print("The program supports the following commands:")
            print("   [A] - Add a new product to the cart")
            print("   [R] - Remove a product from the cart")
            print("   [S] - Print a summary of the cart")
            print("   [Q] - Change the quantity of a product")
            print("   [E] - Export a JSON version of the cart")
            print("   [T] - Terminate the program")
            print("   [H] - List the supported commands")
        else:
            print("Command not recognised. Please try again")

    def input_product(self):
        """Query's the user about the attributes of a product they need to enter.
        Returns this product.
        
        Returns:
            Product or None: Either a Clothing, Food, Medicine object, or None.
        """
        # Each while statement checks one of the user inputs
        # to see if it matches the appropriate data type.
        while True:
            type = input(
                "Insert its type (must be 'Clothing', 'Food', or 'Medicine'): "
            )
            if isinstance(type, str): break
        while True:
            name = input("Insert its name (must be a string): ")
            if isinstance(name, str): break
        while True:
            price = input("Insert its price (must be a float): ")
            try:
                price = float(price)
                break
            except:
                pass
        while True:
            quantity = input("Insert its quantity (must be an integer): ")
            try:
                quantity = int(quantity)
                break
            except:
                pass
        while True:
            id = input(
                "Insert its EAN code (must be a unique 13 digit sequence): ")
            try:
                id = int(id)
                if len(str(id)) == 13:
                    if str(id) not in self.ean_codes:
                        self.ean_codes.append(str(id))
                        break
                    else:
                        print("EAN code already added. Enter a UNIQUE code.")
            except:
                pass
        while True:
            brand = input("Insert its brand: ")
            if isinstance(brand, str): break

        if type == "Clothing":
            while True:
                size = input("Insert its size (must be a string): ")
                if isinstance(type, str): break
            while True:
                material = input("Insert its material (must be a string): ")
                if isinstance(type, str): break
            return Clothing(name, price, quantity, id, brand, size, material)

        elif type == "Food":
            while True:
                expiry_date = input(
                    "Insert its expiry_date (format: \"YYYY-DD-MM\"): ")
                try:
                    expiry_date = str(
                        datetime(int(expiry_date[0:4]), int(expiry_date[5:7]),
                                 int(expiry_date[8:10])))
                    break
                except:
                    pass
            while True:
                gluten_free = input(
                    "Is this product gluten free? Insert 'y' for yes or 'n' for no: "
                )
                if gluten_free == "y" or gluten_free == "n":
                    break
            while True:
                suitable_for_vegetarians = input(
                    "Is this product suitable for vegetarians? Insert 'y' for yes or 'n' for no: "
                )
                if suitable_for_vegetarians == "y" or suitable_for_vegetarians == "n":
                    break
            return Food(name, price, quantity, id, brand, expiry_date,
                        gluten_free, suitable_for_vegetarians)

        elif type == "Medicine":
            while True:
                expiry_date = input(
                    "Insert its expiry_date (format: \"YYYY-MM-DD)\": ")
                try:
                    expiry_date = str(
                        datetime(int(expiry_date[0:4]), int(expiry_date[5:7]),
                                 int(expiry_date[8:10])))
                    break
                except:
                    pass
            while True:
                tablet_or_capsule = input(
                    "Insert 't' for tablet or 'c' for capsule: ")
                if tablet_or_capsule == "t" or tablet_or_capsule == "c":
                    break
            while True:
                size = input("Insert its size (must be a string): ")
                if isinstance(type, str): break
            return Medicine(name, price, quantity, id, brand, expiry_date,
                            tablet_or_capsule, size)

        else:
            print("Type of product not found")
            return None


if __name__ == "__main__":
    Main()
