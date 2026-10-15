# Student Records System

This is a Student Records System for a tech institute which captures the student's information and scores. It is also able to display information about the students when needed, and logs encountered errors.

A training school keeps student test scores in a simple text file. People key in data manually, so it is full of mistakes such as missing names, scores like "N/A" or above 100 or below 0, the same student ID twice, blank lines, and rows with too few numbers. This program reads the file safely, keeps the correct records, and logs the wrong ones.

## Setup

- Python 3 is required. No extra libraries are needed.
- Run the program from the project folder:

    python main.py

## Menu

1. Create/reset sample data
2. View all students
3. Search for a student by ID
4. Add a new student
5. Generate report
6. Exit

The program keeps running until the user chooses 6.

## File Format

Each line in `students.txt` is one student:

    student_id,full_name,python,sql,excel

Example:

    ST001,Chiamaka Nnedi,78,84,91

The sample file has 22 lines: 14 valid records and 8 deliberately invalid ones to test the validation.

## Validation Rules

A record is rejected if:
- the line is blank
- it does not have exactly 5 fields
- the student ID or name is missing
- the student ID is a duplicate (IDs are compared in capital letters, so "st001" equals "ST001")
- a score is not a whole number (e.g. "N/A")
- a score is below 0 or above 100

Every rejected record is appended to `errors.log` with the record and the reason it was rejected.

## Grading Scale

| Average | Grade | Category |
|---------|-------|----------|
| 90 - 100 | A | Excellent |
| 80 - 89.99 | B | Very Good |
| 70 - 79.99 | C | Good |
| 60 - 69.99 | D | Average |
| Below 60 | F | Needs Improvement |

## Files

| File | Purpose | Mode |
|------|---------|------|
| `main.py` | The program | - |
| `students.txt` | Student records | `w` to reset, `r` to read, `a` to add a student |
| `errors.log` | Rejected records and reasons | `a` (keeps previous entries) |
| `results_report.txt` | Results and class statistics | `w` (fresh report every time) |
| `TESTING.md` | Test cases and results | - |

## Design Decisions

- **Validation:** `validate_record` checks each record for correctness and completeness. If anything is wrong it raises a `ValueError`; if not, it returns the student with the scores as numbers. It is used both when loading the file and when adding a student, so the rules are written once.
- **One bad record does not stop the rest:** each line is checked inside its own `try/except`, so a bad line is logged and the program moves to the next line.
- **Validate before writing:** a new student is only appended to `students.txt` after every check passes.
- **Missing file:** if `students.txt` does not exist, the program shows a message and the menu still works, so the user can choose option 1 to create it.
- **Errors return the user to the menu:** invalid menu input is caught and the menu is shown again.
- **Reused helpers:** `calculate_average`, `determine_grade` and `log_error` are used by more than one part of the program.
