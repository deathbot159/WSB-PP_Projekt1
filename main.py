from os import system, name as osName, path as fsPath
import csv

from Helpers.Student import *

from consolemenu import *
from consolemenu.items import *
from texttable import *

students = []
provided = {}

# Global menu
menu = ConsoleMenu("Baza studentów", f"Aktualna ilość studentów w bazie: {len(students)}",
                   exit_option_text="Zakończ program")


def cClear():
    if osName == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    pass


def addStudent():
    if len(provided) == 0:
        cClear()
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    if "name" not in provided:
        name = input("Podaj imię studenta: ")
        if name == "":
            addStudent()
            return
        provided["name"] = name
    if "surname" not in provided:
        surname = input("Podaj nazwisko studenta: ")
        if surname == "":
            addStudent()
            return
        provided["surname"] = surname
    if "albumnr" not in provided:
        albumnr = input("Podaj numer albumu: ")
        try:
            for student in students:
                if int(albumnr) == int(student.albumnr):
                    print(f"Nr albumu {albumnr} jest już przypisany do studenta {student.name} {student.surname}!")
                    addStudent()
                    return
            provided["albumnr"] = int(albumnr)
        except ValueError:
            addStudent()
            return
    if "grade" not in provided:
        grade = input("Podaj ocenę: ")
        try:
            provided["grade"] = float(grade)
        except ValueError:
            addStudent()
            return
    students.append(
        StudentData(len(students) + 1, provided["name"], provided["surname"], provided["albumnr"], provided["grade"]))
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    provided.clear()
    cClear()
    pass


def removeStudent(tablePrinted: bool = False):
    if not tablePrinted:
        cClear()
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    if len(students) == 0:
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Brak studentów w bazie danych."
        return

    if not tablePrinted:
        table = Texttable()
        table.set_cols_align(["c", "c", "c", "c", "c", ])
        values = [["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"]]
        for student in students:
            values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
        table.add_rows(values)
        print(table.draw())

    prov = input("Wpisz identyfikator studenta którego chcesz usunąć z bazy: ")
    try:
        studentId = int(prov)
        found = 0
        for student in students:
            if int(student.id) == studentId:
                found = 1
                break
        if not found:
            print(f"ERROR: Nie znany identyfikator: {studentId}.")
            removeStudent(True)
            return
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students) - 1}\nSukces: Usunięto studenta {student.name} {student.surname} nr alb.: {student.albumnr}."
        students.remove(student)
        cClear()
        return

    except ValueError:
        removeStudent(True)
        return
    pass


def showStudents():
    cClear()
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    if len(students) == 0:
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Brak studentów w bazie danych."
        return
    print("1. Id\n2. Imie\n3. Nazwisko\n4. Nr albumu\n5. Ocena\n6. Wróć do menu.")
    imp = input("Wybierz kolumne wg której mają być posortowani studenci: ")
    try:
        selection = int(imp)
        if selection not in [1, 2, 3, 4, 5, 6]:
            print("ERROR: Wybierz prawidłową kolumnę.")
            showStudents()
            return
        table = Texttable()
        table.set_cols_align(["c", "c", "c", "c", "c", ])
        values = [["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"]]
        cClear()
        if selection == 6:
            return
        elif selection == 1:
            for student in students:
                values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
            table.add_rows(values)
            print(table.draw())
        else:
            sortedArr = []
            if selection == 2:
                sortedArr = sorted(students, key=lambda student: student.name)
            elif selection == 3:
                sortedArr = sorted(students, key=lambda student: student.surname)
            elif selection == 4:
                sortedArr = sorted(students, key=lambda student: student.albumnr)
            elif selection == 5:
                sortedArr = sorted(students, key=lambda student: student.grade)
            for student in sortedArr:
                values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
            table.add_rows(values)
            print(table.draw())
    except ValueError:
        showStudents()
        return
    input("\nWciśnij ENTER by wrócić do menu.")
    cClear()
    pass


def saveToFile():
    cClear()
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    if len(students) == 0:
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Brak studentów w bazie danych."
        return
    path = input("Wpisz ścieszkę na której ma być zapisany plik: \n\t")
    if not fsPath.exists(path):
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Podana ścieszka nie istnieje ({path})."
        return
    fileName = input(
        "Wpisz nazwę pliku bez rozszerzenia do którego ma być zapisana baza danych (np. \"baza_studenci\"): \n\t")
    filePath = fsPath.join(path, fileName + ".csv")

    fileAlreadyExists = fsPath.exists(filePath)
    file = open(filePath, 'w', encoding="UTF8")
    dataWriter = csv.writer(file)
    dataWriter.writerow(["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"])
    data = []
    for student in students:
        data.append([student.id, student.name, student.surname, student.albumnr, student.grade])
    dataWriter.writerows(data)
    subtitleText = f"Aktualna ilość studentów w bazie: {len(students)}\nSukces: %ActionType% baze danych w pliku {fsPath.join(path, fileName + '.csv')}!"
    if fileAlreadyExists:
        subtitleText = subtitleText.replace("%ActionType%", "Nadpisano")
    else:
        subtitleText = subtitleText.replace("%ActionType%", "Zapisano")
    menu.subtitle = subtitleText
    cClear()
    pass


def loadFromFile():
    cClear()
    menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}"
    path = input("Podaj ścieszkę do pliku z bazą danych: \n\t")
    if not fsPath.exists(path):
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Podana ścieszka nie istnieje ({path})."
        return
    if path.split(fsPath.extsep)[1] != "csv":
        menu.subtitle = f"Aktualna ilość studentów w bazie: {len(students)}\nERROR: Nie obsługiwane rozszerzenie pliku ({path})."
        return
    file = open(path, "r", encoding="UTF8")
    dataReader = csv.reader(file)
    next(dataReader)
    soft_problems = 0
    crit_problems = 0
    subtitleText = f"Aktualna ilość studentów w bazie: %arrLen%\nSukces: Dodano studentów z pliku. Liczba " \
                   f"problemów: %totalProblems% w tym %critProblems% krytycznych. "
    for data in dataReader:
        if not data:
            continue
        if len(data) != 5:
            crit_problems += 1
            continue
        try:
            int(data[0])
            int(data[3])
            float(data[4])
        except ValueError:
            t = subtitleText.split("\n")
            t.pop()
            t.append(f"Nie prawidłowe wartości w wierszu ({','.join(data)})")
            menu.subtitle = ("\n".join(t)).replace("%arrLen%", str(len(students)))
            cClear()
            return
        idexists = (len([stud for stud in students if int(stud.id) == int(data[0])]) != 0)
        albumnrexists = (len([stud for stud in students if int(stud.albumnr) == int(data[3])]) != 0)
        if albumnrexists:
            subtitleText += f"\nUwaga: Nr albumu {data[3]} jest juz przypisany do studenta (Podczas próby wpisania: {data[1]} {data[2]} nr alb.: {data[3]})! "
            soft_problems += 1
            continue
        if idexists:
            students.append(StudentData(len(students) + 1, data[1], data[2], data[3], data[4]))
            subtitleText += f"\nUwaga: Student {data[1]} {data[2]} nr alb.: {data[3]} został dodany z nowym id ({len(students)}) "
            soft_problems += 1
        if not idexists and not albumnrexists:
            students.append(StudentData(int(data[0]), data[1], data[2], int(data[3]), float(data[4])))
    menu.subtitle = subtitleText.replace("%arrLen%", str(len(students))) \
        .replace("%totalProblems%", str(soft_problems + crit_problems)) \
        .replace("%critProblems%", str(crit_problems))
    pass


if __name__ == "__main__":
    addStudentOption = FunctionItem("Dodaj studenta", addStudent)
    menu.append_item(addStudentOption)
    removeStudentOption = FunctionItem("Usuń studenta", removeStudent, [])
    menu.append_item(removeStudentOption)
    showStudentsOption = FunctionItem("Wyświetl studentów", showStudents)
    menu.append_item(showStudentsOption)
    saveToFileOption = FunctionItem("Zapisz do pliku", saveToFile)
    menu.append_item(saveToFileOption)
    loadFromFileOption = FunctionItem("Wczytaj z pliku", loadFromFile)
    menu.append_item(loadFromFileOption)

    cClear()
    menu.show()
