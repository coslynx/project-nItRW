import sqlite3
from typing import Union, Tuple

class Database:
    """Represents the database connection and handles database operations."""

    def __init__(self, db_path: str):
        """
        Initializes the Database instance with the database path.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    discord_id BIGINT UNIQUE NOT NULL
                )
                """
            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS guilds (
                    id INTEGER PRIMARY KEY,
                    discord_id BIGINT UNIQUE NOT NULL
                )
                """
            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS blacklist (
                    id INTEGER PRIMARY KEY,
                    discord_id BIGINT UNIQUE NOT NULL
                )
                """
            )
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS whitelist (
                    id INTEGER PRIMARY KEY,
                    discord_id BIGINT UNIQUE NOT NULL
                )
                """
            )
            self.connection.commit()
        except Exception as e:
            raise DatabaseError(f"Error connecting to database: {e}")

    def disconnect(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def add_user(self, discord_id: int) -> bool:
        """
        Adds a new user to the database.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was added successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "INSERT INTO users (discord_id) VALUES (?)", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error adding user: {e}")

    def get_user(self, discord_id: int) -> Union[Tuple[int, int], None]:
        """
        Retrieves a user from the database.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            A tuple containing the user's ID and Discord ID if found, None otherwise.
        """
        try:
            cursor = self.connection.execute(
                "SELECT id, discord_id FROM users WHERE discord_id = ?", (discord_id,)
            )
            user = cursor.fetchone()
            return user
        except Exception as e:
            raise DatabaseError(f"Error getting user: {e}")

    def update_user(self, discord_id: int, **kwargs) -> bool:
        """
        Updates a user in the database.

        Args:
            discord_id: The Discord ID of the user.
            kwargs: A dictionary of key-value pairs to update.

        Returns:
            True if the user was updated successfully, False otherwise.
        """
        try:
            update_query = ", ".join(
                f"{key} = ?" for key in kwargs.keys()
            )
            query = f"UPDATE users SET {update_query} WHERE discord_id = ?"
            params = list(kwargs.values()) + [discord_id]
            self.connection.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error updating user: {e}")

    def delete_user(self, discord_id: int) -> bool:
        """
        Deletes a user from the database.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was deleted successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "DELETE FROM users WHERE discord_id = ?", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error deleting user: {e}")

    def add_guild(self, discord_id: int) -> bool:
        """
        Adds a new guild to the database.

        Args:
            discord_id: The Discord ID of the guild.

        Returns:
            True if the guild was added successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "INSERT INTO guilds (discord_id) VALUES (?)", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error adding guild: {e}")

    def get_guild(self, discord_id: int) -> Union[Tuple[int, int], None]:
        """
        Retrieves a guild from the database.

        Args:
            discord_id: The Discord ID of the guild.

        Returns:
            A tuple containing the guild's ID and Discord ID if found, None otherwise.
        """
        try:
            cursor = self.connection.execute(
                "SELECT id, discord_id FROM guilds WHERE discord_id = ?", (discord_id,)
            )
            guild = cursor.fetchone()
            return guild
        except Exception as e:
            raise DatabaseError(f"Error getting guild: {e}")

    def update_guild(self, discord_id: int, **kwargs) -> bool:
        """
        Updates a guild in the database.

        Args:
            discord_id: The Discord ID of the guild.
            kwargs: A dictionary of key-value pairs to update.

        Returns:
            True if the guild was updated successfully, False otherwise.
        """
        try:
            update_query = ", ".join(
                f"{key} = ?" for key in kwargs.keys()
            )
            query = f"UPDATE guilds SET {update_query} WHERE discord_id = ?"
            params = list(kwargs.values()) + [discord_id]
            self.connection.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error updating guild: {e}")

    def delete_guild(self, discord_id: int) -> bool:
        """
        Deletes a guild from the database.

        Args:
            discord_id: The Discord ID of the guild.

        Returns:
            True if the guild was deleted successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "DELETE FROM guilds WHERE discord_id = ?", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error deleting guild: {e}")

    def add_blacklist(self, discord_id: int) -> bool:
        """
        Adds a user to the blacklist.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was added successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "INSERT INTO blacklist (discord_id) VALUES (?)", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error adding user to blacklist: {e}")

    def get_blacklist(self) -> list:
        """
        Retrieves all blacklisted users.

        Returns:
            A list of blacklisted user Discord IDs.
        """
        try:
            cursor = self.connection.execute("SELECT discord_id FROM blacklist")
            blacklisted_users = [row[0] for row in cursor.fetchall()]
            return blacklisted_users
        except Exception as e:
            raise DatabaseError(f"Error getting blacklist: {e}")

    def remove_blacklist(self, discord_id: int) -> bool:
        """
        Removes a user from the blacklist.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was removed successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "DELETE FROM blacklist WHERE discord_id = ?", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error removing user from blacklist: {e}")

    def add_whitelist(self, discord_id: int) -> bool:
        """
        Adds a user to the whitelist.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was added successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "INSERT INTO whitelist (discord_id) VALUES (?)", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error adding user to whitelist: {e}")

    def get_whitelist(self) -> list:
        """
        Retrieves all whitelisted users.

        Returns:
            A list of whitelisted user Discord IDs.
        """
        try:
            cursor = self.connection.execute("SELECT discord_id FROM whitelist")
            whitelisted_users = [row[0] for row in cursor.fetchall()]
            return whitelisted_users
        except Exception as e:
            raise DatabaseError(f"Error getting whitelist: {e}")

    def remove_whitelist(self, discord_id: int) -> bool:
        """
        Removes a user from the whitelist.

        Args:
            discord_id: The Discord ID of the user.

        Returns:
            True if the user was removed successfully, False otherwise.
        """
        try:
            self.connection.execute(
                "DELETE FROM whitelist WHERE discord_id = ?", (discord_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Error removing user from whitelist: {e}")

class DatabaseError(Exception):
    """Custom exception class for database errors."""
    pass