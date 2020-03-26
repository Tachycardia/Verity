#!/usr/bin/env python3
# Program: Cogs Import Collector
# Author: Darren Trieu Nguyen
# Version: 0.1
# Function: To collect a list of all of the cogs in the given directory
#
# References:
#
# https://stackoverflow.com/questions/1057431/
#   how-to-load-all-modules-in-a-folder
# https://stackoverflow.com/questions/14426574/
#   how-to-import-members-of-all-modules-within-a-package/14428820#14428820

import os
global __all__
__all__ = []
globals_, locals_ = globals(), locals()

# Reading in a list of all cogs (recognizing cogs as .py files in cogs/)
def filterCogs(cogName):
    if ((cogName[-3:] == '.py') and (cogName != '__init__.py')):
        return True
    else:
        return False

cogList = filter(filterCogs, os.listdir(os.path.abspath('cogs')))
cogList = [cogName[:-3] for cogName in cogList]
print('Recognized Cogs: ' + str(cogList))

# Packaging cogs and appending into __all__ to be imported by the main bot
for cog in cogList:
    if cog[0] != '_':
        package_module = '.'.join([__name__, cog])
        try:
            module = __import__(package_module, globals_, locals_, [cog])
        except:
            print('Error: CogImportError')
        for cogName in module.__dict__:
            if not cogName.startswith('_'):
                globals_[cogName] = module.__dict__[cogName]
                __all__.append(cogName)

__all__ = [cogName[:-3] for cogName in cogList]

