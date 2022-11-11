from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from Helpers import Console
from StudentDB import StudentsDB

menu = ConsoleMenu("Baza studentów", exit_option_text="Zakończ Program")

Database = StudentsDB(menu)

if __name__ == "__main__":
    addStudentOption = FunctionItem("Dodaj studenta", Database.addStudent)
    menu.append_item(addStudentOption)
    removeStudentOption = FunctionItem("Usuń studenta", Database.removeStudent, [])
    menu.append_item(removeStudentOption)
    showStudentsOption = FunctionItem("Wyświetl studentów", Database.showStudents)
    menu.append_item(showStudentsOption)
    saveToFileOption = FunctionItem("Zapisz do pliku", Database.saveToFile)
    menu.append_item(saveToFileOption)
    loadFromFileOption = FunctionItem("Wczytaj z pliku", Database.loadFromFile)
    menu.append_item(loadFromFileOption)

    Console.clear()
    menu.show()
