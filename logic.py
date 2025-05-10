import csv
from entryModel import JournalEntry
from typing import List
from datetime import datetime

csvFile = "entries.csv"

def saveEntryToCsv(entry: JournalEntry) -> None:
    """Saves the journal entry to the CSV."""
    with open(csvFile, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([entry.title, entry.content, entry.time.strftime('%m-%d-%Y %I:%M %p')])
def loadEntriesFromCsv() -> List[JournalEntry]:
    """Loads the journal entries from the CSV."""
    entries = []
    try:
        with open(csvFile, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    title, content, timeStr = row
                    time = datetime.strptime(timeStr, '%m-%d-%Y %I:%M %p')
                    entry = JournalEntry(title=title, content=content, time=time)
                    entries.append(entry)
                else:
                    print(f"Skipping invalid rows: {row}")
    except FileNotFoundError:
        pass
    return entries
def updateEntriesToCSV(entries):
    """Edits the journal entries to the CSV."""
    with open("entries.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow([entry.title, entry.content, entry.time.strftime('%m-%d-%Y %I:%M %p')])

