# Verity
Verification Discord Bot
========================

Dependencies:
-------------

Python3:

- discord

Quickstart:
-----------

1. Create a file called `verityKey.secret` and put your client secret key in 
   this file.
2. Run `./start.sh`

Installation And Use:
---------------------

This discord bot comes with a virtual environment that includes the discord
package with voice support. It can be loaded by running: 
`source VerityEnv/bin/activate`

Alternatively, instructions to install the discord package can be found here:
https://pypi.org/project/discord.py/

Once the dependencies are met, the bot can be run by running `python3 verity.py`.

Changelog:
----------

Version 0.8: 

- Added editable config file for paths
- Separated bot functions into cogs
