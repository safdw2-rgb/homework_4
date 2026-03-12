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
        self.value = self.check_number(value)

    def check_number(self, number):
        try:
            if int(number) and len(number) == 10:
                return number
            else:
                raise ValueError("Enter correct number")
        except ValueError:
            raise ValueError("Enter correct number")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        try:
            phone = Phone(number)
            self.phones.append(phone)
        except Exception as e:
            print(e)

    def remove_phone(self, number):

        phone = self.find_phone(number)

        if phone:
            self.phones.remove(phone)
        else:
            print(f"Phone {number} not found")


    def edit_phone(self, old_number, new_number):
        try:
            found_phone = None
            for phone in self.phones:
                if phone.value == old_number:
                    found_phone = phone
                    break
            if found_phone:
                self.phones.remove(found_phone)
                self.phones.append(Phone(new_number))
                print(f"Phone {old_number} changed to {new_number}")
            else:
                print(f"Error: Phone {old_number} not found in contacts.")

        except Exception as e:
            print(e)

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
        return f"Contact {name} not found"

