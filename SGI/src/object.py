from form import Form
from viewport import Viewport

class Object():
    def __init__(self, viewport: Viewport) -> None:
        self.viewport = viewport

    def confirm_button(self):
        form = self.form_setup()
        self.viewport.objectList.append(form)
        self.viewport.draw(form)
        self.mainWindow.objList.addItem(form.name + ': ' + str(form.id))

    def form_setup(self) -> Form:
        coordinatesList = list()
        plaintext = self.coordinates_tab.text()
        if (self.check(plaintext)):
            coordinates = plaintext.split(';')
            for coordinate in coordinates:
                coordinate = coordinate.replace("(", "")
                coordinate = coordinate.replace(")", "")
                xy = coordinate.split(',')
                x = int(xy[0])
                y = int(xy[1])
                coordinatesList.append((x,y))
            form = Form(self.name.text(), coordinatesList, len(self.viewport.objectList))
            return form

    def check(self, plaintext):
        stack = []
        prev = ''
        for char in plaintext:
            if len(stack) > 0:
               prev = stack.pop()
            if not (self.isOperator(char) or char.isnumeric()):
                return False
            stack.append(char)
            if prev == '(' and ((not char.isnumeric()) and char != '-'):
                print(2)
                return False
            if prev == ')' and char != ';':
                return False
            if prev == '-' and (char == '(' or char == ')'):
                return False
        return True

    def isOperator(self, char):
        if (char == '(' or char == ')' or char == ',' or char == ';' or char == '-'):
            return True
        return False
