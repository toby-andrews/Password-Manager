from tkinter import *
import random
from tkinter import messagebox
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_clicked():
    global rand_pw
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '_']
    rand_letter = (random.sample(letters, 8))
    rand_symbol = (random.sample(symbols, 8))
    rand_number = (random.sample(numbers, 8))
    rand_list = (rand_letter + rand_symbol + rand_number)
    random.shuffle(rand_list)
    rand_pw = ''.join(map(str, rand_list))
    password.delete(0, END)
    password.insert(0, rand_pw)
    window.clipboard_clear()
    window.clipboard_append(rand_pw)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_clicked():
    website = website_in.get().title()
    email = email_in.get()
    pw = password.get()
    new_data = {
        website: {
            "email": email,
            "password": pw,
        }
    }
    if len(website) < 3:
        messagebox.showwarning(title="Warning", message="The website box is blank")

    elif len(email) < 3:
        messagebox.showwarning(title="Warning", message="The email box is blank")

    elif len(pw) < 3:
        messagebox.showwarning(title="Warning", message="The password box is blank")

    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)  # after except it jumps to finally.
        else:  # remember else will only run if everything in try works. It doesn't run after except.
            # Updating old data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_in.delete(0, END)
            email_in.delete(0, END)
            email_in.insert(END, "tobyandrews@gmail.com")
            password.delete(0, END)


# ---------------------------- SEARCH FUNCTIONALITY ------------------------------- #
def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            search = website_in.get().title()
    except FileNotFoundError:
        messagebox.showwarning(title="No passwords saved", message="You haven't created any passwords yet")
    else:
        if search in data:
            email = data[search]["email"]
            pw = data[search]["password"]
            messagebox.askokcancel(title=f"{search}", message=f"Email:\n{email}\n Password:\n{pw}")
        else:
            messagebox.showwarning(title="Does not Exist", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.minsize(width=200, height=200)
window.config(bg="white", padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
canvas.config(bg="white")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=2, row=0)

# Website text
website_txt = Label(text="Website:", font=("Arial", 18, "bold"), bg='white', fg='black')
website_txt.grid(column=0, row=1)
website_txt.config(pady=2, padx=2)

# Email/Username Text
user_txt = Label(text="Email/Username:", font=("Arial", 18, "bold"), bg='white', fg='black')
user_txt.grid(column=0, row=2)
user_txt.config(pady=2, padx=2)

# Password text
password_txt = Label(text="Password:", font=("Arial", 18, "bold"), bg='white', fg='black')
password_txt.grid(column=0, row=3)
password_txt.config(pady=2, padx=2)

# Website input

website_in = Entry(bg="white", fg="black", width=21, highlightbackground="white", insertbackground="black")
website_in.grid(column=1, row=1, columnspan=2)
website_in.focus()

# Email_input

email_in = Entry(bg="white", fg="black", width=35, highlightbackground="white", insertbackground="black")
email_in.insert(END, "tobyandrews@gmail.com")
email_in.grid(column=1, row=2, columnspan=3)

# Output boc for generate pw

rand_pw = ""
password = Entry(bg="white", fg="black", width=21, highlightbackground="white", insertbackground="black")
password.insert(END, rand_pw)
password.grid(column=1, row=3, columnspan=2)

# Button to generate password

generate_btn = Button(bg="white", text="Generate Password", font=("Arial", 12, "bold"), width=13,
                      highlightbackground="white", command=generate_clicked)
generate_btn.grid(column=3, row=3)

# Button to add to directory

add_directory_btn = Button(text="Add", height=1, width=43, font=("Arial", 12, "bold"), highlightbackground="white",
                           command=add_clicked)
add_directory_btn.grid(column=2, row=4, columnspan=2)

# Button to search through direction
search_directory_btn = Button(text="Search", font=("Arial", 12, "bold"), width=13, highlightbackground="white",
                              command=find_password)
search_directory_btn.grid(column=3, row=1)

window.mainloop()
