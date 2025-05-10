import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, END
from typing import List
from entryModel import JournalEntry
from datetime import datetime
from logic import (
    saveEntryToCsv,
    loadEntriesFromCsv,
    updateEntriesToCSV,
)

class JournalApp:
    """Class for the personal journal GUI."""
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Personal Journal")
        self.root.geometry("500x400")
        self.entries: List[JournalEntry] = []
        self.setupWidgets()
    def setupWidgets(self) -> None:
        """Creates the widgets for the main journal window."""
        self.root.geometry("600x500")
        self.root.minsize(600, 500)
        tk.Label(self.root, text=f"{datetime.now().strftime('%m-%d-%Y')}", font=("Arial", 12), fg="gray").pack(pady=5, fill="x")
        tk.Label(self.root, text="Title", font=("Arial", 12)).pack(pady=2, fill="x")
        self.entryTitle = tk.Entry(self.root, font=("Arial", 12))
        self.entryTitle.pack(fill="x", padx=10, pady=2)
        self.entryText = Text(self.root, height=15, wrap="word", font=("Arial", 12))
        self.entryText.pack(expand=True, fill="both", padx=10, pady=5)
        buttonFrame = tk.Frame(self.root)
        buttonFrame.pack(fill="x", pady=5)

        for text, command in [("Save Entry", self.saveEntry), ("View/Edit Entries", self.showEntries)]:
            tk.Button(buttonFrame, text=text, command=command).pack(side="left", padx=5)
    def run(self) -> None:
        """Runs the Tkinter main loop."""
        self.root.mainloop()

    def saveEntry(self) -> None:
        """Saves a new journal entry to the CSV file."""
        title = self.entryTitle.get().strip()
        entryText = self.entryText.get("1.0", END).strip()

        if not title:
            messagebox.showwarning("Invalid", "Enter a title")
            return

        if not self.validateEntry(entryText):
            messagebox.showwarning("Invalid", "Enter an entry")
            return

        entry = JournalEntry(title=title, content=entryText)
        saveEntryToCsv(entry)
        self.entryTitle.delete(0, END)
        self.entryText.delete("1.0", END)
        messagebox.showinfo("Saved", "Successful")

    def showEntries(self) -> None:
        """New window for viewing, editing, and searching."""
        try:
            self.entries = loadEntriesFromCsv()
            if not self.entries:
                messagebox.showinfo("No Entries", "No previous entries found")
                return
            def formatEntry(index: int, entry: JournalEntry) -> str:
                time = entry.time.strftime('%m-%d-%Y %I:%M %p')
                return f"[{index}] {entry.title}\n{time}\n{entry.content}\n{'-' * 50}\n"
            def displayEntries(entries: list[JournalEntry]) -> None:
                textArea.delete(1.0, END)
                if not entries:
                    textArea.insert(END, "No matching entries found\n")
                    return
                for i, entry in enumerate(entries, 1):
                    entryText = formatEntry(i, entry)
                    textArea.insert(END, entryText)
            def searchEntries() -> None:
                x = searchEntry.get().strip().lower()
                if not x:
                    displayEntries(self.entries)
                else:
                    filtered = [
                        entry for entry in self.entries
                        if x in entry.title.lower() or x in entry.content.lower()
                    ]
                    displayEntries(filtered)
            def editSelected() -> None:
                try:
                    index = int(entryNumber.get()) - 1
                    if not (0 <= index < len(self.entries)):
                        raise IndexError
                    self.editEntry(index)
                    top.destroy()
                except Exception:
                    messagebox.showerror("Invalid", "Input a valid entry number")

            mainWindowX = self.root.winfo_x()
            mainWindowY = self.root.winfo_y()
            top = Toplevel(self.root)
            top.title("Previous Entries")
            top.geometry(f"500x400+{mainWindowX + 50}+{mainWindowY + 50}")
            top.minsize(500, 400)
            scrollBar = Scrollbar(top)
            scrollBar.pack(side="right", fill="y")
            textArea = Text(top, yscrollcommand=scrollBar.set, wrap="word", height=15)
            textArea.pack(expand=True, fill="both", padx=10, pady=10)
            scrollBar.config(command=textArea.yview)
            searchLabel = tk.Label(top, text="Search")
            searchLabel.pack(pady=2)
            searchEntry = tk.Entry(top, font=("Arial", 12))
            searchEntry.pack(fill="x", padx=10)
            searchButton = tk.Button(top, text="Search", command=searchEntries)
            searchButton.pack(pady=5)
            displayEntries(self.entries)
            editLabel = tk.Label(top, text="Entry journal number to edit")
            editLabel.pack(pady=2)
            entryNumber = tk.Entry(top)
            entryNumber.pack(pady=2)
            editButton = tk.Button(top, text="Edit Entry", command=editSelected)
            editButton.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open entries: {e}")
    def editEntry(self, index: int) -> None:
        """New window to edit entry."""
        editWindow = Toplevel(self.root)
        editWindow.title("Edit Entry")
        editWindow.geometry("400x300")
        editText = Text(editWindow, font=("Arial", 12), height=12, width=45)
        editText.insert(END, self.entries[index].content)
        editText.pack(padx=10, pady=10, fill="both", expand=False)
        def saveEdit() -> None:
            newContent = editText.get("1.0", END).strip()

            if self.validateEntry(newContent):
                self.entries[index].content = newContent
                updateEntriesToCSV(self.entries)
                messagebox.showinfo("Updated", "Successful")
                editWindow.destroy()
            else:
                messagebox.showwarning("Invalid", "Cannot save an empty entry")

        saveBtn = tk.Button(editWindow, text="Save Changes", command=saveEdit)
        saveBtn.pack(pady=5)
        editWindow.minsize(400, 300)
    def validateEntry(self, content: str) -> bool:
        """Validates the content of the journal entry."""
        return bool(content.strip())
