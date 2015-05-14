from rotmg_playerInfo import *

__author__ = 'Muffin'

if(__name__) == '__main__':
    lolwut = RotmgPlayerInfo("REDACTED", "REDACTED");
    for k, v in lolwut.classList.classDict.items():
        v.printStats()