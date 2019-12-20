#=============================================================================#
# import from external libraries                                              #
#=============================================================================#

import argparse
import numpy as np
import pandas as pd
import pickle

#=============================================================================#
# import from djak suite                                                      #
#=============================================================================#

#=============================================================================#
# import from internal modules                                                #
#=============================================================================#

from config import defaults

#=============================================================================#
# global functions                                                            #
#=============================================================================#

#=============================================================================#
# class definition                                                            #
#=============================================================================#

class basic:
    def __init__(self):
        self.__dict__.update(state)

class util:

    #=========================================================================#
    # constructor                                                             #
    #=========================================================================#

    def __init__(self, *args, **kwargs):
        # set attributes with default dictionary from config.py and key-word dictionary
        defaults.update(kwargs)
        self.__dict__.update(defaults)
        # set attributes from command-line input
        NotImplemented

    #=========================================================================#
    # public - defined                                                        #
    #=========================================================================#

    def findme(self):
        NotImplemented

    def loadme(self, filename, **kwargs):
        # extract name and extension from filename
        name, ext = os.path.splitext(filename)
        # construct alias for desired load method
        func = f"self.__loadme__{ext[1:]}__"
        # return the loaded object
        obj = func(filename, **kwargs)
        return obj

    def printme(self, *args, **kwargs):
        #---------------------------------------------------------------------#
        # set variables                                                       #
        #---------------------------------------------------------------------#
        tabs = kwargs['tabs'] if 'tabs' in kwargs else 0
        output = kwargs['output'] if 'output' in kwargs else False
        #---------------------------------------------------------------------#
        # collect lines                                                       #
        #---------------------------------------------------------------------#
        # set up container to hold lines
        lines = []
        for arg in args:
            # if input is tuple, parse object to print and other commands from tuple
            if isinstance(arg, tuple):
                if len(arg) == 1:
                    header, message = False, None
                    x = arg[0]
                elif len(arg) == 2:
                    header = False
                    message, x = arg
                elif len(arg) == 3:
                    header, message, x = arg
                # collect lines if header/message is present
                if message != None:
                    if header:
                        lines.extend(self.__printme__header__(message, tabs))
                    else:
                        lines.extend(self.__printme__string__(message, tabs))
                    lines.extend(self.__printme__controller__(x, tabs+1))
            # if input is not a tuple, take input as opbject, x, to print
            else:
                x = arg
                lines.extend(self.__printme__controller__(x, tabs))
        #---------------------------------------------------------------------#
        # process lines                                                       #
        #---------------------------------------------------------------------#
        # return list of lines if output selected
        if output:
            return lines
        # otherwise print each line to command line
        else:
            for line in lines: print(line)

    def saveme(self, filename, obj, **kwargs):
        # extract name and extension from filename
        name, ext = os.path.splitext(filename)
        # construct alias for desired save method
        func = f"self__saveme__{ext[1:]}__"
        # return the loaded object
        obj = func(filename, obj)
        return obj

    def writeme(self, filename, *args, **kwargs):
        # set variables with key word arguments
        write = kwargs['write'] if 'wirte' in kwargs else 'w'
        # enforce output when kwargs fed to printme()
        kwargs['output'] = True
        # extract lines from printme()
        lines = self.printme(*args, **kwargs)
        # make a single string of text
        lines = "\n".join(lines)
        with open(filename, write): as f:
            f.writelines(lines)

    #=========================================================================#
    # public - declared only                                                  #
    #=========================================================================#

    #=========================================================================#
    # "protected" - defined                                                   #
    #=========================================================================#

    #=========================================================================#
    # "protected" - declared only                                             #
    #=========================================================================#

    #=========================================================================#
    # "private" - defined                                                     #
    #=========================================================================#

    @staticmethod
    def __loadme__csv__(filename, **kwargs):
        obj = pd.read_csv(filename, **kwargs)
        return obj

    @staticmethod
    def __loadme__npy__(filename, **kwargs):
        obj = np.load(filename, **kwargs)
        return obj

    @staticmethod
    def __loadme__pkl__(filename, **kwargs):
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        return obj

    @staticmethod
    def __loadme__py__(filename, **kwargs):
        name, ext = os.path.splitext(filename)
        exec(f"import {name} as obj")
        obj = basic(obj.__dict__)
        return obj

    @staticmethod
    def __loadme__txt__(filename, **kwargs):
        with open(filename, 'r') as f:
            obj = f.readlines()
        obj = [x.rstrip('\n') for x in obj]
        return obj

    def __printme__controller__(self, x, tabs):
        if isinstance(x, pd.core.frame.DataFrame):
            lines = self.__printme__dataframe__(x, tabs)
        elif isinstance(x, dict):
            lines = self.__printme__dict__(x, tabs)
        elif isinstance(x, list):
            lines = self.__printme__list__(x, tabs)
        elif isinstance(x, (str, int, float)):
            lines = self.__printme__string__(x, tabs)
        else:
            print(f"{type(x)} not found")
        return lines

    def __printme__dataframe__(self, x, tabs):
        NotImplemented

    def __printme__dict__(self, x, tabs):
        lines = []
        for key, value in x.items():
            lines.extend(self.printme(key, tabs=tabs, output=True))
            lines.extend(self.printme(value, tabs=tabs+1, output=True))
        return lines

    def __printme__header__(self, x, tabs):
        tabSpace = self.__printme__tabSpace__(tabs)
        decorator = tabSpace + "".join(["=" for _ in range(72 - len(tabSpace))])
        lines = ["", decorator, f"{tabSpace}{x}", decorator, ""]
        return lines

    def __printme__list__(self, x, tabs):
        tabSpace = self.__printme__tabSpace__(tabs)
        lines = [f"{tabSpace}{x1}" for x1 in x]
        return lines

    def __printme__string__(self, x, tabs):
        tabSpace = self.__printme__tabSpace__(tabs)
        lines = [f"{tabSpace}{x}"]
        return lines

    def __printme__tabSpace__(self, tabs):
        return "".join([" " for _ in range(tabs*self.__tab_pad__)])

    def __saveme__csv__(self, filename, obj, **kwargs):
        # make sure obj is a DataFrame
        self.__saveme__assert_message__(filename, obj, pd.core.frame.DataFrame)
        # treat default 'index' option in DataFrame.to_csv method as False instead of True
        options = {'index' = False}
        options.update(kwargs)
        # save obj as csv
        obj.to_csv(filename, **options)

    @staticmethod
    def __saveme__assert_message__(filename, obj, instance):
        assert isinstance(obj, instance), f"you entered a filename, {filename}, with an object of type {type(obj)}; which is invalid."

    def __saveme__npy__(self, filename, obj, **kwargs):
        self.__saveme__assert_message__(filename, obj, np.ndarray)
        np.save(filename, obj)

    def __saveme__pkl__(self, filename, obj, **kwargs):
        self.__saveme__assert_message__(filename, obj, dict)
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)

    def __saveme__txt__(self, filename, obj, **kwargs):
        self.__saveme__assert_message__(filename, obj, list)
        with open(filename, 'w') as f:
            f.writelines(obj)

#=============================================================================#
