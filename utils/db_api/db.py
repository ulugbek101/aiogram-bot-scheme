import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    def connect(self):
        return pymysql.Connection(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) -> dict | list:
        database = self.connect()
        cursor = database.cursor()

        cursor.execute(sql, params)
        data = None

        if fetchone:
            data = cursor.fetchone()

        elif fetchall:
            data = cursor.fetchall()

        if commit:
            database.commit()

        return data

    def create_users_table(self) -> None:
        """
        Creates users table
        :return: None
        """
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id INT NOT NULL UNIQUE,
                fullname VARCHAR(100),
                username VARCHAR(100)
            )
        """
        self.execute(sql)

    def create_categories_table(self) -> None:
        """
        Creates categories table
        :return: None
        """
        sql = """
            CREATE TABLE IF NOT EXISTS categories(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        """
        self.execute(sql)

    def create_products_table(self) -> None:
        """
        Creates products table
        :return: None
        """
        sql = """
            CREATE TABLE IF NOT EXISTS products(
                id INT PRIMARY KEY AUTO_INCREMENT,
                category_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255) NOT NULL,
                photo VARCHAR(255) NOT NULL,
                price DECIMAL(12, 2) NOT NULL
            )
        """
        self.execute(sql)

    def create_cart_table(self) -> None:
        """
        Creates cart table
        :return: None
        """
        sql = """
            CREATE TABLE IF NOT EXISTS cart(
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL
            );
        """
        self.execute(sql)

    def create_orders_history_table(self) -> None:
        """
        Creates orders history table
        :return: None
        """
        sql = """
            CREATE TABLE orders_history (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                total_price DECIMAL(12, 2),
                date DATE DEFAULT CURRENT_DATE,
                time TIME DEFAULT CURRENT_TIME
            );
        """
        self.execute(sql)

    def get_orders_history(self, user_id) -> list:
        """
        Returns all orders made by particular user
        :param user_id: user's id
        :return: list
        """
        sql = """
            SELECT * FROM orders_history 
            WHERE user_id = %s
        """
        self.execute(sql, (user_id,), fetchall=True)

    def get_categories(self) -> list:
        """
        Returns all categories from categories table
        :return: list
        """
        sql = """
            SELECT * FROM categories
        """
        return self.execute(sql, fetchall=True)

    def get_cart_products(self, user_id: int) -> list:
        """
        Returns user's all cart products
        :user_id: user's id
        :return: list
        """
        sql = """
            SELECT * FROM cart WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def update_cart_product_quantity(self, user_id: int, product_id: int, new_quantity: int) -> None:
        """
        Updates user's cart product's quantity
        :param user_id: user's id
        :param product_id: product's id
        :param new_quantity: product's new quantity
        :return: None
        """
        sql = """
            UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s
        """
        self.execute(sql, (new_quantity, user_id, product_id), commit=True)

    def delete_cart_product(self, order_id: int) -> None:
        """
        Deletes cart product from user's cart
        :param order_id: int
        :return: None
        """
        sql = """
            DELETE FROM cart WHERE id = %s
        """
        self.execute(sql, (order_id,), commit=True)

    def get_products(self, category_id: int) -> list:
        """
        Returns products from certain category
        :param category_id: category id
        :return: list
        """
        sql = "SELECT * FROM products WHERE category_id = %s"
        return self.execute(sql, (category_id,), fetchall=True)

    def get_product(self, product_id: int) -> dict:
        """
        Returns product by product id
        :param product_id: product's id
        :return: dict
        """
        sql = "SELECT * FROM products WHERE id = %s"
        return self.execute(sql, (product_id,), fetchone=True)

    def get_user(self, telegram_id: int) -> dict:
        """
        Returns user object from users table by telegram id
        :telegram_id: user's telegram id
        :return: dict
        """
        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def register_user(self, telegram_id: int, fullname: str, username: str) -> None:
        """
        Creates new user in users table
        :param telegram_id: user's telgram id
        :param fullname: user's fullname
        :param username: user's username
        :return: None
        """
        sql = """
            INSERT INTO users (telegram_id, fullname, username)
            VALUES (%s, %s, %s)
        """
        self.execute(sql, (telegram_id, fullname, username), commit=True)

    def add_product_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        """
        Adds product to cart table for a specifidc user
        :user_id: user's id
        :product_id: product's is
        :quantity: product's quantity
        :return: None
        """
        sql = """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """
        self.execute(sql, (user_id, product_id, quantity), commit=True)

    def add_to_orders_history(self, user_id: int, product_id: int,
                              quantity: int, total_price: float | int) -> None:
        """
        Adds product from user's cart to user's orders history
        :param user_id: user's id
        :param product_id: product's id
        :param quantity: product's quantity
        :param total_price: product's total price
        :return: None
        """
        sql = """
            INSERT INTO orders_history (user_id, product_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (user_id, product_id, quantity, total_price), commit=True)
