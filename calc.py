# Palden Lhamo
# Introduction to Computer Science: The Way of the Program
# Calculator Final Semester Project

from graphics import *

class Button:
    def __init__(self, win, center, width, height, label):
        # initialize a new button on a window with a center point and dimensions
        # w and h are half the width and height of the button
        w, h = width/2.0, height/2.0
        x, y = center.getX(), center.getY()
        # if w is half the width, then the center point PLUS half the width
        # is the right side, and center MINUS half width is left side
        # any click that is LEFT of the right side, and RIGHT of the left side
        # is on the button
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin) # top left corner of button
        p2 = Point(self.xmax, self.ymax) # bottom right corner
        # rectangle extends from top left to bottom right
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        # give  rect access to the window, so it can draw itself
        self.rect.draw(win)
        # label for this button (5, for example, or +)
        self.label = Text(center, label)
        self.label.setSize(32)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p): # p is the point that the user clicked on
        # return whether the button is active AND the click is between min/max
        # if minimum of x (buttons' mininmum x) is less than the click and the
        # click is less than the button's maximum, that means it's on the button 
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and 
                self.ymin <= p.getY() <= self.ymax)
        # if this is false, then activate can never return true 

    def getLabel(self):
        # return the button label as a string
        return self.label.getText()

    def activate(self):
        # activate by making text black, making rectangle width 1(??),
        # and making self.active true (so the clicked function will know)
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True # if self.active is true, clicked() can return true

    def deactivate(self):
        # if you click on a deactivated button, it returns false (not clicked)
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

class Calculator:
    def __init__(self):
        # sets up the dimensions and size, will call createbuttons and display
        # self. means into the calculator's instance memory rather than a local value
        win = GraphWin("calculator", 800, 600)
        win.setCoords(0, 0, 7, 7) # columns, rows, changed grid to 7 by 7
        win.setBackground("slategray")
        self.win = win
        self.__createButtons()
        self.__createDisplay()
        self.X = 0 # variable X starts with a value of 0

    def __createButtons(self):
        # creates rows and columns, internal calculation by sending values
        # that will later be converted to pixels depending on calculator size
        # for ex. if 20 pixels is a good square, we would multiply by a certain factor
        # like a standard calculator, the button [m+] indicates storing memory,
        #  but on this calculator, it stores into the variable X which can be used in
        #  a formula
        bSpecs = [              (2, 1, '0'), (3, 1, '.'),                           (6, 1, 'm+X'),
                   (1, 2, '1'), (2, 2, '2'), (3, 2, '3'), (4, 2, '+'), (5, 2, '-'), (6, 2, '^'),
                   (1, 3, '4'), (2, 3, '5'), (3, 3, '6'), (4, 3, '*'), (5, 3, '/'), (6, 3, 'pyt'),
                   (1, 4, '7'), (2, 4, '8'), (3, 4, '9'), (4, 4, '<-'), (5, 4, 'C'), (6, 4, 'X')]
        # made a button pyt for Pythagorean theorem
        # made a button ^ for exponent
        self.buttons = []
        for (cx, cy, label) in bSpecs:
            self.buttons.append(Button(self.win, Point(cx, cy), 0.75, 0.75, label))
        self.buttons.append(Button(self.win, Point(4.5, 1), 1.75, 0.75, "="))
        for b in self.buttons:
            b.activate()
                            
    def __createDisplay(self):
        # sets up the output display at the top to show the user the current value
        # white background rectangle
        bg = Rectangle(Point(0.5, 5.5), Point(5.5, 6.5))
        bg.setFill('white')
        bg.draw(self.win)
        
        # currently inputs the values
        text = Text(Point(3, 6), "")
        text.draw(self.win)
        text.setFace("courier")
        text.setStyle("bold")
        text.setSize(32)
        self.display = text

        # last evaluated formula/etc.
        reminder = Text(Point(1.0, 6.35), "=")
        reminder.draw(self.win)
        reminder.setFace("courier")
        reminder.setStyle("bold")
        reminder.setSize(12)
        self.reminder = reminder

        # current value of x, shows user what current stored value of x is
        xval = Text(Point(5.0, 6.35), "x=0")
        xval.draw(self.win)
        xval.setFace("courier")
        xval.setStyle("bold")
        xval.setSize(12)
        self.xval = xval

    def getButton(self):
        # continuously loop to see if a button is clicked, then return
        # the clicked button when it's clicked
        while True:
            p = self.win.getMouse()
            for b in self.buttons:
                if b.clicked(p):
                    # exits the whole method, which causes it to exit the loop
                    return b.getLabel() 
                
    def processButton(self, key):
        # process the clicked button; special handling for certain keys
        text = self.display.getText()
        if key == 'C':
            self.display.setText("")
        elif key == '<-':
            self.display.setText(text[:-1])
        elif key == 'm+X':
            # m+x can only store float values, not formulas
            # try if for anything had a chance not to work at all to avoid the program crashing
            try:
                self.X = float(text)
                self.xval.setText("x=" + str(self.X))
            except:
                pass
        elif key == '=':
            originalFormula = text
            try:
                # to handle exponents:
                # split by hat, join by two stars, replacing all the hats with the
                # double star
                text = "**".join(text.split("^"))
                
                # to handle Pythagorean theorem:
                parts = text.split("pyt") # split the text by p
                # once we've split it, if the list has a length greater than 1,
                #   then that means there is a p in it
                if len(parts) > 1:
                    # 3p4 -> ['3', '4']
                    # '((3)**2+(4)**2)**0.5
                    # take the first number, square it, and add the second term squared,
                    # raise everything to the 1/2 power to square root 
                    text = '((' + parts[0] + ")**2 + (" + parts[1] + ")**2)**0.5"

                # to handle X:
                text = "self.X".join(text.split("X"))

                # let Python evaluate the expression
                print("Evaluating " + text)
                result = eval(text)
            except:
                result = 'ERROR'
            self.display.setText(str(result))
            self.reminder.setText(originalFormula + "=")
        else:
            self.display.setText(text+key)

    def run(self):
        # while loop in getButton will wait until it gets a button,
        # then returns a key, which gets processed; then the whole thing repeats
        while True:
            key = self.getButton()
            self.processButton(key)

if __name__ == '__main__':
    theCalc = Calculator()
    theCalc.run()

