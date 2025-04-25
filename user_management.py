from pymongo import MongoClient
from datetime import datetime
import sys

# MongoDB connection
def connect_to_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['user_management_db']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

# Account management functions
def create_account(db):
    account_name = input("Enter account name: ")
    if db.accounts.find_one({"name": account_name}):
        print("Account already exists!")
        return
    
    account = {
        "name": account_name,
        "created_at": datetime.now(),
        "users": []
    }
    db.accounts.insert_one(account)
    print(f"Account '{account_name}' created successfully!")

def add_user_to_account(db):
    account_name = input("Enter account name: ")
    account = db.accounts.find_one({"name": account_name})
    if not account:
        print("Account not found!")
        return
    
    username = input("Enter username: ")
    email = input("Enter user email: ")
    
    if db.users.find_one({"username": username}):
        print("Username already exists!")
        return
    
    user = {
        "username": username,
        "email": email,
        "created_at": datetime.now(),
        "account_id": account["_id"],
        "groups": []
    }
    
    db.users.insert_one(user)
    db.accounts.update_one(
        {"_id": account["_id"]},
        {"$push": {"users": user["_id"]}}
    )
    print(f"User '{username}' added to account '{account_name}' successfully!")

def create_account_with_user(db):
    account_name = input("Enter new account name: ")
    if db.accounts.find_one({"name": account_name}):
        print("Account already exists!")
        return
    
    username = input("Enter username: ")
    email = input("Enter user email: ")
    
    if db.users.find_one({"username": username}):
        print("Username already exists!")
        return
    
    account = {
        "name": account_name,
        "created_at": datetime.now(),
        "users": []
    }
    
    account_id = db.accounts.insert_one(account).inserted_id
    
    user = {
        "username": username,
        "email": email,
        "created_at": datetime.now(),
        "account_id": account_id,
        "groups": []
    }
    
    user_id = db.users.insert_one(user).inserted_id
    db.accounts.update_one(
        {"_id": account_id},
        {"$push": {"users": user_id}}
    )
    print(f"Account '{account_name}' and user '{username}' created successfully!")

# Group management functions
def create_group(db):
    group_name = input("Enter group name: ")
    if db.groups.find_one({"name": group_name}):
        print("Group already exists!")
        return
    
    group = {
        "name": group_name,
        "created_at": datetime.now(),
        "users": []
    }
    db.groups.insert_one(group)
    print(f"Group '{group_name}' created successfully!")

def add_user_to_group(db):
    username = input("Enter username: ")
    user = db.users.find_one({"username": username})
    if not user:
        print("User not found!")
        return
    
    group_name = input("Enter group name: ")
    group = db.groups.find_one({"name": group_name})
    if not group:
        print("Group not found!")
        return
    
    if group["_id"] in user["groups"]:
        print(f"User '{username}' is already in group '{group_name}'!")
        return
    
    db.users.update_one(
        {"_id": user["_id"]},
        {"$push": {"groups": group["_id"]}}
    )
    db.groups.update_one(
        {"_id": group["_id"]},
        {"$push": {"users": user["_id"]}}
    )
    print(f"User '{username}' added to group '{group_name}' successfully!")

def display_menu():
    print("\n=== User Management System ===")
    print("1. Create new account")
    print("2. Add user to existing account")
    print("3. Create new account with user")
    print("4. Create new group")
    print("5. Add user to group")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def main():
    db = connect_to_mongodb()
    while True:
        choice = display_menu()
        if choice == "1":
            create_account(db)
        elif choice == "2":
            add_user_to_account(db)
        elif choice == "3":
            create_account_with_user(db)
        elif choice == "4":
            create_group(db)
        elif choice == "5":
            add_user_to_group(db)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()