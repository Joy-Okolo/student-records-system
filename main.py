#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' This is a Student Records System for a tech institute which captures the student's information and scores
It is also able to display information about the students when needed, and logging encountered errors.
We will be working with six different menu, which are:

1. Create/reset sample data
2. View all students
3. Search for a student by ID
4. Add a new student
5. Generate report
6. Exit
'''

def create_sample_file() -> bool:
    """This function creates or resets students.txt file with 22 sample records.

    The file is opened in write mode, so any old content is erased
    first. Some records are deliberately wrong/invalid to test the validation.

    Returns:
        True if the file was written, otherwise False.
    Args:
        None.    
    Raises:
        None. An OSError (e.g. no permission to write) is caught inside
        the function and reported with a message instead.    
    """
    try:
        with open("students.txt", "w") as f:   # "w" = write mode: create the file, or erase it if it already exists.
            f.write("ST001,Chiamaka Nnedi,78,84,91\n")
            f.write("ST002,Joy Okolo,65,72,69\n")
            f.write("ST003,Imole Ade,90,88,94\n")
            f.write("ST004,Peace Peter,55,61,70\n")
            f.write("ST005,Julia Aku,81,77,86\n")
            f.write("ST006,Seun Lamina,105,74,80\n")    # score above 100.
            f.write("ST007,Chika Eze,N/A,68,75\n")      # score is not a number.
            f.write("ST008,Esther Musa,90,82\n")        # only 4 fields whereas 5 is required.
            f.write("\n")                               # creates blank line.
            f.write("ST009,Daniel John,71,65,79\n")
            f.write("ST010,Ruth Offiah,88,92,90\n")
            f.write("ST003,Michael Ade,73,80,76\n")     # duplicate ID (ST003 was previously used).
            f.write("ST011,,78,84,90\n")                # missing name.
            f.write("ST012,Peter Amos,66,70,74\n")
            f.write("ST013,Jane Okoro,95,93,96\n")
            f.write(",Henry Uche,48,55,60\n")           # missing ID.
            f.write("ST014,Grace Bello,-7,60,65\n")     # negative score.
            f.write("ST015,Sullivan Chime,76,82,79\n")
            f.write("ST016,Ola Dopamu,69,73,77\n")
            f.write("ST017,Joy James,84,87,89\n")
            f.write("ST018,Samuel Olaniyi,57,63,68\n")
            f.write("ST019,Peller Adelaja,66,70,74\n")

    except OSError as ose:                        # if the file could not be written, throw an exception and retur False
        print("Unable to create sample file:", ose)
        return False

    else:                                       # if no error, share a successful message and return True
        print("Sample file created/reset successfully.")
        return True


# In[2]:


with open("students.txt", "r") as f:         # Open the file we just created, in read mode.
   print(f.read()) 


# In[3]:


def log_error(record: str, reason: str):    # Takes the bad record and the reason; returns nothing.
    """This function Appends/adds a rejected or invalid student record and its reason to errors.log file.
    append mode keeps previous records, so the log builds up a history of every rejected records.

    Args:
        record: The rejected record.
        reason: The reason why the record was rejected.

    Returns:
        None.

    Raises:
        None. It is an OSError, it only writes to the error log 
        and reports with a message so the program keeps running.
    """
    try:
        with open("errors.log", "a") as f:  # "a" adds to the end and never erase old records.
            f.write(f"Record: {record} | Reason: {reason}\n")   # document it as one line per rejected record inside errors.log file.

    except OSError as ose:  # If for any reason, the file could not open or be written into, notify the user and continue the log.
        print("Unable to write to error log:", ose)


# In[4]:


log_error("ST998,,70,70,70", "Missing student name")

with open("errors.log", "r") as f:   # Open the log in read mode.
    print(f.read())                  # Show everything in the log.


# In[5]:


def validate_record(line: str, seen_ids: list):
    """This function checks each of the student's record against all the business rules. 
    If the function finishes without raising an error, the record is valid.

    Args:
       Each line of student's records in student.txt, and other records that will be added
       and IDs of students already accepted.

    Returns:
        None. Reaching the end without an error means the record is valid.

    Raises:
        ValueError: If the line is blank, does not have exactly 5 fields,
            has a missing ID or name, has a duplicate ID, or has a score
            that is not a whole number from 0 to 100.
    """
    if line == "\n" or line == "":              # If the line is empty or just an end of line, throw a valuerror exception
        raise ValueError("Blank line")          

    fields = [] 
    current = ""

    for character in line:                      # Look at the line one character at a time.
        if character == "\n":                   # Skip the "end of line" character.
            continue

        if character == ",":                    # A comma means the current piece of record is finished.
            fields = fields + [current]         # Add the finished piece to the end of the list.
            current = ""                        # reset to empty piece.
        else:                                   # Any other character belongs to the current piece.
            current = current + character       # Add it to the end of the piece.

    fields = fields + [current]                 # Save the last piece (it has no comma after it).

    if len(fields) != 5:                        # if the piece of record does not have exactly 5 fields.
        raise ValueError(f"Expected 5 fields but found {len(fields)}") #raise a valueError exception

    student_id = fields[0].upper()              # The first field is the ID. upper() makes "st001" the same as "ST001".
    student_name = fields[1]                    # second field is the name.

    if student_id == "":                        # Nothing was between the start of the line and the first comma.
        raise ValueError("Missing student ID")  #then student ID is missing

    if student_name == "":                      # Nothing was between the first and second commas.
        raise ValueError("Missing student name")#then student name is missing

    if student_id in seen_ids:                  # This ID was already accepted earlier. then it's a duplicate
        raise ValueError(f"Duplicate student ID {student_id}")

    subjects = ["Python", "SQL", "Excel"]
    scores = []                                 # The three converted scores will be kept here.

    for i in range(3):                          # i is 0, then 1, then 2: once per subject.
        subject = subjects[i]                   # e.g. "Python" when i is 0.
        score_text = fields[i + 2]              # Scores are pieces 2, 3 and 4.

        try:                                    # int() fails on text like "N/A", so use try.
            score = int(score_text)             # Turn the text "78" into the number 78.
        except ValueError:                      # The text was not a whole number.
            raise ValueError(f"{subject} score '{score_text}' is not a valid number")

        if score < 0 or score > 100:            # Allowed range is 0 to 100 inclusive.
            raise ValueError(f"{student_name} {subject} score is {score}, it has to be between 0 and 100 to become valid")

        scores = scores + [score]               # This score passed every check, so keep it.
    return [student_id, student_name, scores[0], scores[1], scores[2]]   # Hand back the finished student.


# In[6]:


print(validate_record("ST001,Amaka Okafor,78,84,91\n", []))

# In[8]:


def load_students() -> tuple:                   # Returns three values together (a tuple).
    """This reads students.txt line by line and collect the valid records.
    Each line is validated. Invalid lines are logged to errors.log and
    skipped, so one bad record never stops the rest from loading.

    Args:
        None.

    Returns:
        A tuple (students, total_records, invalid_records):
    Raises:
        None. FileNotFoundError and other OSErrors are caught inside the
        function and reported with a message
    """
    students = []
    seen_ids = [] 
    total_records = 0
    invalid_records = 0

    try:
        with open("students.txt", "r") as f:
            for line in f:                      # Go through the file one line at a time.
                total_records += 1              # Count every line, including blank ones.

                try:
                    student = validate_record(line, seen_ids)     # Check the line. Raises ValueError if anything is wrong.

                except ValueError as var:
                    invalid_records += 1  
                    log_error(line.strip(), str(var))     # Record the line and the reason in errors.log.

                else: 
                    students.append(student)            # Keep the student.
                    seen_ids.append(student[0])         # Remember the ID for future duplicate checks.

    except FileNotFoundError:                   # if students.txt does not exist.
        print(f"{"students.txt"} was not found. Choose option 1 to create it.")

    except OSError as ose:
        print(f"Unable to read {"students.txt"}:", ose)

    else:
        print(f"Loaded {len(students)} valid and {invalid_records} invalid records.")

    finally:
        print("Student loading finished.")

    return students, total_records, invalid_records


# In[9]:


def calculate_average(python_score: int, sql_score: int, excel_score: int) -> float: 
    """Calculate the average of a student's three subject scores.

    Args:
        python_score, sql_score and excel_score
    Returns:
        The average score as a floating-point number, rounded to 2 decimal places.
    Raises:
        None. Three validated whole numbers always produce an average.
    """
    average = (python_score + sql_score + excel_score) / 3
    return round(average, 2)


# In[10]:


def calculate_class_average(averages: list) -> float:      # Takes the list of every student's average.
    """This function calculates the class average from a list of student averages.
    Args:
        A list containing the average score of each valid student.
    Returns:
        The class average as a floating-point number rounded to 2 decimal
    Raises:
        A ZeroDivisionError from an empty list
    """
    try: 
        class_average = sum(averages) / len(averages)

    except ZeroDivisionError as zero:             # The list was empty, so len() was 0.
        print(zero)
    else:
        return round(class_average, 2)


# In[11]:


def determine_grade(average: float) -> tuple:   # Takes an average, returns (grade, category).
    """This function converts a student's average into a letter grade and performance category.
    Args: The student's average score.
    Returns:
        A tuple (grade, category), e.g. ("B", "Very Good").
    Raises:
        None because every possible number falls into one of the grade bands.
    """
    if average >= 90:
        return "A", "Excellent"
    elif average >= 80:
        return "B", "Very Good"
    elif average >= 70:
        return "C", "Good"
    elif average >= 60:
        return "D", "Average"
    else:
        return "F", "Needs Improvement"


# In[12]:


def find_student(students: list):
    """Ask the user for a student ID and display that student's full result. The result includes the three scores, 
    the average, the grade and the performance category.
    Args:
        The list of valid student records to search.
    Returns:
        None because the result is just printed to the screen.
    Raises:
        Empty input and missing IDs are handled with messages.
    """
    i = 0                                       # Start at position 0, the first student in the list.

    while i < len(students):                    # Keep going while there are still students left to check.
        student = students[i]                   # Take the student at position i.

        if student[0] == std_id:                # If this student's ID matches.
            average = calculate_average(student[2], student[3], student[4])
            grade, category = determine_grade(average)
            print("\nStudent found!")
            print("Student ID: ", student[0])
            print("Name: ", student[1])
            print("Python score: ", student[2])
            print("SQL score: ", student[3])
            print("Excel score: ", student[4])
            print("Average: ", average)
            print("Grade: ", grade)
            print("Category: ", category)
            return                              # Found them, so stop looking.

        i = i + 1                               # Not this one: move to the next position.

    print(f"No student found with ID {std_id}.")    # Only reached if the loop finished with no match.


# In[13]:


def add_student(students: list):
    """Ask for a new student's details, validate them, then append them to students.txt.
    Args:
        The list of valid student records
    Returns:
        True if the student was validated and saved, otherwise False.
    Raises:
        A ValueError from validation and an OSError from writing the file
    """
    student_id = input("Enter student ID: ")
    student_name = input("Enter student name: ")
    python_score = input("Enter Python score: ")
    sql_score = input("Enter SQL score: ")
    excel_score = input("Enter Excel score: ")

    line = f"{student_id},{student_name},{python_score},{sql_score},{excel_score}" 

    seen_ids = []                               # Collect the IDs that already exist...
    for student in students:
        seen_ids.append(student[0])             # from each current student.

    try:
        new_student = validate_record(line, seen_ids) # use validate_record function to check for correctness and completeness

    except ValueError as var:                   # if validation fails, raise an exception
        print(var)
        log_error(line, str(var))               # Also record it in errors.log.
        return False                            # Nothing was written.

    try:                                        # if validation passed, then append to student.txt
        with open("students.txt", "a") as f:   
            f.write(line + "\n")                # Write the new record

    except OSError as ose:                        # The file could not be written.
        print(ose)
        return False

    else:                                       # Validation passed AND the file was written.
        students.append(new_student)     # Add the converted student to the list in memory as well.
        print("Student added successfully!")
        return True



# In[14]:


def generate_report(students: list, total_records: int, invalid_records: int):
    """Write results_report.txt with every valid student and class record.

    Args: The list of valid student records.
        The total number of records read from students.txt.
        The number of records that were rejected.

    Returns:
        True if the report was written successfully, otherwise False.

    Raises:
        An OSError while writing the report 
    """
    averages = []                               # Each student's average, for the summary.
    highest_average = -1                        # Lower than any real average, so the first student beats it.
    top_student = ""                            # Name of the best student so far.

    try:
        with open("results_report.txt", "w") as f:   # "w" = write: a fresh report every time.
            f.write("STUDENT RESULTS REPORT\n\n")              # Title and a blank line.

            for student in students:            # One line per valid student.
                average = calculate_average(student[2], student[3], student[4])   # Reuse the helper.
                grade, category = determine_grade(average)                        # Reuse the helper.
                averages.append(average)        # Save for the summary.

                if average > highest_average:   # Better than the best so far?
                    highest_average = average   # New best average.
                    top_student = student[1]    # New top student.

                f.write(f"{student[0]}, {student[1]}, Python: {student[2]}, SQL: {student[3]}, "
                        f"Excel: {student[4]}, Average: {average:.2f}, Grade: {grade}, "
                        f"Category: {category}\n")   # ":.2f" always shows 2 decimal places.

            f.write("\nSUMMARY\n")              # Summary heading.
            f.write(f"Total records read: {total_records}\n")
            f.write(f"Valid records: {len(students)}\n")
            f.write(f"Invalid records: {invalid_records}\n")

            if len(averages) > 0:               # Only calculate statistics if there is at least one student.
                f.write(f"Class average: {calculate_class_average(averages):.2f}\n")
                f.write(f"Highest average: {highest_average:.2f}\n")
                f.write(f"Lowest average: {min(averages):.2f}\n")    # min() picks the smallest number.
                f.write(f"Top student: {top_student}\n")
            else:                               # No valid students at all.
                f.write("No valid student records available.\n")

    except OSError as ose:                        # The report could not be written.
        print("Unable to generate report:", ose)
        return False

    else:                                       
        print(f"Report saved to {"results_report.txt"}.")
        return True

    finally:     
        print("Report generation finished.")


def display_menu():
    """Display the main menu options of the Student Records System.
    Args:
        None.
    Returns:
        None. The menu is printed to the screen.
    Raises:
        None.
    """
    print("1. Create/reset sample data")
    print("2. View all students")
    print("3. Search for a student by ID")
    print("4. Add a new student")
    print("5. Generate report")
    print("6. Exit")


# In[ ]:


def main():                            # Runs the whole program.
    """Run the Student Records System until the user chooses Exit.
    Args:
        None.
    Returns:
        None.
    Raises:
        A ValueError from non-numeric menu input, EOFError and KeyboardInterrupt 
    """
    students, total_records, invalid_records = load_students()   # Load once at the start. Empty list if the file is missing; the program still continues.

    while True:                                 # Repeat forever; only "break" ends the loop.
        display_menu()                          # Show the options.

        try:                                    # Protect against non-numbers and Ctrl+C.
            choice = int(input("Enter your choice (1-6): "))    # Text to number; "abc" raises ValueError.

            if choice == 1:                     # Create/reset
                if create_sample_file():        # Reset the file; True if it worked.
                    students, total_records, invalid_records = load_students()   # Reload so the menu uses the fresh data.

            elif choice == 2:                   # View all
                for student in students:        # Go through each valid student.
                    print(student)              # Print the student's list, e.g. ['ST001', 'Chiamaka Nnedi', 78, 84, 91]

            elif choice == 3:                   # Search
                find_student(students)

            elif choice == 4:                   # Add
                if add_student(students):       # True if a student was added.
                    total_records += 1          # One more record in the file.

            elif choice == 5:                   # Report
                generate_report(students, total_records, invalid_records)

            elif choice == 6:                   # Exit
                print("Goodbye!")
                break                           # Leave the loop; the program ends.

            else:                               # A number, but not 1 to 6.
                print("Please choose a number from 1 to 6.")

        except ValueError:                      # Typed something that isn't a whole number.
            print("Invalid input. Please enter a number from 1 to 6.")

if __name__ == "__main__":                      # True only when this file is run directly.
    main()                                      # Start the program.


# In[ ]:





# In[ ]:





# In[ ]:




