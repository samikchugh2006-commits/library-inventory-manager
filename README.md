# Library Inventory Manager

**Course:** Programming for Problem Solving using Python  
**Assignment:** Object-Oriented Design and Robust Programming in a Library Management System

## Project overview
A small command-line library inventory manager built with Python using OOP principles.  
Features:
- `Book` dataclass with `title`, `author`, `isbn`, and `status` (`available`/`issued`).
- `LibraryInventory` class to manage book records.
- JSON file persistence (`books.json`) with safe load/save and corrupted-file backup handling.
- Menu-driven CLI: Add, Issue, Return, View All, Search, Exit.
- Exception handling and logging (`library_manager.log`).
- Project packaged with Python package layout.

## Files & structure
library-inventory-manager/
├─ cli/
│ └─ main.py # CLI entrypoint
├─ library_manager/
│ ├─ init.py
│ ├─ book.py
│ └─ inventory.py
├─ run.py # run this file to start
├─ books.json # created automatically
├─ library_manager.log
├─ README.md


markdown
Copy code

## How to run (NO terminal needed)
### Use an IDE (VS Code recommended)
1. Open the project folder in VS Code: **File → Open Folder → select `library_inventory_manager`** (project root).
2. Open `run.py`.
3. Click the **Run ▶** button at the top-right of the editor or right-click in `run.py` and select **Run Python File in Terminal**.
4. The interactive menu will appear in the integrated terminal.


