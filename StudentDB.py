import consolemenu
import csv
from os import path as fsPath
from texttable import Texttable

from Helpers import Console
from Helpers.Student import StudentData


class StudentsDB:
    def __init__(self, menu: consolemenu.console_menu.ConsoleMenu):
        self.students = []
        self.provided = {}
        self.menuRef = menu
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"

    def addStudent(self):
        if len(self.provided) == 0:
            Console.clear()
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"
        if "name" not in self.provided:
            name = input("Podaj imię studenta: ")
            if name == "":
                self.addStudent()
                return
            self.provided["name"] = name
        if "surname" not in self.provided:
            surname = input("Podaj nazwisko studenta: ")
            if surname == "":
                self.addStudent()
                return
            self.provided["surname"] = surname
        if "albumnr" not in self.provided:
            albumnr = input("Podaj numer albumu: ")
            try:
                f = False
                if len([stud for stud in self.students if int(stud.albumnr) == int(albumnr)]) != 0:
                    print(f"Nr albumu {albumnr} ma już przypisanego studenta!")
                    self.addStudent()
                    return
                self.provided["albumnr"] = int(albumnr)
            except ValueError:
                self.addStudent()
                return
        if "grade" not in self.provided:
            grade = input("Podaj ocenę: ")
            try:
                self.provided["grade"] = float(grade)
            except ValueError:
                self.addStudent()
                return
        self.students.append(
            StudentData(len(self.students) + 1, self.provided["name"], self.provided["surname"],
                        self.provided["albumnr"],
                        self.provided["grade"]))
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\n" \
                                f"Sukces: Dodano studenta {self.provided['name']} {self.provided['surname']} nr alb. {self.provided['albumnr']} do bazy studentów."
        self.provided.clear()
        Console.clear()
        pass

    def removeStudent(self, tablePrinted: bool = False):
        if not tablePrinted:
            Console.clear()
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"
        if len(self.students) == 0:
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Brak studentów w bazie danych."
            return

        if not tablePrinted:
            table = Texttable()
            table.set_cols_align(["c", "c", "c", "c", "c", ])
            values = [["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"]]
            for student in self.students:
                values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
            table.add_rows(values)
            print(table.draw())

        prov = input("Wpisz identyfikator studenta którego chcesz usunąć z bazy: ")
        try:
            studentId = int(prov)
            searchArr = [stud for stud in self.students if int(stud.id) == int(studentId)]
            if len(searchArr) == 0:
                print(f"ERROR: Nie znany identyfikator: {studentId}.")
                self.removeStudent(True)
                return
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students) - 1}\nSukces: Usunięto studenta {searchArr[0].name} {searchArr[0].surname} nr alb.: {searchArr[0].albumnr}."
            self.students.remove(searchArr[0])
            Console.clear()
            return

        except ValueError:
            self.removeStudent(True)
            return
        pass

    def showStudents(self):
        Console.clear()
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"
        if len(self.students) == 0:
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Brak studentów w bazie danych."
            return
        print("1. Id\n2. Imie\n3. Nazwisko\n4. Nr albumu\n5. Ocena\n6. Wróć do menu.")
        imp = input("Wybierz kolumne wg której mają być posortowani studenci: ")
        try:
            selection = int(imp)
            if selection not in [1, 2, 3, 4, 5, 6]:
                print("ERROR: Wybierz prawidłową kolumnę.")
                self.showStudents()
                return
            table = Texttable()
            table.set_cols_align(["c", "c", "c", "c", "c", ])
            values = [["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"]]
            Console.clear()
            if selection == 6:
                return
            elif selection == 1:
                for student in self.students:
                    values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
                table.add_rows(values)
                print(table.draw())
            else:
                sortedArr = []
                if selection == 2:
                    sortedArr = sorted(self.students, key=lambda student: student.name)
                elif selection == 3:
                    sortedArr = sorted(self.students, key=lambda student: student.surname)
                elif selection == 4:
                    sortedArr = sorted(self.students, key=lambda student: student.albumnr)
                elif selection == 5:
                    sortedArr = sorted(self.students, key=lambda student: student.grade)
                for student in sortedArr:
                    values.append([student.id, student.name, student.surname, student.albumnr, student.grade])
                table.add_rows(values)
                print(table.draw())
        except ValueError:
            self.showStudents()
            return
        input("\nWciśnij ENTER by wrócić do menu.")
        Console.clear()
        pass

    def saveToFile(self):
        Console.clear()
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"
        if len(self.students) == 0:
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Brak studentów w bazie danych."
            return
        path = input("Wpisz ścieszkę na której ma być zapisany plik: \n\t")
        if not fsPath.exists(path):
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Podana ścieszka nie istnieje ({path})."
            return
        fileName = input(
            "Wpisz nazwę pliku bez rozszerzenia do którego ma być zapisana baza danych (np. \"baza_studenci\"): \n\t")
        filePath = fsPath.join(path, fileName + ".csv")

        fileAlreadyExists = fsPath.exists(filePath)
        file = open(filePath, 'w', encoding="UTF8")
        dataWriter = csv.writer(file)
        dataWriter.writerow(["Id", "Imie", "Nazwisko", "Nr albumu", "Ocena"])
        data = []
        for student in self.students:
            data.append([student.id, student.name, student.surname, student.albumnr, student.grade])
        dataWriter.writerows(data)
        subtitleText = f"Aktualna ilość studentów w bazie: {len(self.students)}\nSukces: %ActionType% baze danych w pliku {fsPath.join(path, fileName + '.csv')}!"
        if fileAlreadyExists:
            subtitleText = subtitleText.replace("%ActionType%", "Nadpisano")
        else:
            subtitleText = subtitleText.replace("%ActionType%", "Zapisano")
        self.menuRef.subtitle = subtitleText
        Console.clear()
        pass

    def loadFromFile(self):
        Console.clear()
        self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}"
        path = input("Podaj ścieszkę do pliku z bazą danych: \n\t")
        if not fsPath.exists(path):
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Podana ścieszka nie istnieje ({path})."
            return
        if path.split(fsPath.extsep)[1] != "csv":
            self.menuRef.subtitle = f"Aktualna ilość studentów w bazie: {len(self.students)}\nERROR: Nie obsługiwane rozszerzenie pliku ({path})."
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
                self.menuRef.subtitle = ("\n".join(t)).replace("%arrLen%", str(len(self.students)))
                Console.clear()
                return
            idexists = (len([stud for stud in self.students if int(stud.id) == int(data[0])]) != 0)
            albumnrexists = (len([stud for stud in self.students if int(stud.albumnr) == int(data[3])]) != 0)
            if albumnrexists:
                subtitleText += f"\nUwaga: Nr albumu {data[3]} jest juz przypisany do studenta (Podczas próby wpisania: {data[1]} {data[2]} nr alb.: {data[3]})! "
                soft_problems += 1
                continue
            if idexists:
                self.students.append(StudentData(len(self.students) + 1, data[1], data[2], data[3], data[4]))
                subtitleText += f"\nUwaga: Student {data[1]} {data[2]} nr alb.: {data[3]} został dodany z nowym id ({len(self.students)}) "
                soft_problems += 1
            if not idexists and not albumnrexists:
                self.students.append(StudentData(int(data[0]), data[1], data[2], int(data[3]), float(data[4])))
        self.menuRef.subtitle = subtitleText.replace("%arrLen%", str(len(self.students))) \
            .replace("%totalProblems%", str(soft_problems + crit_problems)) \
            .replace("%critProblems%", str(crit_problems))
        pass
    