# xerris
xerris challenge

This is the python solution to the battle ship challenge.  It can be run in several modes by providing the following arguments:
--manual        playerA gets to manually choose the location and orientation of their ship and bomb locations on playerB's board.  If this arg is ommitted the default is to run in fully automatic mode where both players are "computer players"
--quiet         Omit the bombint sounds when a hit is scored.
--curses-display    instead of a scrolling tty display use a curses display where playerA's board is on the left and playerB's board is on the right.

Note that the unittesting coverage for the player module suffered because of adding all the calls to curses based code which can't be tested in unittest.

