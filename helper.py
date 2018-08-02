class Helper(object):
    defaultText = """Eddie knowledge - what your opponents don't want you to know.\n\nCommands:
    .help
    .changes
    .fd <CHAR> [<MOVENAME>]
    .fds <CHAR> [<MOVENAME>]
    .atklevel <LEVEL>
    .alias <ALIAS>
    .addalias <ALIAS> | <VALUE>
    .removealias <ALIAS>
    .charnames\n
If you want to know more about a command, you can invoke its specific help by calling .help [command].
  Example: .help fd\n
For feature requests or bug reports etc., hit me up on Discord (prk`#1874)."""


    helpText = """Displays information about public commands of Eddie."""

    changesText = """Sends a link to changelog."""

    fdText = """Displays framedata of a specific move. Character names are:
    Axl
    Bedman
    Chipp
    Elphelt
    Faust
    I-No
    Ky
    May
    Millia
    Potemkin
    Ramlethal
    Sin
    Slayer
    Sol
    Sol-DI
    Venom
    Zato
    Leo
    Jack-O
    Jam
    Johnny
    Raven
    Kum
    Dizzy
    Answer
    Baiken

Normals or command normals are written in the standard way of numpad directions and P/K/S/H/D for the button used.

Special moves are named with their actual names. Some of the names are rather weird. In order to deal with that, the command will first search for a perfect fit. If that has not been found, it will search for moves which can be written in the following form:
    % MOVENAME %
meaning that movename can start with anything and end with anything, as long as MOVENAME is present in the string. In case more moves are found (e.g. Leo has two versions of Graviert Wuerde), all are displayed.

In case no MOVENAME is specified, Eddie sends a private message containing all the possible moves that a character has stored in the database.
In case 3 or more moves are found which correspond to MOVENAME, all of them are sent in direct message to prevent cluttering of chat."""

    fdsText = """Displays framedata of a specific move in a simplified manner. Character names are the same as when using the .fd command. Only displays startup, active frames, recovery frames, adv/ib adv and attack level.

Special moves are named with their actual names. Some of the names are rather weird. In order to deal with that, the command will first search for a perfect fit. If that has not been found, it will search for moves which can be written in the following form:
    % MOVENAME %
meaning that movename can start with anything and end with anything, as long as MOVENAME is present in the string. In case more moves are found (e.g. Leo has two versions of Graviert Wuerde), all are displayed.

In case no MOVENAME is specified, Eddie sends a private message containing all the possible moves that a character has stored in the database.
In case 3 or more moves are found which correspond to MOVENAME, all of them are sent in direct message to prevent cluttering of chat."""

    atklevelText = """Displays data of an attack level."""

    aliasText = """Displays value of an alias."""

    addaliasText = """Adds alias which can be used to search for moves. Example:
.addalias nobiru | anti air attack
If an alias already exists, it will not be overwritten."""

    aliasesText = """Sends a list of existing aliases as a PM."""

    removealiasText = """Removes a specified alias from the DB. Currently usable only by admin."""

    charnamesText = """Sends a PM with a list of character names in the DB."""

    helpTable = dict()
    helpTable['default'] = defaultText
    helpTable['help'] = helpText
    helpTable['changes'] = changesText
    helpTable['fd'] = fdText
    helpTable['fds'] = fdsText
    helpTable['atklevel'] = atklevelText
    helpTable['alias'] = aliasText
    helpTable['addalias'] = addaliasText
    helpTable['aliases'] = aliasesText
    helpTable['removealias'] = removealiasText
    helpTable['charnames'] = charnamesText


    def getHelptext(self, *kw):
        if len(kw) == 0:
            return self.helpTable.get('default')
        return self.helpTable.get(kw[0])

