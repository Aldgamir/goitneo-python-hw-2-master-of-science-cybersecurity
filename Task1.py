def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format. Please check the input."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Invalid command format. Please use: add [name] [phone number]")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def search_contact(args, contacts):
    name = args[0]
    if name in contacts:
        return f"Phone number for {name}: {contacts[name]}"
    else:
        return f"{name} not found in contacts."

@input_error
def delete_contact(args, contacts):
    name = args[0]
    if name in contacts:
        del contacts[name]
        return f"{name} deleted from contacts."
    else:
        return f"{name} not found in contacts."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Invalid command format. Please use: change [name] [new phone number]")
    name, new_phone_number = args
    if name in contacts:
        contacts[name] = new_phone_number
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."

@input_error
def show_all(contacts):
    if contacts:
        return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    else:
        return "No contacts found."

@input_error
def remove_contact(args, contacts):
    name = args[0]
    if name in contacts:
        del contacts[name]
        return "Contact removed."
    else:
        return "Contact not found."

def parse_input(user_input):                          
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def main():
    print("Welcome to the assistant bot!")
    contacts = {}
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "end", "finish", "bye"]:
            print("Good bye!")
            break

        elif command == "hello" or command == "hi":
            print("How can I help you?")

        elif command == "add" or command == "new" or command == "create":
            print(add_contact(*args, contacts))

        elif command == "remove" or command == "delete":
            print(remove_contact(*args, contacts))

        elif command == "change" or command == "update":
            print(change_contact(*args, contacts))

        elif command == "phone" or command == "contact" or command == "search":
            print(show_phone(*args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
