import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import database

def open_main_window():
    window = tk.Toplevel(root)
    window.title("College Library Management System")
    window.geometry("600x400")

    img_path = "C:/Users/ljuli/Pictures/PAUL/test/Background.jpg"
    bg_image = Image.open(img_path)
    bg_image = bg_image.resize((600, 400), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image

    def get_selected_row(event):
        global selected_tuple
        if not book_list.curselection():
            return
        index = book_list.curselection()[0]
        selected_tuple = book_list.get(index)
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, selected_tuple[1])
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, selected_tuple[2])
        entry_BN.delete(0, tk.END)
        entry_BN.insert(tk.END, selected_tuple[3])
        entry_genre.delete(0, tk.END)
        entry_genre.insert(tk.END, selected_tuple[4])

    def view_command():
        book_list.delete(0, tk.END)
        for row in database.view_books():
            book_list.insert(tk.END, row)

    def search_command():
        book_list.delete(0, tk.END)
        for row in database.search_books(title_text.get(), author_text.get(), BN_text.get(), genre_text.get()):
            book_list.insert(tk.END, row)

    def add_command():
        database.insert_book(title_text.get(), author_text.get(), BN_text.get(), genre_text.get())
        book_list.delete(0, tk.END)
        book_list.insert(tk.END, (title_text.get(), author_text.get(), BN_text.get(), genre_text.get()))

    def delete_command():
        database.delete_book(selected_tuple[0])
        view_command()

    def update_command():
        database.update_book(selected_tuple[0], title_text.get(), author_text.get(), BN_text.get(), genre_text.get())
        view_command()

    def borrow_command():
        book_id = selected_tuple[0]
        database.borrow_book(current_user[0], book_id)
        messagebox.showinfo("Success", "Book borrowed successfully")
        view_command()

    def return_command():
        book_id = selected_tuple[0]
        conn = sqlite3.connect("library.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM borrow WHERE user_id=? AND book_id=? AND return_date IS NULL",
                    (current_user[0], book_id))
        borrow_id = cur.fetchone()
        conn.close()

        if borrow_id:
            database.return_book(borrow_id[0])
            messagebox.showinfo("Success", "Book returned successfully")
            view_borrowed_books_command()
        else:
            messagebox.showwarning("Warning", "You have not borrowed this book")

    def view_borrowed_books_command():
        book_list.delete(0, tk.END)
        for row in database.view_borrowed_books(current_user[0]):
            book_list.insert(tk.END, row)



    canvas.create_text(100, 25, text="Title: ", fill="white", anchor="w")
    title_text = tk.StringVar()
    entry_title = tk.Entry(window, textvariable=title_text)
    canvas.create_window(150, 25, window=entry_title, anchor="w")

    canvas.create_text(350, 25, text="Author: ", fill="white", anchor="w")
    author_text = tk.StringVar()
    entry_author = tk.Entry(window, textvariable=author_text)
    canvas.create_window(400, 25, window=entry_author, anchor="w")

    canvas.create_text(100, 75, text="Book NO: ", fill="white", anchor="w")
    BN_text = tk.StringVar()
    entry_BN = tk.Entry(window, textvariable=BN_text)
    canvas.create_window(150, 75, window=entry_BN, anchor="w")

    canvas.create_text(350, 75, text="Genre: ", fill="white", anchor="w")
    genre_text = tk.StringVar()
    entry_genre = tk.Entry(window, textvariable=genre_text)
    canvas.create_window(400, 75, window=entry_genre, anchor="w")

    book_list = tk.Listbox(window, height=10, width=50)
    canvas.create_window(50, 125, window=book_list, anchor="nw")

    scrollbar = tk.Scrollbar(window)
    canvas.create_window(365, 125, window=scrollbar, anchor="nw", height=163)

    book_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=book_list.yview)

    book_list.bind('<<ListboxSelect>>', get_selected_row)

    tk.Button(window, text="View All", width=12, command=view_command).place(x=450, y=125)
    tk.Button(window, text="Search Books", width=12, command=search_command).place(x=450, y=155)
    tk.Button(window, text="Add Books", width=12, command=add_command).place(x=450, y=185)
    tk.Button(window, text="Update Books", width=12, command=update_command).place(x=450, y=215)
    tk.Button(window, text="Delete Books", width=12, command=delete_command).place(x=450, y=245)
    tk.Button(window, text="Borrow Books", width=12, command=borrow_command).place(x=450, y=275)
    tk.Button(window, text="Return Books", width=12, command=return_command).place(x=450, y=305)
    tk.Button(window, text="View Borrowed", width=12, command=view_borrowed_books_command).place(x=450, y=335)
    tk.Button(window, text="Close", width=12, command=window.destroy).place(x=450, y=365)


def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "admin123":
        open_main_window()
        

    else:
        messagebox.showerror("Login Error", "Invalid username or password")

root =tk.Tk()
root.title("login")
root.geometry("400x300")

img_path = r"C:\Users\ljuli\Pictures\PAUL\test\Background.jpg" 
bg_image = Image.open(img_path)
bg_image = bg_image.resize((400, 300), Image.LANCZOS) 
bg_image = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")
canvas.image = bg_image 

canvas.create_text(80, 165, text="Username", fill="white", anchor="w", font=("Times New Roman", 9))
entry_username = tk.Entry(root)
canvas.create_window(150, 165, window=entry_username, anchor="w")

canvas.create_text(80, 200, text="Password", fill="white", anchor="w", font=("Times New Roman", 9))
entry_password = tk.Entry(root, show='*')
canvas.create_window(150, 200, window=entry_password, anchor="w")

login_button = tk.Button(root, text="Login", font =("Times New Roman", 9, "bold"), command=validate_login)
canvas.create_window(150, 235, window=login_button, anchor="w")

register_button = tk.Button(root, text="Register", font =("Times New Roman", 9, "bold"))
canvas.create_window(200, 235, window=register_button, anchor="w")



root.mainloop()