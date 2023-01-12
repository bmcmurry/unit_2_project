# ========= IMPORTS ============
import os
import pwinput  # type: ignore
import csv
from datetime import datetime, date
import time
from dataclasses import dataclass
from math import trunc
from termcolor import colored
from prettytable import PrettyTable
from dateutil import parser  # type: ignore

# ====================== DATACLASS ===============


@dataclass
class Users:
    User_Name: str
    Password: str
    Balance: float
    Per_Diem: float
    Amt_Students: int
    Last_Login: str
    Creation_Date: str
    Weekly_Add: float
    Amt_Gain: float
    Debit_Frequency: int


User = Users("", "", 0.00, 0.00, 0, "", "", 0, 0, 0)
# ================ TEXT VARIABLES ====================
# ========== SCREEN PRINT OUTS
menu = colored("MAIN MENU", "cyan", attrs=["bold", "underline"])
title = colored(
    "BCCA GI Procurement Tracker Thing by BLAP Industries",
    "cyan",
    attrs=["bold", "underline"],
)

# ========== PROMPTS
login = colored("[LOGIN]", "blue", attrs=["bold"])
create = colored("[CREATE]", "blue", attrs=["bold"])
students = colored("[STUDENTS]", "blue", attrs=["bold"])
perdiem = colored("[PERDIEM]", "blue", attrs=["bold"])
edit = colored("[EDIT]", "blue", attrs=["bold"])
view = colored("[VIEW]", "blue", attrs=["bold"])
add = colored("[ADD]", "blue", attrs=["bold"])
quit = colored("[QUIT]", "blue", attrs=["bold"])
enter = colored("[ENTER]", "blue", attrs=["bold"])
current = colored("[CURRENT]", "blue", attrs=["bold"])
past = colored("[PAST]", "blue", attrs=["bold"])
frequency = colored("[FREQUENCY]", "blue", attrs=["bold"])
yes = colored("[YES]", "blue", attrs=["bold"])
no = colored("[NO]", "blue", attrs=["bold"])
back = colored("[BACK]", "blue", attrs=["bold"])


# ============== INPUT VALIDATION ===============
# ========= LOGIN VALIDATION
def login_valid() -> str:
    while True:
        action = input(f"{login} or {create} a user? > ").lower().strip()
        if action in ("login", "create", "quit"):
            return action
        print(
            colored(
                f"\n{action} is not a valid option. Please choose a valid option.\n",
                "yellow",
                attrs=["bold"],
            )
        )


def existing_user_valid(USERS: dict) -> str:
    while True:
        if USERS == {}:
            print(
                colored(
                    "\nThere are currently no users saved.", "yellow", attrs=["bold"]
                )
            )
            return "quit"
        User.User_Name = input("\nUsername > ").strip()
        if User.User_Name in USERS.keys():
            while True:
                User.Password = pwinput.pwinput(prompt="Password > ").strip()
                if User.Password == USERS[User.User_Name][0]:
                    return User.User_Name
                elif User.Password.lower() == "quit":
                    return User.Password
                else:
                    print(
                        colored(
                            f"\n{User.Password} is not the password for {User.User_Name}\n",
                            "yellow",
                            attrs=["bold"],
                        )
                    )
        elif User.User_Name.lower() == "quit":
            return User.User_Name
        else:
            print(
                colored(
                    f"\n{User.User_Name} is not a existing user.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def create_user_valid(USERS: dict) -> str:
    while True:
        username = input("\nUsername > ").strip()
        if username not in USERS.keys():
            if "," not in username:
                return username
            else:
                print(
                    colored(
                        f"You cannot use a , in your username.",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        else:
            print(
                colored(
                    f"\n{username} has already been used. Pick a new username.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def perdiem_ask_valid() -> str:
    while True:
        print(f"Is that correct?")
        print(f"Enter {yes} to receive that amount of time periods of per diem.")
        action = (
            input(
                f"""Enter {no} to manually provide the number of times you should have recieved per diem. > """
            )
            .lower()
            .strip()
        )
        if action not in ("yes", "no"):
            print(
                colored(f"\n{action} is not a valid entry.\n", "yellow", attrs=["bold"])
            )
        else:
            return action


# ========= NUMBER VALIDATION
def valid_expense() -> float:
    while True:
        input_amt = input("Enter the amount of the purchase > ")
        try:
            float_input_amt = float(input_amt)
            if float_input_amt > 0:
                return float_input_amt
            elif float_input_amt <= 0:
                print(
                    colored(
                        f"\n{float_input_amt} is a negative value or zero. Your entry must be a positive number.\n",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        except ValueError:
            print(
                colored(
                    f"\n{input_amt} is not a valid number.\n", "yellow", attrs=["bold"]
                )
            )


def amt_Per_Diem() -> float:
    while True:
        amt_Per_Diem = input("Input per student per diem > ")
        try:
            float_per_diem = float(amt_Per_Diem)
            if float_per_diem > 0:
                return float_per_diem
            else:
                print(
                    colored(
                        f"\n{amt_Per_Diem} is a negative value or zero. Your entry must be a positive number.\n",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        except:
            print(
                colored(
                    f"\n{amt_Per_Diem} is not a valid number.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def valid_amt_students() -> int:
    while True:
        student_amt = input("How many students are in the class? > ")
        if student_amt.isdigit():
            int_stud_amt = int(student_amt)
            if int_stud_amt > 0:
                return int_stud_amt

            else:
                print(
                    colored(
                        f"\n{student_amt} is a negative value or zero. Your entry must be a positive number.\n",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        else:
            print(
                colored(
                    f"\n{student_amt} is not a valid number.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def valid_debit_frequency() -> int:
    while True:
        amt_days = input("How many days would you like between debits? > ")
        if amt_days.isdigit():
            int_amt_days = int(amt_days)
            if int_amt_days > 0:
                return int_amt_days

            else:
                print(
                    colored(
                        f"\n{amt_days} is a negative value or zero. Your entry must be a positive number.\n",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        else:
            print(
                colored(
                    f"\n{amt_days} is not a valid day amount.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def perdiem_manual_valid() -> int:
    while True:
        action = input("How many times should we add per diem? > ")
        if action.isdigit():
            int_action = int(action)
            return int_action
        else:
            print(
                colored(f"\n{action} is not a valid entry.\n", "yellow", attrs=["bold"])
            )


# ======== BUTTON VALIDATION
def edit_valid_options() -> str:
    edit = (
        input(
            f"\nWhat will you edit?\n{students}, {perdiem}, or {frequency} of perdiem > "
        )
        .lower()
        .strip()
    )
    choices = ["students", "perdiem", "frequency"]
    while edit not in choices:
        print(
            colored(
                f"\n{edit} is not a valid option. Please choose a valid option.\n",
                "yellow",
                attrs=["bold"],
            )
        )
        edit = (
            input(
                f"What will you edit?\n{students}, {perdiem}, or {frequency} of perdiem > "
            )
            .lower()
            .strip()
        )
    return edit


def menu_valid() -> str:
    commands = ["edit", "view", "add", "quit"]
    print(menu.center(85))
    print(
        f"""{edit} your profile     {view} a report    {add} an expense     {quit}\n""".center(
            10
        )
    )
    action = input("> ").lower().strip()
    while action not in commands:
        print(
            colored(
                f"\n{action} is not a valid option. Please choose a valid option.\n",
                "yellow",
                attrs=["bold"],
            )
        )
        action = input("> ").lower().strip()
    return action


# =========== DATE VALIDATION


def check_future_csv():
    while True:
        action = (
            input(
                "What is the month and year of the report you would like to add to?\n Example entry is (May 20XX) > "
            )
            .title()
            .strip()
        )
        today = datetime.now()
        try:
            datetime.strptime(action, "%B %Y")
            if bool(parser.parse(action) <= today):
                return action
            else:
                print(
                    colored(
                        f"\n{action} is a future date. Please provide a date in the past.\n",
                        "yellow",
                        attrs=["bold"],
                    )
                )
        except AttributeError:
            print(
                colored(f"\n{action} is not a valid date.\n", "yellow", attrs=["bold"])
            )
        except ValueError:
            print(
                colored(f"\n{action} is not a valid date.\n", "yellow", attrs=["bold"])
            )


# ============ USER LOGIN FUNCTIONS ==============
def create_user(USERS: dict) -> str:
    User.Creation_Date = check_date()
    User.Last_Login = check_date()
    User.User_Name = create_user_valid(USERS)
    if User.User_Name == "quit":
        return User.User_Name
    User.Password = pwinput.pwinput(prompt="Password > ").strip()
    if User.Password == "quit":
        return User.Password
    User.Per_Diem = amt_Per_Diem()
    User.Amt_Students = valid_amt_students()
    User.Debit_Frequency = valid_debit_frequency()
    amountperdiem()
    addperdiem()
    with open("users_file.txt", "a") as user_file:
        user_file.write(
            f"{User.User_Name},{User.Password},{User.Per_Diem},{User.Amt_Students},{User.Creation_Date}, {User.Last_Login},{User.Balance},{User.Debit_Frequency}\n"
        )
    return User.User_Name


def existing_user() -> None:
    with open("users_file.txt", "r") as users_file:
        users_raw = users_file.readlines()
        for person in users_raw:
            person_raw_list = person.split(",")
            if User.User_Name in person_raw_list:
                User.Per_Diem = float(person_raw_list[2])
                User.Amt_Students = int(person_raw_list[3])
                User.Creation_Date = person_raw_list[4]
                User.Last_Login = person_raw_list[5]
                User.Balance = float(person_raw_list[6])
                User.Debit_Frequency = int(person_raw_list[7])
                return None


def user_dictionary() -> dict:
    USERS = {}
    with open("users_file.txt", "r") as user_file:
        raw_file = user_file.readlines()
        for item in raw_file:
            raw_user_pword = item.split(",")
            USERS[raw_user_pword[0]] = [
                raw_user_pword[1].strip(),
                raw_user_pword[2].strip(),
                raw_user_pword[3].strip(),
                raw_user_pword[4],
            ]
        return USERS


def perdiem_manual() -> None:
    times = perdiem_manual_valid()
    User.Amt_Gain = times * (User.Per_Diem * User.Amt_Students)
    User.Balance += User.Amt_Gain


def perdiem_ask() -> None:
    today = date.today()
    raw_date = User.Last_Login.split()
    raw_month = raw_date[0]
    day = int(raw_date[1])
    year = int(raw_date[2])
    month = datetime.strptime(raw_month, "%B").month
    last_login_done = date(year, month, day)
    debit = today - last_login_done
    pay = debit.days
    amount_of_times = trunc(pay % User.Debit_Frequency)
    print(
        f"\nYou normally receive your perdiem amount every {User.Debit_Frequency} days. \nBased on your last login, you would receive {amount_of_times} time periods of per diem.\n"
    )
    action = perdiem_ask_valid()
    if action == "yes":
        calculateperdiem()
    else:
        perdiem_manual()


# ==================== DATE FUNCTIONS =====================


def check_date() -> str:
    now = datetime.now()
    date_time_str = now.strftime("%B %d %Y")
    return date_time_str.title()


def check_month() -> str:
    now = datetime.now()
    month_time_str = now.strftime("%B %Y")
    return month_time_str.title()


def lastloginwrite(last_user) -> None:
    replace_user = f"{User.User_Name},{User.Password},{User.Per_Diem},{User.Amt_Students},{User.Creation_Date},{User.Last_Login},{User.Balance},{User.Debit_Frequency}"
    with open(r"users_file.txt", "r") as file:
        data = file.read()
        data = data.replace(last_user, replace_user)
    with open(r"users_file.txt", "w") as file:
        file.write(data)


# ============ CSV WRITING ======================
def expense_choice(path):
    action = ""
    while action not in ("current", "past"):
        action = (
            input(f"\nWould you like to record a {current} or {past} expense? > ")
            .lower()
            .strip()
        )
        if action == "current":
            write_csv(path)
        elif action == "past":
            write_past_csv(path)
        else:
            print(
                colored(f"\n{action} is not a valid input.", "yellow", attrs=["bold"])
            )


def append_csv(path) -> None:
    date_time_str = check_date()
    month_time_str = check_month()
    input_purchase = input("Enter the location of the purchase > ").title().strip()
    input_amt = valid_expense()
    remaining_balance(input_amt)
    row = [input_purchase, input_amt, date_time_str, User.Balance]
    with open(f"{path}/{month_time_str}.csv", "a") as current_file:
        csv_writer = csv.writer(current_file)
        csv_writer.writerow(row)
    print(
        colored(
            f"\n<<<< The report for {month_time_str} has been updated! >>>>",
            attrs=["bold"],
        )
    )
    time.sleep(2)


def append_past_csv(path, action):
    if os.path.exists(f"{path}/{action}.csv"):
        with open(f"{path}/{action}.csv", "a") as current_file:
            csv_writer = csv.writer(current_file)
            input_purchase = (
                input("Enter the location of the purchase > ").title().strip()
            )
            input_amt = valid_expense()
            remaining_balance(input_amt)
            row = [input_purchase, input_amt, action, User.Balance]
            csv_writer.writerow(row)
        print(
            colored(
                f"\n<<<< The report for {action} has been updated! >>>>", attrs=["bold"]
            )
        )
        time.sleep(2)


def write_past_csv(path):
    action = check_future_csv()
    if not os.path.exists(f"{path}/{action}.csv"):
        with open(f"{path}/{action}.csv", "w+") as current_file:
            fields = ["POS", "Spent", "Date", "Balance"]
            csv_writer = csv.DictWriter(current_file, fieldnames=fields)
            csv_writer.writeheader()
        append_past_csv(path, action)
        print(
            colored(
                f"\n<<<< New file {action} was created for the {path} directory! >>>>",
                attrs=["bold"],
            )
        )
        time.sleep(2)
    else:
        append_past_csv(path, action)


def write_csv(path) -> None:
    month_time_str = check_month()
    if not os.path.exists(f"{path}/{month_time_str}.csv"):
        with open(f"{path}/{month_time_str}.csv", "w+", newline="") as current_file:
            fields = [f"POS", f"Spent", f"Date", f"Balance"]
            csv_writer = csv.DictWriter(current_file, fieldnames=fields)
            csv_writer.writeheader()
        print(colored(f"\n<<<< New profile for {path} created! >>>>", attrs=["bold"]))
        time.sleep(2)
    else:
        append_csv(path)


def folder_to_file(USERS, month_time_str) -> str:
    folder = []
    for user in USERS.keys():
        folder.append(user)
    for name in folder:
        if name == User.User_Name:
            spot = folder.index(name)
    path = folder[spot]
    if not os.path.exists(path):
        os.makedirs(path)
        write_csv(path)
        return path
    else:
        return path


# ================ USER WORKFLOW =========================


# ===== EDIT BUTTON =====
def edit_profile(last_user) -> str:
    edit = edit_valid_options()
    if edit == "students":
        User.Amt_Students = edit_students()
    elif edit == "perdiem":
        User.Per_Diem = edit_perdiem()
    elif edit == "frequency":
        User.Debit_Frequency = edit_debit_frequency()
    replace_user = f"{User.User_Name},{User.Password},{User.Per_Diem},{User.Amt_Students},{User.Creation_Date},{User.Last_Login},{User.Balance},{User.Debit_Frequency}"
    with open(r"users_file.txt", "r") as file:
        data = file.read()
        data = data.replace(last_user, replace_user)
    with open(r"users_file.txt", "w") as file:
        file.write(data)
    print(colored(f"\n<<<< {edit.title()} has been updated! >>>>", attrs=["bold"]))
    time.sleep(2)
    return replace_user


def edit_students() -> int:
    previous_students = User.Amt_Students
    int_new_students = valid_amt_students()
    validation = input(
        f"You have changed the amount of students from {previous_students} to {int_new_students}.\nPress {enter} to continue."
    )
    return int_new_students


def edit_perdiem() -> float:
    previous_perdiem = "${:,.2f}".format(User.Per_Diem)
    while True:
        new_perdiem = input("How much is the perdiem per student? > ")
        try:
            float_new_perdiem = float(new_perdiem)
            if float_new_perdiem > 0:
                formatted_new = "${:,.2f}".format(float_new_perdiem)
                validation = input(
                    f"You have changed the amount of per diem per student from {previous_perdiem} to {formatted_new}.\nPress {enter} to continue."
                )
                return float_new_perdiem
            else:
                print(
                    colored(
                        "\nPlease put in a positive amount.\n", "yellow", attrs=["bold"]
                    )
                )
        except ValueError:
            print(
                colored(
                    f"\n{new_perdiem} is not a valid number.\n",
                    "yellow",
                    attrs=["bold"],
                )
            )


def edit_debit_frequency() -> int:
    previous_freq = User.Debit_Frequency
    debit_frequency = valid_debit_frequency()
    validation = input(
        f"You have changed the frequency of your per diem from {previous_freq} days to {debit_frequency} days.\nPress {enter} to continue."
    )
    return debit_frequency


# ===== VIEW BUTTON ======


def view_reports(path) -> None:
    while True:
        report_choice = (
            input(f"Do you want to view {current} month or {past} a month? > ")
            .lower()
            .strip()
        )
        if report_choice == "current":
            read_current_csv(path)
            action = input(f"Press {enter} to return to main menu.")
            return None
        elif report_choice == "past":
            read_past_csv(path)
            action = input(f"Press {enter} to return to main menu.")
            return None
        else:
            print(colored("Invalid choice", "yellow", attrs=["bold"]))


def read_past_csv(path) -> None:  # back to normal
    while True:
        action = (
            input(
                f"Which monthly report would you like to view?\n Example entry is (May 20XX) or go {back} > "
            )
            .title()
            .strip()
        )
        if action == "Back":
            return None
        if os.path.exists(f"{path}/{action}.csv"):
            print(
                colored(
                    f"\nExpense Report for {action}\n",
                    "magenta",
                    attrs=["bold", "underline"],
                )
            )
            with open(f"{path}/{action}.csv", "r") as current_file:
                csv_reader = csv.DictReader(current_file)
                table = PrettyTable()
                table.field_names = [
                    colored("Date:", "magenta", attrs=["bold"]),
                    colored("Location:", "magenta", attrs=["bold"]),
                    colored("Spent:", "magenta", attrs=["bold"]),
                    colored("Remaining Balance:", "magenta", attrs=["bold"]),
                ]

                for data in csv_reader:
                    spent_raw = "${:,.2f}".format(float(data["Spent"]))
                    balance = "${:,.2f}".format(float(data["Balance"]))
                    spent = colored(spent_raw, "red")
                    table.add_row([data["Date"], data["POS"], spent, balance])
                table.sortby = colored("Date:", "magenta", attrs=["bold"])
                print(table)
                return None
                if len(data) == 0:
                    print(
                        colored(
                            "\nThere are no expenses in this report.",
                            attrs=["bold", "underline"],
                        )
                    )
        else:
            print(
                colored(f"\n{action} is not a valid input.\n", "yellow", attrs=["bold"])
            )


def read_current_csv(path) -> None:
    month_time_str = check_month()
    print(
        colored(
            f"\nExpense Report for {month_time_str}\n",
            "magenta",
            attrs=["bold", "underline"],
        )
    )
    with open(f"{path}/{month_time_str}.csv", "r") as current_file:
        csv_reader = csv.DictReader(current_file, fieldnames=None)
        table = PrettyTable()
        table.field_names = [
            colored("Date:", "magenta", attrs=["bold"]),
            colored("Location:", "magenta", attrs=["bold"]),
            colored("Spent:", "magenta", attrs=["bold"]),
            colored("Remaining Balance:", "magenta", attrs=["bold"]),
        ]
        if (
            bool(csv_reader)
        ) == False:  # if i flip this to true i get the msg if its on false we get reports
            print(
                colored(
                    "\nThere are no expenses in this report.",
                    attrs=["bold", "underline"],
                )
            )
        else:
            for data in csv_reader:
                spent_raw = "${:,.2f}".format(float(data["Spent"]))
                balance = "${:,.2f}".format(float(data["Balance"]))
                spent = colored(spent_raw, "red")
                table.add_row([data["Date"], data["POS"], spent, balance])
            table.sortby = colored("Date:", "magenta", attrs=["bold"])
            print(table)


# ================ MATH FUNCTIONS ========================
def calculateperdiem() -> None:
    today = date.today()
    raw_date = User.Last_Login.split()
    raw_month = raw_date[0]
    day = int(raw_date[1])
    year = int(raw_date[2])
    month = datetime.strptime(raw_month, "%B").month
    last_login_done = date(year, month, day)
    debit = today - last_login_done
    pay = debit.days
    if pay >= User.Debit_Frequency:
        amount_of_weeks = trunc(pay / User.Debit_Frequency)
        User.Amt_Gain = amount_of_weeks * User.Weekly_Add
        User.Balance += User.Amt_Gain
        User.Last_Login = check_date()


def amountperdiem() -> None:
    User.Weekly_Add = User.Per_Diem * User.Amt_Students


def remaining_balance(amt_spent: float) -> None:
    User.Balance -= amt_spent


def addperdiem() -> None:
    User.Balance += User.Weekly_Add


# ================= MAIN =================


def main() -> None:
    # ======= VARIABLES =========
    current_month = check_month()
    USERS = user_dictionary()
    print(title.center(85), "\n")
    action = login_valid()
    user_pass = ""
    logged_in = False
    perdiem_asked = False
    last_user = "_"
    # =======
    while action != "quit" and user_pass != "quit":
        if not logged_in:
            if action == "create":
                user_pass = create_user(USERS)
                USERS = user_dictionary()
                if user_pass != "quit":
                    path = folder_to_file(USERS, current_month)
                    logged_in = True
                    os.system("clear")
                    last_user = f"{User.User_Name},{User.Password},{User.Per_Diem},{User.Amt_Students},{User.Creation_Date},{User.Last_Login},{User.Balance},{User.Debit_Frequency}"
                    perdiem_asked = True
            elif action == "login":
                USERS = user_dictionary()
                user_pass = existing_user_valid(USERS)
                existing_user()
                if user_pass != "quit":
                    path = folder_to_file(USERS, current_month)
                    logged_in = True
                    os.system("clear")
                    last_user = f"{User.User_Name},{User.Password},{User.Per_Diem},{User.Amt_Students},{User.Creation_Date},{User.Last_Login},{User.Balance},{User.Debit_Frequency}"
        else:
            if not perdiem_asked:
                print(title.center(85))
                perdiem_ask()
                perdiem_asked = True
                os.system("clear")
            else:
                print(title.center(85))
                userbalance = "${:,.2f}".format(User.Balance)
                print(
                    colored(
                        f"\n{User.User_Name}               Current Balance: {userbalance}            {User.Last_Login}\n".center(
                            85
                        ),
                        attrs=["bold"],
                    )
                )
                calculateperdiem()
                action = menu_valid()
                if action == "edit":
                    last_user = edit_profile(last_user)
                elif action == "view":
                    view_reports(path)
                elif action == "add":
                    expense_choice(path)
                os.system("clear")
    lastloginwrite(last_user)


if __name__ == "__main__":
    main()
