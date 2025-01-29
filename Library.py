import tkinter as tk
from tkinter import ttk, messagebox

# Sample book data
library = [
    {"title": "Python Basics", "author": "John Doe", "isbn": "12345", "available": True},
    {"title": "Advanced Python", "author": "Jane Smith", "isbn": "67890", "available": False},
    {"title": "Data Science Intro", "author": "Alice Brown", "isbn": "11223", "available": True}
]

# Function to display books
def display_books(filtered_list=None):
    books_list.delete(*books_list.get_children())  # Clear previous entries
    book_source = filtered_list if filtered_list is not None else library
    for book in book_source:
        status = "Available" if book["available"] else "Checked Out"
        books_list.insert("", "end", values=(book["title"], book["author"], book["isbn"], status))

# Function to search books
def search_books():
    query = search_entry.get().strip().lower()
    filter_by = filter_var.get()

    if not query:
        display_books()  # Show all books if search is empty
        return

    filtered_books = []
    for book in library:
        if filter_by == "Title" and query in book["title"].lower():
            filtered_books.append(book)
        elif filter_by == "Author" and query in book["author"].lower():
            filtered_books.append(book)
        elif filter_by == "Availability":
            availability_match = "available" if book["available"] else "checked out"
            if query in availability_match.lower():
                filtered_books.append(book)

    display_books(filtered_books)

# Function to add a book
def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Check if book already exists
    for book in library:
        if book["isbn"] == isbn:
            messagebox.showerror("Error", "Book with this ISBN already exists!")
            return

    library.append({"title": title, "author": author, "isbn": isbn, "available": True})
    display_books()
    messagebox.showinfo("Success", f"Book '{title}' added successfully!")
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

# Function to borrow a book
def borrow_book():
    selected_item = books_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a book to borrow!")
        return

    book_isbn = books_list.item(selected_item, "values")[2]
    for book in library:
        if book["isbn"] == book_isbn:
            if not book["available"]:
                messagebox.showwarning("Warning", "Book is already checked out!")
                return
            book["available"] = False
            display_books()
            messagebox.showinfo("Success", f"You borrowed '{book['title']}'!")
            return

# Function to return a book
def return_book():
    selected_item = books_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a book to return!")
        return

    book_isbn = books_list.item(selected_item, "values")[2]
    for book in library:
        if book["isbn"] == book_isbn:
            if book["available"]:
                messagebox.showwarning("Warning", "Book is already available!")
                return
            book["available"] = True
            display_books()
            messagebox.showinfo("Success", f"You returned '{book['title']}'!")
            return

# Create main window
window = tk.Tk()
window.title("Library Management System")
window.geometry("700x500")
window.configure(bg="#F5F5F5")

# Title label
title_label = tk.Label(window, text="Library Management System", font=("Arial", 16, "bold"), bg="#F5F5F5", fg="#333")
title_label.pack(pady=10)

# Search Frame
search_frame = tk.Frame(window, bg="#F5F5F5")
search_frame.pack(pady=5)

tk.Label(search_frame, text="Search:", bg="#F5F5F5").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame, width=25)
search_entry.grid(row=0, column=1, padx=5)

tk.Label(search_frame, text="Filter by:", bg="#F5F5F5").grid(row=0, column=2, padx=5)
filter_var = tk.StringVar(value="Title")
filter_dropdown = ttk.Combobox(search_frame, textvariable=filter_var, values=["Title", "Author", "Availability"])
filter_dropdown.grid(row=0, column=3, padx=5)

search_button = ttk.Button(search_frame, text="Search", command=search_books)
search_button.grid(row=0, column=4, padx=5)

# Book List Frame
list_frame = tk.Frame(window)
list_frame.pack(pady=5, fill="both", expand=True)

columns = ("Title", "Author", "ISBN", "Status")
books_list = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
for col in columns:
    books_list.heading(col, text=col)
    books_list.column(col, width=150)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=books_list.yview)
books_list.configure(yscroll=scrollbar.set)
books_list.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add Book Section
add_frame = tk.Frame(window, bg="#F5F5F5")
add_frame.pack(pady=10)

tk.Label(add_frame, text="Title:", bg="#F5F5F5").grid(row=0, column=0, padx=5)
title_entry = tk.Entry(add_frame, width=20)
title_entry.grid(row=0, column=1, padx=5)

tk.Label(add_frame, text="Author:", bg="#F5F5F5").grid(row=0, column=2, padx=5)
author_entry = tk.Entry(add_frame, width=20)
author_entry.grid(row=0, column=3, padx=5)

tk.Label(add_frame, text="ISBN:", bg="#F5F5F5").grid(row=0, column=4, padx=5)
isbn_entry = tk.Entry(add_frame, width=15)
isbn_entry.grid(row=0, column=5, padx=5)

add_button = ttk.Button(add_frame, text="Add Book", command=add_book)
add_button.grid(row=0, column=6, padx=5)

# Borrow & Return Buttons
action_frame = tk.Frame(window, bg="#F5F5F5")
action_frame.pack(pady=10)

borrow_button = ttk.Button(action_frame, text="Borrow Book", command=borrow_book)
borrow_button.grid(row=0, column=0, padx=10)

return_button = ttk.Button(action_frame, text="Return Book", command=return_book)
return_button.grid(row=0, column=1, padx=10)

# Display initial book list
display_books()

# Start Tkinter event loop
window.mainloop()
