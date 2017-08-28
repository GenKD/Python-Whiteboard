'''
    Python Whiteboard
    Made by: Genevieve Duchesneau
    Last Modified on 07/06/2017
    Version 1.0.0


    ToDo:
            Add RGB color picker in place of 4 base colors?
            Add features to unfinished spaces in menu bar.
                (New, Open, Save, Save_As, Print, Properties, Undo, Redo, Cut, Copy, Paste, Delete, Help.)
            Fix Text (currently not working in this iteration).
            Modify text feature to allow text input instead of "Test"
            Fix Line.
            Fix Arc.
            Fix Rectangle.
            Fix Oval.
            Eventually make this a .exe file to install on computers outside of this and run without other programs.

            Notes:

                Good reference for TkInter = http://www.tkdocs.com

                New / Open / Save / Save_As
                -----
                These may not be necessary for this program since it is primarily intended as a whiteboard for my
                Surface.  In doing these I would have to add functionality to modify canvas size, dictact canvas size
                rule (i.e. pixels, cm, inches.) and then add in functionality to zoom in/out on the canvas as well as
                add scroll bars.  This may be unnecessary for this type of program in its current form.


                Undo / Redo
                -----
                These can most likely be solved by pushing every action onto an undo stack first, and limiting stack
                size to something like 20 commands.  if the user clicks undo, then the last item from the stack is first
                copied to the Redo stack and then deleted from the undo stack.  If the user calls redo and (which will
                only be available when the Redo stack has a command saved into it) then the command will be printed to
                the screen, copied to the Undo stack, and deleted from the Redo stack.  Once this is functioning you can
                add in Ctrl + z and Shift + Ctrl + z keyboard commands as well.

                Redo is non functioning with the stack method I currently have in place.
                Undo has issue with recognizing time between mouse down and mouse up as a single line object.  this
                creates large sets of lines. possibly add a feature to Undo so that it will only remove if there is in
                fact an object in the undo_stack.

                Zoom in/out
                -----
                Have not looked into this but when size of canvas is a set variable, this (along with scroll functional-
                ity) will be key in being able to work in single documents with large amounts of notes.

                Eraser
                -----
                May want to look into other ways of working with the eraser since it currently just draws the BG color
                (default = white) over the paint on the screen.  This could be problematic later when the file is in
                constant states of change since it will be adding constant objects to the stack, potentially slowing the
                overall processes in the long term.

                Active color
                -----
                Add active color depression feature so that you can tell which button is active.

                Text Menu
                -----
                Make it so that when the text button is selected it will make a menu appear packed to the right of the
                toolbar which will allow you to choose text options like size, font, etc...
'''

from tkinter import *
import tkinter.font
import tkinter.messagebox


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    undo_stack = []
    # redo_stack = []

    def __init__(self):
        self.root = Tk()
        self.root.title(string='Whiteboard')

        self.top_frame=Frame(self.root)
        self.top_frame.pack(side=TOP, fill=X)

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side=TOP, fill=BOTH)

        self.m = Menu(self.top_frame)
        self.root.config(menu=self.m)

        # ***** Menu ***** #

        self.sub_menu = Menu(self.m)
        self.m.add_cascade(label="File", menu=self.sub_menu)
        self.sub_menu.add_command(label="New", command=self.new_file)
        self.sub_menu.add_command(label="Open", command=self.open_file)
        self.sub_menu.add_command(label="Save", command=self.save_file)
        self.sub_menu.add_command(label="Save as", command=self.save_file_as)
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Print", command=self.print_file)
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Properties", command=self.properties)
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Exit", command=self.application_quit)

        self.edit_menu = Menu(self.m)
        self.m.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_command(label="Delete", command=self.delete)

        self.help_menu = Menu(self.m)
        self.m.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Help", command=self.help_option)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.about)

        # ***** Toolbar ***** #

        self.toolbar = Frame(self.bottom_frame, bg='grey')
        self.toolbar.pack(side=TOP, fill=X)

        self.pen_button = Button(self.toolbar, text='pen', command=self.use_pen)
        self.pen_button.pack(side=LEFT, padx=2, pady=2)

        self.brush_button = Button(self.toolbar, text='brush', command=self.use_brush)
        self.brush_button.pack(side=LEFT, padx=2, pady=2)

        self.text_button = Button(self.toolbar, text='text', command=self.text_draw)
        self.text_button.pack(side=LEFT, padx=2, pady=2)

        self.eraser_button = Button(self.toolbar, text='eraser', command=self.use_eraser)
        self.eraser_button.pack(side=LEFT, padx=2, pady=2)

        self.black_color_button = Button(self.toolbar, bg='black', command=self.color_black)
        self.black_color_button.pack(side=LEFT, padx=2, pady=2)

        self.red_color_button = Button(self.toolbar, bg='red', command=self.color_red)
        self.red_color_button.pack(side=LEFT, padx=2, pady=2)

        self.green_color_button = Button(self.toolbar, bg='green', command=self.color_green)
        self.green_color_button.pack(side=LEFT, padx=2, pady=2)

        self.blue_color_button = Button(self.toolbar, bg='blue', command=self.color_blue)
        self.blue_color_button.pack(side=LEFT, padx=2, pady=2)

        self.choose_size_button = Scale(self.toolbar, from_=1, to=50, orient=HORIZONTAL)
        self.choose_size_button.pack(side=LEFT, padx=2, pady=2)

        self.clean_canvas_button = Button(self.toolbar, text='clear canvas', command=self.canvas_wipe)
        self.clean_canvas_button.pack(side=LEFT, padx=2, pady=2)

        self.undo_button = Button(self.toolbar, text='undo', command=self.undo)
        self.undo_button.pack(side=LEFT, padx=2, pady=2)

        self.undo_10_button = Button(self.toolbar, text='undo 10', command=self.undo10)
        self.undo_10_button.pack(side=LEFT, padx=2, pady=2)

        self.undo_100_button = Button(self.toolbar, text='undo 100', command=self.undo100)
        self.undo_100_button.pack(side=LEFT, padx=2, pady=2)

        # self.redo_button = Button(self.toolbar, text='redo', command=self.redo)
        # self.redo_button.pack(side=LEFT, padx=2, pady=2)

        # ***** Whiteboard ***** #

        self.whiteboard = Frame(self.bottom_frame, bg='grey')

        self.c = Canvas(self.root, bg='white', width=1000, height=1000)
        self.c.pack(fill=BOTH, expand=TRUE, padx=2, pady=2)

        self.setup()
        # start the event loop.
        self.root.mainloop()

    # sets up the initial options and defines your starting parameters.
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    # activates the pen option.
    def use_pen(self):
        self.activate_button(self.pen_button)

    # activates the brush option.
    def use_brush(self):
        self.activate_button(self.brush_button)

    # sets current color to black.
    def color_black(self):
        self.eraser_on = FALSE
        self.color = 'black'

    # sets current color to red.
    def color_red(self):
        self.eraser_on = FALSE
        self.color = 'red'

    # sets current color to green.
    def color_green(self):
        self.eraser_on = FALSE
        self.color = 'green'

    # sets current color to blue.
    def color_blue(self):
        self.eraser_on = FALSE
        self.color = 'blue'

    # "erases" objects by setting current color to white which is the BG color at this time
    # possibly make this actually set to the same color as whatever the BG is set to?
    # find a way to actually "erase".
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    # clears the canvas
    def canvas_wipe(self):
        self.c.delete("all")

    # makes it visually apparent which button's are currently depressed or chosen.
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    # the function to paint a color onto the canvas.
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            # adds the current painted object onto the undo_stack
            self.undo_stack.append(self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=50))
        self.old_x = event.x
        self.old_y = event.y

    # def line_draw(self, event):

    # def arc_draw(self, event):

    # def oval_draw(self, event):

    # def rectangle_draw(self, event):

    # text is not functioning at this time.
    def text_draw(self, event):
        print(tkinter.font.families())
        self.text_font = tkinter.font.Font(family='Helvitica', size=self.choose_size_button.get(), weight='bold')
        event.widget.create_text(self.old_x, self.old_y, fill=self.color, font=self.text_font, text=input())

    # resets the old x and y for the next instance of use.
    def reset(self, event):
        self.old_x, self.old_y = None, None

    # place holder for creating new menu options or buttons.
    def do_nothing(self):
        print("Would Do Something in any other program, but here it prints this.")

    # will create a "new" canvas object
    def new_file(self):
        print("Creates a new document.")

    # will open files as a canvas.
    def open_file(self):
        print("Opens a window to specify which document to open.")

    # will save the current canvas as whatever option the user has already chosen (png, jpeg, etc...)
    def save_file(self):
        # initial save can be with postscript (ps)
        # seems like PIL or imageMagic will be the best choices for this.
        print("Saves the current document.")

    # will allow user to save to a new location or as a new type.
    def save_file_as(self):
        # will call same as above but with a input window to choose the CWD as well as the name.
        print("Opens a window denote how to save the current document.")

    # will print the file.
    def print_file(self):
        # good information on this here ("http://timgolden.me.uk/python/win32_how_do_i/print.html")
        print("Opens the print menu for the current document.")

    # opens the window which allows user to view/set choices for the canvas.
    def properties(self):
        print("Opens a window which will allow you to specify the size of the current canvas in pixels.  Will also"
              "list the last save.")

    # working
    # quit the program.
    def application_quit(self):
        self.root.quit()

    # working
    # remove the last action from the undo_stack.
    def undo(self):
        id = self.undo_stack.pop()
        self.c.delete(id)
        # line below is for adding queue feature for undo/redo when redo is added.
        # self.redo_stack.append(self.c.delete(id))

    # working
    # removes last 10 from stack
    def undo10(self):
        count = 0
        while count < 10:
            id = self.undo_stack.pop()
            self.c.delete(id)
            # line below is for adding queue feature for undo/redo when redo is added.
            # self.redo_stack.append(self.c.delete(id))
            count += 1

    # working
    # removes last 100 from stack.
    def undo100(self):
        count = 0
        while count < 100:
            id = self.undo_stack.pop()
            self.c.delete(id)
            # line below is for adding queue feature for undo/redo when redo is added.
            # self.redo_stack.append(self.c.delete(id))
            count += 1

    # will move an option from the redo to undo stack and place them back on the canvas.
    def redo(self):
        print("Will redo the last action.")
        # self.undo_stack.append(self.c.create_line(self.redo_stack.pop()))

    # will cut the selection from the canvas
    def cut(self):
        print("Will cut the selected section.")

    # will copy the selection from the canvas
    def copy(self):
        print("Will copy the selected section.")

    # will paste the clipboard to the mouse location on the canvas
    def paste(self):
        print("Will paste whatever is in the clipboard.")

    # will delete the selection from the canvas
    def delete(self):
        print("Will delete the selection.")

    # will open the help menu
    def help_option(self):
        print("Will open the help menu.")

    # opens the about messagebox
    def about(self):
        tkinter.messagebox.showinfo('About', 'Python Whiteboard\nMade by: Genevieve Duchesneau\nVersion 1.0.0')

# starts the program
if __name__ == '__main__':
    runningEnvironment = Paint()
