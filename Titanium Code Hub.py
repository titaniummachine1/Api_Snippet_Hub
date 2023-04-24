import webbrowser
import tkinter as tk
import json

tables = {}

# Load the furniture data from the JSON file
try:
    with open('Lua_Database.json', 'r') as f:
        tables = json.load(f)
except FileNotFoundError:
    print("Error: file not found.")
except json.JSONDecodeError:
    print("Error: invalid JSON format.")

# Print the furniture data to the console
print(tables)

INITIAL_RESULTS_COUNT = 15

def search_tables(query):
    # Search for tables that match the query and return up to 10 results
    results = []
    for table in tables["tables"]:
        if query in table["name"].lower() or any(query in doc.lower() for doc in table["doc"]):
            results.append(table)
        if len(results) == INITIAL_RESULTS_COUNT:
            break
    return results


def show_table_doc(table):
    # Open a web browser to display the documentation for the table
    doc = table["doc"]
    if doc.startswith("http"):
        webbrowser.open(doc)
    else:
        window = tk.Toplevel()
        window.title(table["name"])
        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side="right", fill="y")
        doc_text = tk.Text(window, wrap="word", yscrollcommand=scrollbar.set)
        doc_text.insert("end", doc)
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
        name_button = tk.Button(
            results_frame,
            text=table["name"],
            font=("Arial", 12, "bold"),
            fg="blue",
            cursor="hand2",
            bd=0,
            relief="flat",
            padx=0,
            pady=0,
            bg="#E0E0E0",
            activebackground="#586069",
            command=lambda table=table: show_table_doc(table),
            borderwidth=1,
            highlightthickness=2,
            highlightbackground="#E0E0E0",
            highlightcolor="#E0E0E0",
            disabledforeground="#586069",
            )
        name_button.config(
            relief="ridge",
            overrelief="ridge",
            highlightthickness=5,
            highlightbackground="#586069",
            highlightcolor="#586069",
            )
        name_button.grid(row=i, column=0, sticky="w")
        doc_button = tk.Button(
            results_frame,
            text=table["doc"],
            bd=1,
            relief="flat",
            padx=10,
            pady=5,
            bg="#E0E0E0",
            activebackground="#C0C0C0",
            command=lambda table=table: show_table_doc(table),
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#1B1F23",
            highlightcolor="#586069",
            disabledforeground="#A0A0A0",
            )
        doc_button.config(
            relief="ridge",
            overrelief="ridge",
            highlightthickness=2,
            highlightbackground="#586069",
            highlightcolor="#C0C0C0",
            )
        doc_button.grid(row=i, column=1, sticky="w")
        name_button.bind("<Enter>", lambda event, btn=name_button: btn.config(bg="#C0C0C0"))
        name_button.bind("<Leave>", lambda event, btn=name_button: btn.config(bg="#E0E0E0"))
        doc_button.bind("<Enter>", lambda event, btn=doc_button: btn.config(bg="#C0C0C0"))
        doc_button.bind("<Leave>", lambda event, btn=doc_button: btn.config(bg="#E0E0E0"))
        
    # Show the "Show More" button if there are additional results
    show_more_button.pack_forget()
    if len(search_results) > INITIAL_RESULTS_COUNT:
        show_more_button.pack(side="bottom", pady=10)
        results = search_results[INITIAL_RESULTS_COUNT:]
    else:
        results = []



    # Display the additional search results
def show_more_results():
    
    # Called when the "Show More" button is clicked
    global tables
    search_query = search_entry.get().lower()
    search_results = search_tables(search_query)
    additional_results = search_results[INITIAL_RESULTS_COUNT:]

    # Clear the results frame
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Display the additional search results
    for i, table in enumerate(additional_results):
        name_label = tk.Label(results_frame, text=table["name"], font=("Arial", 12, "bold"), fg="blue", cursor="hand2")
        name_label.grid(row=i, column=0, sticky="w")
        def on_label_click(event, table=table):
            show_table_doc(table)
        name_label.bind("<Button-1>", on_label_click)
        doc_label = tk.Label(results_frame, text=table["doc"])
        doc_label.grid(row=i, column=1, sticky="w")

    # Hide the "Show More" button if there are no more results
    show_more_button.pack_forget()
    if len(search_results) > INITIAL_RESULTS_COUNT + len(additional_results):
        show_more_button.pack(side="bottom", pady=10)


           
# Create the main window and widgets
root = tk.Tk()
root.title("Titanium Code Hub")
search_label = tk.Label(root, text="Search:")
search_label.pack(side="top")
search_entry = tk.Entry(root, width=77)
search_entry.pack(side="top")
# Bind the search entry to the on_search function

search_entry.bind("<KeyRelease>", lambda event: on_search())
results_frame = tk.Frame(root)
results_frame.pack()
root.configure(bg="#1B1F23")
# Get the width of the screen
screen_width = root.winfo_screenwidth()
# Set the size and position of the main window
root.geometry(f"{screen_width}x500+0+150")

# Start the main event loop
root.mainloop()
