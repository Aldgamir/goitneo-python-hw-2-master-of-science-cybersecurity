from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone():
            raise ValueError("Invalid phone number format")

    def validate_phone(self):
        return len(str(self.value)) <= 12 and str(self.value).isdigit()    # Number of digits are increased uo to 12
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, name, *phones):
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        self.data[name] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def search_record(self, name):
        if name in self.data:
            return str(self.data[name])
        else:
            return f"{name} not found in contacts."

    def add_phone_to_record(self, name, phone):
        if name in self.data:
            self.data[name].add_phone(phone)

    def delete_phone_from_record(self, name, phone):
        if name in self.data:
            self.data[name].delete_phone(phone)

    def edit_phone_in_record(self, name, old_phone, new_phone):
        if name in self.data:
            self.data[name].edit_phone(old_phone, new_phone)

    def find_record_by_phone(self, phone):
        for record in self.data.values():
            if record.find_phone(phone):
                return record
        return None

    def __str__(self):
        if self.data:
            return "\n".join(str(record) for record in self.data.values())
        else:
            return "No contacts found."

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
def add_contact(args, address_book):
    name = args[0]
    phones = args[1:]
    address_book.add_record(name, *phones)
    return f"Contact '{name}' added."

@input_error
def remove_contact(args, address_book):
    name = args[0]
    address_book.delete_record(name)
    return f"Contact '{name}' removed."

@input_error
def change_contact(args, address_book):
    if len(args) != 3:                                    # Функція запросить імʼя, старий телефон і новий телефон (три аргументи)
        raise ValueError("Invalid command format. Please use: change [name] [old phone number] [new phone number]")
    name, old_phone, new_phone = args
    address_book.edit_phone_in_record(name, old_phone, new_phone)
    return f"Phone '{old_phone}' edited to '{new_phone}' for contact '{name}'."

@input_error
def search_contact(args, address_book):
    name = args[0]
    return address_book.search_record(name)

@input_error
def show_phone(args, address_book):
    phone = args[0]
    record = address_book.find_record_by_phone(phone)
    if record:
        return str(record)
    else:
        return f"No contact found for phone '{phone}'."

@input_error
def show_all(address_book):
    return str(address_book)

def parse_input(user_input):
    cmd, *args = user_input.split(maxsplit=1)
    cmd = cmd.strip().lower()
    if args:
        if cmd in ["phone", "delete"]:
            if len(args[0].split()) != 1:  # Команди, зо мають працювати лише з одним аргументом
                raise ValueError(f"Invalid command format for '{cmd}'. Please check the input.")
            return cmd, [args[0]]
        elif len(args[0].split()) < 2:  # Усі інші команди працюють з двома аргументами
            raise ValueError(f"Invalid command format for '{cmd}'. Please check the input.")
        return cmd, args[0].split()
    else:
        return cmd, []

def main():
    print("Welcome to the assistant bot!")
    address_book = AddressBook()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "end", "finish", "bye"]:
            print("Good bye!")
            break

        elif command == "hello" or command == "hi":
            print("How can I help you?")

        elif command == "add" or command == "new" or command == "create":
            print(add_contact(*args, address_book))

        elif command == "remove" or command == "delete":
            print(remove_contact(*args, address_book))

        elif command == "change" or command == "update":
            print(change_contact(*args, address_book))

        elif command == "phone" or command == "contact" or command == "search":
            print(search_contact(*args, address_book))

        elif command == "all":
            print(show_all(address_book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
