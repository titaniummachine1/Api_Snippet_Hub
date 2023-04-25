import tkinter as tk

from DownlaodData import download_database

tables = download_database()
# continue with rest of code using tables



INITIAL_RESULTS_COUNT = 10
def search_tables(query):
    # Search for tables that match the query and return up to 10 results
    results = []
    for table in tables["tables"]:
        if query in table["Title"].lower() or query in table["subTitle"].lower():
            results.append(table)
        elif any(query in doc.lower() for doc in table["dLine"].values()):
            results.append(table)
        elif any(query in code.lower() for code in table["SLine"].values()):
            results.append(table)
        if len(results) == INITIAL_RESULTS_COUNT:
            break
    return results


def show_table_doc(table):
    # Open a new window to display the documentation for the table
    window = tk.Toplevel()
    window.title(table["Title"])
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side="right", fill="y")
    doc_text = tk.Text(window, wrap="word", yscrollcommand=scrollbar.set)
    for line in table["dLine"].values():
        if line:
            doc_text.insert("end", line + "\n")
    for line in table["SLine"].values():
        if line:
            doc_text.insert("end", line + "\n")
    doc_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=doc_text.yview)
    doc_text.config(state="disabled")


def on_search(event=None):
    # Called when the search entry changes
    query = search_entry.get().lower()
    search_results = search_tables(query)
    # Clear the results frame
    for widget in results_frame.winfo_children():
        widget.destroy()
    # Display the search results
    for i, table in enumerate(search_results[:INITIAL_RESULTS_COUNT]):
        doc_button = tk.Button(
            results_frame,
            text=f"{table['Title']}\n{table['subTitle']}",
            font=("Arial", 12),
            fg="black",
            cursor="hand2",
            padx=10,
            pady=10,
            bg="#4CAF50",
            activebackground="#3E8E41",
            command=lambda table=table: show_table_doc(table),
        )
        doc_button.grid(row=i, column=0, sticky="w")
        doc_button.bind("<Enter>", lambda event,
                        btn=doc_button: btn.config(bg="#C0C0C0"))
        doc_button.bind("<Leave>", lambda event,
                        btn=doc_button: btn.config(bg="#E0E0E0"))

    # Display the additional search results
    results = []


# Create the main window and widgets
root = tk.Tk()
root.title("Api Snippet Hub")
search_label = tk.Label(root, text="Search:", font=("Arial", 16))
search_label.configure(bg=root.cget("bg"), fg="#1B1F23")

search_label.pack(side="top")
search_entry = tk.Entry(root, width=77)
search_entry.pack(side="top")
# Bind the search entry to the on_search function

search_entry.bind("<KeyRelease>", lambda event: on_search())
results_frame = tk.Frame(root)
results_frame.pack()
root.configure(bg="#1B1F23")
# set the width and height of the window
width = 800
height = 600
# get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate the x and y coordinates to center the window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

# set the position of the window
root.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))

# Start the main event loop
root.mainloop()
