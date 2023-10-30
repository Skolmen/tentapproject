from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
import secrets

Base = declarative_base()

class ApiKey(Base):
    __tablename__ = 'api_keys'

    PERMISSION_TYPES = ('read-only', 'read and write')
    KEY_STATUS = ('active', 'disabled')

    api_id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String(255), unique=True)
    status = Column(Enum(*KEY_STATUS))
    permissions = Column(Enum(*PERMISSION_TYPES))
    created_at = Column(DateTime, server_default=('CURRENT_TIMESTAMP'))

class ApiKeyManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def generate_api_key(self):
        return secrets.token_hex(32)

    def create_new_key(self, new_permission: str = ApiKey.PERMISSION_TYPES[0]):
        """
        Create a new API key with the specified permission.

        :param new_permission: The permission for the new API key (e.g., 'read-only', 'read and write').
        :return: The generated API key, or None if an invalid permission is provided.
        """
        # Ensure that the new_permission value is a valid enum value
        if new_permission not in ApiKey.PERMISSION_TYPES:
            return None  # Return None to indicate an invalid permission

        api_key = self.generate_api_key()
        status = ApiKey.KEY_STATUS[0]
        session = self.Session()
        api = ApiKey(api_key=api_key, status=status, permissions=new_permission)
        session.add(api)
        session.commit()
        session.close()
        return api_key

    def get_all_keys(self):
        session = self.Session()
        keys = session.query(ApiKey).all()
        session.close()
        return keys

    def edit_key_status(self, api_id: int, new_status: str = ApiKey.KEY_STATUS[0]):
        """
        Edit the status of an API key.

        :param api_id: The ID of the API key to edit.
        :param new_status: The new status for the API key (e.g., 'active' or 'disabled').
        :return: The updated API key, or None if an invalid status is provided.
        """
        # Ensure that the new_status value is a valid status value
        if new_status not in ApiKey.KEY_STATUS:
            return None  # Return None to indicate an invalid status

        session = self.Session()
        api = session.query(ApiKey).filter(ApiKey.api_id == api_id).first()
        if api:
            api.status = new_status
            session.commit()
        session.close()
        return api

    def edit_key_permissions(self, api_id: int, new_permission: str):
        """
        Edit the permissions of an API key.

        :param api_id: The ID of the API key to edit.
        :param new_permission: The new permission for the API key (e.g., 'read-only' or 'read and write').
        :return: The updated API key, or None if an invalid permission is provided.
        """
        # Ensure that the new_permission value is a valid enum value
        if new_permission not in ApiKey.PERMISSION_TYPES:
            return None  # Return None to indicate an invalid permission

        session = self.Session()
        api = session.query(ApiKey).filter(ApiKey.api_id == api_id).first()
        if api:
            api.permissions = new_permission
            session.commit()
        session.close()
        return api

    def close(self):
        self.engine.dispose()

class ApiKeyMenu:
    def __init__(self, api_key_manager):
        self.api_key_manager = api_key_manager

    def show_menu(self):
        while True:
            print("\nAPI Key Management Menu:")
            print("1. Create new key")
            print("2. Show keys")
            print("3. Edit status")
            print("4. Edit permissions")  # Add an option to edit permissions
            print("5. Exit")

            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "1":
                api_key = self.api_key_manager.create_new_key()
                print(f"API key generated and stored successfully:\n{api_key}")

            elif choice == "2":
                keys = self.api_key_manager.get_all_keys()
                if keys:
                    print("\nAPI Keys:")
                    for key in keys:
                        print(f"API ID: {key.api_id}, Key: {key.api_key}, Status: {key.status}, Permissions: {key.permissions}, Created At: {key.created_at}")
                else:
                    print("No keys found in the database.")

            elif choice == "3":
                api_id = input("Enter the API ID you want to edit: ")
                status_choice = input("Options:\n1. Activate\n2. Disable\n3. Go Back\nEnter your choice (1/2/3): ")
                if status_choice == "1":
                    result = self.api_key_manager.edit_key_status(api_id, "active")
                    if result:
                        print(f"API key with ID {api_id} has been activated.")
                    else:
                        print(f"API key with ID {api_id} not found in the database.")
                elif status_choice == "2":
                    result = self.api_key_manager.edit_key_status(api_id, "disabled")
                    if result:
                        print(f"API key with ID {api_id} has been disabled.")
                    else:
                        print(f"API key with ID {api_id} not found in the database.")
                elif status_choice == "3":
                    print("No changes made. Going back to the main menu.")
                else:
                    print("Invalid choice. No changes made.")

            elif choice == "4":
                api_id = input("Enter the API ID you want to edit permissions for: ")
                permission_choice = input("Options:\n1. Set read-only\n2. Set read and write\n3. Go Back\nEnter your choice (1/2/3): ")
                if permission_choice == "1":
                    result = self.api_key_manager.edit_key_permissions(api_id, "read-only")
                    if result:
                        print(f"API key with ID {api_id} has been set to 'read-only'.")
                    else:
                        print(f"API key with ID {api_id} not found in the database.")
                elif permission_choice == "2":
                    result = self.api_key_manager.edit_key_permissions(api_id, "read and write")
                    if result:
                        print(f"API key with ID {api_id} has been set to 'read and write'.")
                    else:
                        print(f"API key with ID {api_id} not found in the database.")
                elif permission_choice == "3":
                    print("No changes made. Going back to the main menu.")
                else:
                    print("Invalid choice. No changes made.")

            elif choice == "5":
                self.api_key_manager.close()
                print("Exiting the API Key Management Program.")
                break

            else:
                print("Invalid choice. Please select a valid option (1/2/3/4/5).")

if __name__ == "__main__":
    db_url = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    api_key_manager = ApiKeyManager(db_url)
    menu = ApiKeyMenu(api_key_manager)
    menu.show_menu()