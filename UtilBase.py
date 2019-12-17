#=============================================================================#
# import from external libraries                                              #
#=============================================================================#

#=============================================================================#
# import from djak suite                                                      #
#=============================================================================#

#=============================================================================#
# import from internal modules                                                #
#=============================================================================#

import config as conf

#=============================================================================#
# class definition                                                            #
#=============================================================================#

class UtilBase:

    #=========================================================================#
    # constructor                                                             #
    #=========================================================================#

    def __init__(self, name, *args, **kwargs):
        """constructor for UtilBase. Any class that directly or indirectly inherits UtilBase"""
        #==============================================================#
        self.name = name
        #==============================================================#
        # use the parser, if provided; if none provided, create an empty one
        if len(args) == 1:
            parser = args[0]
        elif len(args) == 0:
            parser = argparse.ArgumentParser(description="argument parser for UtilBase")
        self.__init_set_options_parser__(parser)
        #==============================================================#
        # if any key-word arguments are provided, write/overwrite their
        # items as attributes
        self.__dict__.update(kwargs)

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

    def __init__set_options_parser__(self, parser):
        """takes the given parser, adds default options (found in config.py) to the parser, then adds all the options as attributes"""
        #==============================================================#
        # verbose                                                      #
        #==============================================================#
        if conf.verbose == True:
            action = 'store_false'
        else:
            action = 'store_true'
        parser.add_argument('-v', '--verbose', action=action, help="if true, will print extra detail to terminal. useful for debuging or seeing what is happening under the hood.")
        #==============================================================#
        args = parser.parse_args()
        self.__dict__.update(args.__dict__)
        #==============================================================#
