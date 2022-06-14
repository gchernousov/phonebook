import csv
import re


def open_phonebook():
  with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    return contacts_list


def edit_name(full_name):
  """Функция для правки ФИО"""
  full_name_list = full_name.split()
  lastname = full_name_list[0]
  firstname = full_name_list[1]
  surname = ""
  if len(full_name_list) > 2:
    surname = full_name_list[2]

  return lastname, firstname, surname


def edit_phone_number(phone_number_old):
  """Функция для правки номера телефона"""
  phone_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?(-|\s)*(\d{3})(-|\s)*(\d{2})(-|\s)*(\d{2})"
  change_to = r"+7(\2)\4-\6-\8"
  phone_number_new = re.sub(phone_pattern, change_to, phone_number_old)

  if "доб" in phone_number_new:
    phone_pattern = r"(\+7\(\d+\)\d+-\d+-\d+)\s*\(?\w+.?\s*(\d+)\)?"
    change_to = r"\1 доб.\2"
    phone_number_new = re.sub(phone_pattern, change_to, phone_number_new)

  return phone_number_new


def edit_info(phonebook):
  """Функция для формирования новой телефонной книги
  с исправленным ФИО и номером телефона"""

  new_contact_list = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]

  for contact in phonebook[1:]:
    full_name = f"{contact[0]} {contact[1]} {contact[2]}"
    new_name_list = edit_name(full_name)

    lastname = new_name_list[0]
    firstname = new_name_list[1]
    surname = new_name_list[2]
    organization = contact[3]
    position = contact[4]
    phone_number_old = contact[5]

    phone_number_new = edit_phone_number(phone_number_old)

    email = contact[6]

    new_contact = []

    new_contact.append(lastname)
    new_contact.append(firstname)
    new_contact.append(surname)
    new_contact.append(organization)
    new_contact.append(position)
    new_contact.append(phone_number_new)
    new_contact.append(email)

    new_contact_list.append(new_contact)

  print("Телефонная книжка обновлена")
  return new_contact_list


def edit_double_record(new_contact_list):
  """Функция для корректировки контактов"""
  count = 1

  for control_record in new_contact_list[count:]:
    for check_row in new_contact_list[count + 1:]:
      if control_record[0] == check_row[0] and control_record[1] == check_row[1]:
        c = 2
        for n in range(5):
          n = n + c
          if control_record[n] != "" and check_row[n] == "":
            check_row[n] = control_record[n]
          elif control_record[n] == "" and check_row[n] != "":
            control_record[n] = check_row[n]

    count += 1

  return new_contact_list


def delete_double_record(contact_list):
  """Функция для удаления одинаковых строк"""

  count = 1

  for contact in contact_list[count:]:
    full_name_control = f"{contact[0]} {contact[1]} {contact[2]}"
    for check_row in contact_list[count + 1:]:
      full_name_check = f"{check_row[0]} {check_row[1]} {check_row[2]}"
      if full_name_control == full_name_check:
        contact_list.pop(count)
        count -= 1
    count += 1

  return contact_list


def save_phonebook(new_contact_list):
  with open("phonebook.csv", "w", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contact_list)
    print("Телефонная книжка сохранена")


if __name__ == "__main__":

  contacts_list = open_phonebook()
  new_contact_list = edit_info(contacts_list)
  new_contact_list = edit_double_record(new_contact_list)
  new_contact_list = delete_double_record(new_contact_list)
  save_phonebook(new_contact_list)