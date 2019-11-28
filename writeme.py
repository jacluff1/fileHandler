
#=============================================================================#
# import internal modules                                                     #
#=============================================================================#

#=============================================================================#
# import external packages                                                    #
#=============================================================================#

import argparse
import os

#=============================================================================#
# write templates                                                             #
#=============================================================================#

def write_template(*args):
    """for each given input file name, write a general template for python files and save it to file name. NOTE: do not provide '.py' file extenstion."""
    for filename in args:
        f1 = open(f"{filename}.py", 'w')
        f1.write("""\
#=============================================================================#
# import from external libraries                                              #
#=============================================================================#

#=============================================================================#
# import from djak suite                                                      #
#=============================================================================#

#=============================================================================#
# import from internal modules                                                #
#=============================================================================#
        """)
        f1.close()

def write_template_class(*args):
    """for each given input file name, write a template for python class files and save it to file name. NOTE: do not provide '.py' file extenstion."""
    for filename in args:
        write_template(filename)
        f1 = open(f"{filename}.py", 'a')
        f1.write(f"""\

#=============================================================================#
# class definition                                                            #
#=============================================================================#

class {filename}:

    #=========================================================================#
    # constructor                                                             #
    #=========================================================================#

    def __init__(self, *args, **kwargs):
        NotImplemented

    #=========================================================================#
    # public - defined                                                        #
    #=========================================================================#

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
        """)
        f1.close()

#=============================================================================#
# write to files                                                              #
#=============================================================================#

#=============================================================================#
# main                                                                        #
#=============================================================================#

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="arguments for writing files")

    parser.add_argument('-c', '--classTemplate', default=None, help="all the filenames (without '.py' extension) that you wish to write the the class template to. for single file, no quotes are needed; for multiple files, quotes are needed with each file separted by whitespace. default = None")

    parser.add_argument('-p', '--path', type=str, default=None, help="if path is not None, will join the path and filename for all filenames. default = None")

    parser.add_argument('-f', '--functionTemplate', type=str, default=None, help="all the filenames (without '.py' extension) that you wish to write the the functional template to. for single file, no quotes are needed; for multiple files, quotes are needed with each file separted by whitespace. default = None")

    args = parser.parse_args()
    kwargs = args.__dict__

    # TODO: set up verbose printing via printing methods in printme

    # make a template map
    tempMap = {
        'classTemplate': write_template_class,
        'functionTemplate': write_template,
    }

    for key,func in tempMap.items():
        if kwargs[key] == None:
            kwargs[key] = []
        elif " " in kwargs[key]:
            # split files into a list, white space is present in input
            kwargs[key] = kwargs[key].split()
        else:
            # if single file, still put into a list
            kwargs[key] = [kwargs[key]]
        if kwargs['path'] != None:
            # add any selected directory to filename(s)
            kwargs[key] = [os.path.join(kwargs['path'], filename) for filename in kwargs[key]]
        for filename in kwargs[key]: func(filename)
