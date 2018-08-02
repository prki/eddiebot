def moveNameInDB(key, dbCursor):
    dbCursor.execute("select movename from moves where movename=? collate nocase", (key,))
    moves = dbCursor.fetchall()

    if not moves:
        return False
    return True


async def getCharMoves(char, dbCursor):
    dbCursor.execute("select movename from moves where charname=? collate nocase", (char,))
    moves = dbCursor.fetchall()

    if not moves:
        return None

    moveString = "```"
    for move in moves:
        moveString = moveString + (move[0]) + "\n"
    moveString = moveString + "```"

    return moveString


def getFrameData(char, move, dbCursor):
    """Function returning a list of strings containing framedata
    for each move found in the database. If a precise result is found,
    return that one. If not, return a relaxed result where only similar
    moves are being found."""

    dbCursor.execute("select * from moves where charname=? collate nocase and\
                     movename =? collate nocase", (char, move))

    retVal = dbCursor.fetchall()

    if not retVal:
        #Nothing found with precise search, relax the movename reqs
        dbCursor.execute("select * from moves where charname=? collate nocase and\
                         movename like ? collate nocase", (char, '%' + move + '%'))
        retVal = dbCursor.fetchall()

    return retVal
