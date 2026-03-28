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
        valid_number = self.check_number(value)
        super().__init__(valid_number)

    def is_valid_number(self, number):
        return number.isdigit() and 10 <= len(number) <= 12

    def check_number(self, number):
        if self.is_valid_number(number):
            return number

        symbols_to_remove = ["+", "(", ")", "-", " "]

        for symbol in symbols_to_remove:
            number = number.strip().replace(symbol, "")

        if self.is_valid_number(number):
            return number
        else:
            raise ValueError("Enter correct number.")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        phone = Phone(number)
        self.phones.append(phone)

    def remove_phone(self, number):
        phone = self.find_phone(number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone {number} not found.")

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone:
            new_phone_obj = Phone(new_number)
            self.phones.remove(phone)
            self.phones.append(new_phone_obj)
        else:
            raise ValueError(f"Phone {old_number} not found in contacts.")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted."
        return f"Contact {name} not found."

    def rename(self, old_name, new_name):
        if old_name not in self.data:
            raise ValueError(f"Contact {old_name} doesn't exist.")
        if new_name in self.data:
            raise ValueError(f"Contact {new_name} already exists. Please choose another name.")

        record = self.data.pop(old_name)
        record.name = Name(new_name)
        self.data[new_name] = record

    def find_owner_by_phone(self, phone_number):
        for record in self.data.values():
            if record.find_phone(phone_number):
                return record.name.value
        return None

def input_error(func):
    def check_errors(*args):
        try:
            return func(*args)
        except IndexError:
            return "Error: Please provide all the information."
        except ValueError as e:
            return f"Error: {e}"
    return check_errors


class Operator:

    def __init__(self):
        self.contact_book = AddressBook()
        self.COMMANDS = {
            "hello": lambda _: "How can I help you?",
            "add": self.add_contact,
            "change": self.change_contact,
            "rename": self.rename_contact,
            "phone": self.show_phone_number,
            "search": self.find_by_phone_number,
            "show all": self.show_all_numbers,
            "delete": self.delete_contact,
            "remove": self.remove_phone_number,
            "info": self.show_info,
            "good bye": lambda _: "Good Bye!",
            "close": lambda _: "Good Bye!",
            "exit": lambda _: "Good Bye!"}
        self.error_messages = [
            "Please provide a contact name.",
            "Please provide all the info.",
            "Please provide name, old phone number, and new phone number."
        ]

    def empty_contact_book(self):
        if len(self.contact_book) == 0:
            return "Error: Contact book is empty."

    def main(self):
        print("Welcome to the helper bot! Enter 'info' to show available commands.")
        while True:
            user_input = input(">>> ").strip()
            if not user_input:
                print("Error: Please enter a command.")
                continue

            matched_command = None
            for key in self.COMMANDS.keys():
                if user_input.lower().startswith(key):
                    matched_command = key
                    break

            if matched_command:
                method = self.COMMANDS[matched_command]

                args_str = user_input[len(matched_command):].strip()
                args = args_str.split() if args_str else []

                result = method(args)
                print(result)

                if result == "Good Bye!":
                    break
            else:
                print("Error: Unknown command.")

    def show_info(self, args):
        return (
            "Available commands:\n"
            "-------------------\n"
            "hello                           - Greet the bot\n"
            "add [name] [phone]              - Add a new contact or phone\n"
            "change [name] [old] [new_phone] - Change an existing phone number\n"
            "rename [old_name] [new_name]    - Change a contact's name\n"
            "phone [name]                    - Show phones for a contact\n"
            "search [phone]                  - Find contact name by phone number\n"
            "show all                        - Show all contacts\n"
            "delete [name]                   - Delete a whole contact\n"
            "remove [name] [phone]           - Remove a specific phone\n"
            "info                            - Show this help message\n"
            "good bye, close, exit           - Exit the program"
        )

    def check_correct(self, args, error_messages, num_args):
        if len(args) < len(error_messages) and len(args) < num_args:
            raise ValueError(error_messages[len(args)])


    @input_error
    def add_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        name, phone = args[0], args[1]

        owner = self.contact_book.find_owner_by_phone(phone)
        if owner and owner != name:
            raise ValueError(f"Phone {phone} is already assigned to contact {owner}.")

        record = self.contact_book.find(name)

        if record:
            if record.find_phone(phone):
                raise ValueError(f"Contact {name} already has phone {phone}.")

            record.add_phone(phone)
            return f"Phone {phone} added to contact {name}."
        else:
            new_record = Record(name)
            new_record.add_phone(phone)
            self.contact_book.add_record(new_record)
            return f"Contact {name} added."

    @input_error
    def change_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        record = self.contact_book.find(name)

        if not record:
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 3)

        old_phone, new_phone = args[1], args[2]

        owner = self.contact_book.find_owner_by_phone(new_phone)
        if owner and owner != name:
            raise ValueError(f"Phone {new_phone} is already assigned to contact {owner}.")

        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} changed."

    @input_error
    def delete_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]

        return self.contact_book.delete(name)

    @input_error
    def rename_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        old_name, new_name = args[0], args[1]

        self.contact_book.rename(old_name, new_name)

        return f"Contact {old_name} successfully renamed to {new_name}."

    @input_error
    def remove_phone_number(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        result = self.contact_book.find(name)

        if not result:
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 2)

        phone = args[1]

        result.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."

    @input_error
    def show_phone_number(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]

        record = self.contact_book.find(name)
        if record:
            return str(record)
        else:
            return f"Error: Contact {name} doesn't exist."

    @input_error
    def find_by_phone_number(self, args):
        self.check_correct(args, self.error_messages, 1)

        phone = args[0]

        valid_phone = Phone(phone).value

        owner = self.contact_book.find_owner_by_phone(valid_phone)

        if owner:
            record = self.contact_book.find(owner)
            return str(record)
        else:
            return f"Phone {valid_phone} not found in contacts."

    def show_all_numbers(self, args):

        if not self.contact_book.data:
            return "Contact book is empty."

        result = []
        for record in self.contact_book.data.values():
            result.append(str(record))

        return "\n".join(result)


operator = Operator()
operator.main()