import tkinter as tk
import difflib

from DownlaodData import download_database

tables = download_database()
# continue with rest of code using tables



INITIAL_RESULTS_COUNT = 20
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
    # set the width and height of the window
    width = 1000
    height = 800
    # get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate the x and y coordinates to center the window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    # set the position of the window
    window.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
    for line in table["dLine"].values():
        if line:
            doc_text.insert("end", line + "\n")
    doc_text.insert("end", "\n")  # Add a newline character between the two sets of values
    s_lines = ""
    for line in table["SLine"].values():
        if line:
            doc_text.insert("end", line + "\n")
            s_lines += line + "\n"
    doc_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=doc_text.yview)
    doc_text.config(state="disabled")
    
    # Copy the SLines to the clipboard
    window.clipboard_clear()
    window.clipboard_append(s_lines)

    

    

def on_search(event=None):
    # Called when the search entry changes
    query = search_entry.get().lower()
    search_results = search_tables(query)
    
    # Clear the results frame
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    # Create a canvas to hold the search results
    canvas = tk.Canvas(results_frame, width=470, height=700)  # Set the width and height of the canvas
    canvas.grid(row=0, column=0, sticky="news")
    
    # Create a frame to hold the search result buttons
    button_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    
    # Display the search results
    for i, table in enumerate(search_results):
        doc_button = tk.Button(
            button_frame,
            text=f"{table['Title']}\n{table['subTitle']}",
            font=("Arial", 12),
            fg="black",
            cursor="hand2",
            padx=10,
            pady=10,
            bg="#adb5bd",
            command=lambda table=table: show_table_doc(table),
            width=50  # Set the width of the button
        )
        doc_button.grid(row=i, column=0, sticky="w")
        doc_button.bind("<Enter>", lambda event,
                        btn=doc_button: btn.config(bg="#dee2e6"))
        doc_button.bind("<Leave>", lambda event,
                        btn=doc_button: btn.config(bg="#adb5bd"))
    
    # Update the canvas scrollregion to include all the search result buttons
    button_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Create a vertical scrollbar and attach it to the canvas
    scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.config(yscrollcommand=scrollbar.set)
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
root.configure(bg="#171515")
# set the width and height of the window
width = 1000
height = 800
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
