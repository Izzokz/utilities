import os

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from mod.file_man import search

class Textfile:

    """Textfile modifier and interpreter
    WARNING : ITS DATABASES STYLE IS CASE SENSITIVE
    Example of use: file = Textfile('file.txt', create = 'y', 'logfile.txt', type_log = 'error')
    Special argument: create: 'y' or 'n' (if the file doesn't exist and create == 'y', it will create the file, else, an error appears)
    Arguments : Name of the file (.txt, .json, .py, etc.), Name of the logfile (optional)
    The last argument is the type of the logfile construction (optional) :
        'info' if every single action has to be noted
        'error' (default) to warn when problems occur
    BEWARE : pickvarval and pickconstval support tuples and lists but not composed or complex types like tables
    Utilities: -file.const_() -> {'CONSTANT': '9', 'CONST': '10', 'CONST_': 'True', 'CONSTX': ''}
               -file.pickconstval('CONSTANT') -> 9
               -file.classes() -> ['Class1', 'Klass(Classs)', 'Classs']
               -file.class_names() -> ['Class1', 'Klass', 'Classs'] (without inheritance arguments)
               -file.create_var('any_variable', 'anything(str, int, float, list...)') -> appends 'anyvariable = anything(str, int, float, list...)' to the Textfile
               -file.create_var_list(list) -> appends elements of the list if these verify the condition of variables (variable = value)
               -file.add(list or str) -> appends every element of the list to the Textfile using line breaks or only one line if the argument isn't a list
               -file.pickvarval('variable') -> returns the value of the variable
               -file.lines() -> determinates the total number of lines in the file
               -file.is_line(line_n) -> returns True if the line number <line_n> exists, False if it doesn't
               -file.changeline(line_number, 'content') -> changes the content of the line <line_number> by <'content'>
               -file.delete_line(line_number) -> deletes the line number <line_number>
               -file.delete_lines(from, to) -> deletes the lines number <from> to number <to>
                    -file.delete_lines(from) -> deletes every line since the line number <from>
               -file.changevarval('variable', 'anything(str, int, float, list...)') -> changes the value of the variable by 'anything(str, int, float, list...)'
               -file.resetlog() -> resets the logfile"""

    def __init__(self, filename: str, create: str = 'n', log_file: str = None, type_log: str = 'error'):
        self.name = search(filename, create = create)
        
        if self.name == None:
            if create == 'y':
                self.name = search(filename)
            else:
                raise Exception("The file doesn't exist, use the parameter (create = 'y') to create it.")
            
        self.log = Log(log_file)
        if type_log == 'info':
            self.type_log = 'info'
        else:
            self.type_log = 'error'
        try:
            with open(self.name) as none:
                pass
        except:
            pass
    
    def kill(self):
        return None
    
    def rename(self, title: str):
        for char in title:
            if char in '\/:*?|<>"':
                raise ValueError('Forbidden characters for files : \ / : * ? | < > "')
        #adds path to title
        os.rename(self.name, title)
        return None

    def const_(self):

        """Returns the name of every CONSTANT in a dict"""

        with open(self.name, 'r') as file:
            return dict((line.split()[0], self.fix_value(" ".join(line.split()[2:]))) for line in file if len(line.split()) > 2 if line.split()[0].isupper() if line.split()[1] == '=')
    
    def pickconstval(self, const: str):

        """Returns the value of the CONSTANT using the const_() method"""

        if const in self.const_():
            return self.const_()[const]
        return None

    def create_var(self, var: str, value):

        """Creates a new line adding the variable and its value
            file.create_var('var', value) -> 'var' = value"""

        with open(self.name, 'a') as file:
            file.write(f"{var} = {value}\n")
            if self.type_log == 'info':
                self.log.info(f"A new variable has been added :\n   {var} = {value}")
        return None

    def create_var_list(self, var_list: list):

        """Adds lines of variable in a list if the syntax is correct
            Correct syntax: ["var1 = 1", "var2 = 2", "var3 = 3"]
                >>> var1 = 1
                >>> var2 = 2
                >>> var3 = 3
            Incorrect syntax: ["var1 = 1", "var2, 2", "var3 = 3"]
                >>> var1 = 1
                (log) : +----------------|ERROR|----------------+
                        'var2,' isn't a variable, the line hasn't been added
                          correct syntax: variable = value
                        +----------------|ERROR|----------------+
                >>> var3 = 3"""

        with open(self.name, 'a') as file:
            for var in var_list:
                if len(var.split()) >= 3 and var.split()[1] == '=':
                    file.write(f"{var}\n")
                    if self.type_log == 'info':
                        self.log.info(f"A variable has been added:\n   {var}")
                else:
                    self.log.error(f"'{var.split()[0]}' isn't a variable, the line hasn't been added\n  correct syntax: variable = value")
        return None
    
    def add(self, line_list):

        """Adds lines from the line_list, no restriction
        (NEW) Just appends one line if line_list is actually a string"""

        if type(line_list) == str:
            with open(self.name, 'a') as file:
                file.write(f"{line_list}\n")
                return None
        
        with open(self.name, 'a') as file:
            for line in line_list:
                file.write(f"{line}\n")
                if self.type_log == 'info':
                    self.log.info(f"A new line has been added:\n    {line}")
        return None

    def classes(self):

        """Determinates the classes available returned into a list"""

        with open(self.name, 'r') as file:
            return [
                "".join([letter for letter in iter(lambda x = iter(line.split()[n]): next(x), ':') if letter.isalnum() or letter == '(' or letter == ')'])
                for line in file
                for n in range(len(line.split()))
                if len(line.split()) > 0
                and line.split()[n].istitle()
                ]
    
    def class_names(self):

        """Determinates the classes available (without inheritance arguments) returned into a list"""

        with open(self.name, 'r') as file:
            return [
                "".join([letter for letter in iter(lambda x = iter(line.split()[n]): next(x), '(') if letter.isalnum()])
                for line in file
                for n in range(len(line.split()))
                if len(line.split()) > 0
                and line.split()[n].istitle()
                ]
    
    def delete(self):

        """Delete the whole content of the file"""

        with open(self.name, 'w') as file_to_delete:
            file_to_delete.write('')
            if self.type_log == 'info':
                self.log.info(f"The file <{self.name}> has been reset")
        return None
    
    def pickvarval(self, var: str):

        """Pick up the value of the variable mentionned
        Very useful when variables are stocked in a .txt file for example
        file.pickvarval('var1') -> 1
            Correct syntax in the textfile: var1 = 1
            Incorrect syntax in the textfile: var1 1"""

        with open(self.name, 'r') as file:
            for line in file:
                if len(line.split()) > 2:
                    if line.split()[0] == var and line.split()[1] == '=':
                        value = " ".join(line.split()[2:])
                        return self.fix_value(value)
        return None
    
    def lines(self):

        """Returns the number of lines used in the file"""

        number_of_lines = 0
        with open(self.name, 'r') as file:
            for line in file:
                number_of_lines += 1
        return number_of_lines
    
    def is_line(self, line_n: int):

        """Verifies if the line number <line_n> exists
        Returns True if it exists, False if it doesn't"""

        if type(line_n) != int or line_n > self.lines() or line_n <= 0:
            return False
        return True
    
    def changeline(self, line_n: int, content):

        """Changes the line number <line_n> into <content> if the line exists"""

        if not self.is_line(line_n):
            self.log.error(f"No line has been changed")
            return None
        lines = []
        current_line = 0
        with open(self.name, 'r') as updating_file:
            for line in updating_file:
                current_line += 1
                if current_line != line_n:
                    lines.append(line)
                else:
                    old_line = line
                    lines.append(f"{content}\n")
        with open(self.name, 'w') as rewrite:
            rewrite.writelines(lines)
            if self.type_log == 'info':
                self.log.info(f"The line {line_n} has been changed:\n   from {old_line}   to {content}")
        return None

    def delete_line(self, line_n):

        """Deletes the line number <line_n> if it exists"""

        if not self.is_line(line_n):
            self.log.error(f"No line has been deleted")
            return None
        lines = []
        current_line = 0
        with open(self.name, 'r') as updating_file:
            for line in updating_file:
                current_line += 1
                if current_line != line_n:
                    lines.append(line)
                else:
                    old_line = line
        with open(self.name, 'w') as rewrite:
            rewrite.writelines(lines)
            if self.type_log == 'info':
                self.log.info(f"The line {line_n} ({old_line[:-1]}) has been deleted")
        return None
    
    def delete_lines(self, from_: int, to: int = -1):

        """Deletes lines number <from_> to number <to> if they exist
        Uses: -file.delete_lines(55, 65) -> deletes lines 55, 56, 57... 65
              -file.delete_lines(55) -> deletes lines 55, 56, 57... last line"""

        if to == -1:
            to = self.lines()
        for nothing in range(from_, to + 1):
            self.delete_line(from_)
        return None
    
    def changevarval(self, varname: str, value):

        """Changes the value of the variable <varname> if the syntax is correct
        Very useful when you need to change a variable in a .txt or .py file when the file isn't executing

        file.changevarval(varname, 89) -> varname = None => varname = 89"""

        if varname.isupper():
            self.log.error(f"{varname} is literally a CONSTANT, no change can be done")
            return None
        current_line = 0
        with open(self.name, 'r') as updating_file:
            for line in updating_file:
                current_line += 1
                if len(line.split()) >= 3:
                    if line.split()[0] == varname:
                        if line.split()[1] == '=':
                            return self.changeline(current_line, f"{varname} = {value}")
                        else:
                            self.log.error(f"{line} isn't interpreted as a variable, no change done\n    correct syntax: variable = value")
        self.log.error(f"No variable named '{varname}' has been found")
        return None
    
    def resetlog(self):

        """Resets the logfile"""

        return self.log.reset()

    def fix_value(self, value):

        if value[0] == '[' and value[-1] == ']':
            return [self.fix_value(element[1:-1]) if element[0] == ',' and element[-1] == ',' else self.fix_value(element[:-1]) if element[-1] == ',' else self.fix_value(element[1:]) if element[0] == ',' else self.fix_value(element) for element in value[1:-1].split() if element != ',']
        elif value[0] == '(' and value[-1] == ')':
            return tuple(self.fix_value(element[1:-1]) if element[0] == ',' and element[-1] == ',' else self.fix_value(element[:-1]) if element[-1] == ',' else self.fix_value(element[1:]) if element[0] == ',' else self.fix_value(element) for element in value[1:-1].split() if element != ',')
        if value == 'None':
            return None
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        elif isnumber(value):
            return int(value)
        elif (value[0] == '"' and value[-1] == '"') or (value[0] == f"'" and value[-1] == f"'"):
            return value[1:-1]
        elif isfloat(value):
            return float(value)
        return self.fix_value(value)
    
def isfloat(value): #Also accepts negative numbers

    """The float version of .isnumeric() and also accepts negative sign ONLY if it's the first character"""

    value = negative_pass(value)
    point = 0
    index = 0
    for char in value:
        if char == '.':
            point += 1
        elif not char.isdecimal():
            return False
        if point > 1:
            return False
        index += 1
    return True

def isnumber(value): #Accepts negative numbers

    """Acts like .isnumeric() but also accepts negative sign ONLY if it's the first character"""
    
    value = negative_pass(value)
    for char in value:
        if not char.isnumeric():
            return False
    return True

def isflint(value): #float or integer

    """Returns True if the string can become an integer or a float
    isflint('-.556') -> True
    isflint('-999') -> True"""

    if isfloat(value) or isnumber(value):
        return True
    return False

def typeflint(value):

    """Return True if value is an integer or a float
    Admits negative numbers and strings aren't allowed"""

    return negative_pass(value, 'no')

def negative_pass(value, string_mode = 'yes'): #Returns the value as its string form to let other methods treat the case or False if the value isn't a string, nor a float or an integer.

    """Used in isnumber() and isfloat() methods to let negative numbers be what they are
    '-55'.isnumeric() -> False
    isnumber('-55') -> True
    isfloat('-.999') -> True"""

    if string_mode == 'no':
        if type(value) != int and type(value) != float:
            return False
        else:
            return isflint(value)

    if type(value) != str:
        if type(value) == int or type(value) == float:
            value = str(value)
        else:
            return False
    elif len(value) == 0:
        return False
    if value[0] == '-':
        value = value[1:]
    return value

class Log:

    """Log is a small module used by Textfile to generate logs if a logfile is saved
    Utilities: -log.info(info) -> verifies if a log has been entered and execute log.write(info) if True
               -log.write(info) -> generates a log
               -log.error(error) -> verifies if a log has been entered and execute log.write_error(error) if True
               -log.write_error(error) -> generates an highlighted log
               -log.reset() -> resets the logfile
    (Beware : notes every single edit if no condition has been manually entered)"""

    def __init__(self, log: str):
        self.log = log
    
    def info(self, info: str):
        if self.log != None:
            return self.write(info)
        else:
            return None
    
    def error(self, error: str):
        if self.log != None:
            return self.write_error(error)
        else:
            return None
    
    def write_error(self, error: str):
        with open(self.log, 'a') as log:
            log.write(f"+----------------|ERROR|----------------+\n{error}\n+----------------|ERROR|----------------+\n")
        return None
    
    def write(self, info: str):
        with open(self.log, 'a') as log:
            log.write(f"{info}\n")
        return None

    def reset(self):
        if self.log != None:
            with open(self.log, 'w') as reset:
                reset.write("")
        return None

# a = Textfile('test.txt')