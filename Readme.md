# 📊 Comparator

A simple tool that reads your data recipes (JSON), runs comparisons automatically, and gives you the results in a neat Excel file. **No coding required.**

---

## 📁 Folder Setup (Critical!)

Place your `comparator.exe` in a folder with this exact structure:
```
Your_Folder/
│
├── comparator.exe
├── querys-schema.json
│
├── sequences/ ← Put your .json recipes here
│ └── MyCheck.json
│
└── querys/ ← SQL templates (don't edit these)
├── totalMatch.sql
└── ...
```

> ⚠️ If these folders aren't next to the `.exe`, the tool won't find your files.

---

## ▶️ How to Run
1. Double-click `comparator.exe`.
2. A menu will show all JSON files in your `sequences/` folder.
3. Type the number of the one you want and press **Enter**.
4. Check the results in **`result.xlsx`** (saved in the same folder).

---

## 📝 Writing Your Recipe (JSON)

Create a `.json` file in the `sequences/` folder. It's a list of steps. Here are the most common fields:

| Field | What it means | Example |
| :--- | :--- | :--- |
| `name` | Sheet name in Excel. | `"Invoice Check"` |
| `typeofcomparison` | How to compare. | `"Total Match"`, `"Inner Join"`, `"Outer Join"` |
| `table1` / `table2` | The data sources. | `"orders"` |
| `column1` | Primary column to match/join on. | `"OrderID"` |
| `column2` | Secondary column (used for combines or difference calculations). | `"TotalAmount"` |
| `savetoexcel` | Save results? | `true` |

**Example JSON:**
```json
[
    {
        "name": "Missing Orders",
        "typeofcomparison": "Outer Join",
        "table1": "Sales_2024",
        "table2": "Sales_2025",
        "column1": "Order_ID",
        "column2": "TotalAmount",
        "savetoexcel": true
    }
]
```
🛠️ Quick Fixes (Troubleshooting)
Problem	Solution
No JSON files found.	Put your .json files in the sequences/ folder.
Window closes on error.	It now pauses automatically. Read the red error text, fix the JSON, and rerun.
Excel file is empty.	Double-check your table1 / table2 names exist in the data.



Reporte SFDC (Access - Integrity Order Report): https://advanta-seeds.lightning.force.com/lightning/r/Report/00OS3000004ltmjMAA/view?queryScope=userFolders

Reporte SFDC (Access - Line Item Control): https://advanta-seeds.lightning.force.com/lightning/r/Report/00OS30000052gujMAA/view?queryScope=userFolders

Reporte SFDC (Access Invoice & Line ltem 5491): https://advanta-seeds.lightning.force.com/lightning/r/Report/00OS3000005fpmrMAA/view

OLD - Reporte SFDC (Access - Invoices Report 5491): https://advanta-seeds.lightning.force.com/lightning/r/Report/00OS3000004oz4yMAA/view?queryScope=userFolders


:
