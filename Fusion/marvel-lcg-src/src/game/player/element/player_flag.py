from core import *

class PlayerFlag:

    def __init__(self) -> None:
        self.Reset()

    FLAG = Literal[
        "ECHO_REFLEXES_DEJA_PAYEES",
        "MAGIK_ONCE_PER_PHASE",
        "YOU_TAKE_THE_FIRST_TURN_DURING_THE_PLAYER_PHASE",
        # CORRECTIF (26/10/2026, pack Rachel Summers `rm`) : nombre de tours en plus (rm007 Temporal Reversal) ;
        # « finir le tour » demande par une carte (rm013 Memory From The Future).
        "RM_TOUR_SUPPLEMENTAIRE",
        "RM_FIN_DE_TOUR",
    ]

    ################################################################################
    #
    def Reset(self):
        self.flags: Dict[str, int] = {}

    def Set(self, flag: FLAG, value: int):
        self.flags[flag] = value

    def Get(self, flag: FLAG) -> int:
        if flag in self.flags:
            return self.flags[flag]
        return 0

    def Update(self, flag: FLAG, value: int):
        value += self.Get(flag)
        self.Set(flag, value)

