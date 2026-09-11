from typing import TypeAlias
from core import *

class ResRBYG:

    # `L` : l'eclair (lightning), ressource MAISON du pack Zeus, ajoutee le
    # 11/09/2026. Cinquieme couleur a part entiere : un joker la vaut aussi,
    # et elle ne paie pas un cout type d'une autre couleur.
    RBYG: TypeAlias = Literal["R", "B", "Y", "G", "L"]
    RBY: TypeAlias = Literal["R", "B", "Y", "L"]

    def __init__(self, r: int, b: int, y: int, g: int, l: int = 0) -> None:
        from game.element.resources import Resources
        self.r = r # phySiCal
        self.b = b # mental
        self.y = y # energy
        self.g = g # wild, can be used as their type or any of the other types.
        self.l = l # lightning (eclair)

        self.total = r + b + y + g + l

        self.types = sum(1 for color in [self.r, self.b, self.y, self.g, self.l] if color > 0)

        self.color_text = ""
        self.color_text += f'{Resources.RES_TEXT["r"]*self.r}'
        self.color_text += f'{Resources.RES_TEXT["b"]*self.b}'
        self.color_text += f'{Resources.RES_TEXT["y"]*self.y}'
        self.color_text += f'{Resources.RES_TEXT["g"]*self.g}'
        self.color_text += f'{Resources.RES_TEXT["l"]*self.l}'

    def __mul__(self, val: int) -> 'ResRBYG':
        return ResRBYG(self.r*val, self.b*val, self.y*val, self.g*val, self.l*val)

    def __add__(self, other: 'ResRBYG|int') -> 'ResRBYG':
        if isinstance(other, int):
            return ResRBYG(self.r, self.b, self.y, self.g, self.l)
        else:
            return ResRBYG(self.r+other.r, self.b+other.b, self.y+other.y, self.g+other.g, self.l+other.l)

    def __sub__(self, other: 'ResRBYG|int') -> 'ResRBYG':
        if isinstance(other, int):
            return self + (-1 * other)
        else:
            return ResRBYG(self.r-other.r, self.b-other.b, self.y-other.y, self.g-other.g, self.l-other.l)

    @staticmethod
    def FromText(rbyg: str) -> 'ResRBYG':
        rbyg = rbyg.lower()
        r, b, y, g, l = rbyg.count('r'), rbyg.count('b'), rbyg.count('y'), rbyg.count('g'), rbyg.count('l')
        return ResRBYG(r, b, y, g, l)

    def OnlyHasColor(self, text: "ResRBYG.RBY") -> bool:
        if self.total == 0:
            return False
        if text == "R":
            return self.r + self.g == self.total
        elif text == "B":
            return self.b + self.g == self.total
        elif text == "Y":
            return self.y + self.g == self.total
        elif text == "L":
            return self.l + self.g == self.total

    def GetColor(self, text: 'ResRBYG.RBYG', *, convert_green_res: bool = True) -> int:
        if "G" in text:
            assert convert_green_res == False, f"{text=}"
        if convert_green_res:
            g = self.g
        else:
            g = 0
        if text == "R":
            return self.r + g
        elif text == "B":
            return self.b + g
        elif text == "Y":
            return self.y + g
        elif text == "L":
            return self.l + g
        elif text == "G":
            return self.g

    # if `green_is_a_type`, return [0, 5]
    # if not `green_is_a_type`, return [0, 4]
    def GetTypeKindsInternal(self, green_is_a_type: bool) -> int:
        types = 0
        if self.r > 0:
            types += 1
        if self.b > 0:
            types += 1
        if self.y > 0:
            types += 1
        if self.l > 0:
            types += 1
        if green_is_a_type:
            types += self.g
            types = min(5, types)
        return types

    def IsSameType(self) -> bool:
        # Au plus UNE couleur non-joker presente.
        return sum(1 for color in [self.r, self.b, self.y, self.l] if color > 0) <= 1

    def IsDifferentType(self) -> int:
        types = self.GetTypeKindsInternal(False)
        if self.g:
            types += self.g
            types = min(4, types)
        return types

    def CanPayThisCost(self, cost: 'ResRBYGA') -> bool:
        if self.total == 0:
            return False
        if cost.rbyg.total == 0:
            return True
        else:
            return \
                cost.r > 0 and self.r > 0 or \
                cost.b > 0 and self.b > 0 or \
                cost.y > 0 and self.y > 0 or \
                cost.l > 0 and self.l > 0 or \
                self.g > 0 or \
                cost.a > 0

class ResRBYGA:

    def __init__(self, a: int, rbyg: 'ResRBYG') -> None:
        self.rbyg = rbyg
        self.a = a
        self.true_val = self.a + self.rbyg.total
        self.total = max(0, self.true_val)

        self.color_text = self.rbyg.color_text
        if self.a > 0:
            self.color_text += str(self.a)

        if self.color_text == "":
            self.color_text = "0"

    @property
    def r(self) -> int:
        return self.rbyg.r
    @property
    def b(self) -> int:
        return self.rbyg.b
    @property
    def y(self) -> int:
        return self.rbyg.y
    @property
    def g(self) -> int:
        return self.rbyg.g
    @property
    def l(self) -> int:
        return self.rbyg.l

    def __mul__(self, val: int) -> 'ResRBYGA':
        return ResRBYGA(self.a*val, self.rbyg)

    def __add__(self, other: 'ResRBYGA|int') -> 'ResRBYGA':
        if isinstance(other, int):
            return ResRBYGA(self.a + other, self.rbyg)
        else:
            return ResRBYGA(self.a + other.a, self.rbyg + other.rbyg)

    def __sub__(self, val: int) -> 'ResRBYGA':
        return self + (-1 * val)

    @staticmethod
    def FromText(rbyga: str) -> 'ResRBYGA':
        rbyga = rbyga.lower()
        rbyga = rbyga.lstrip("RBY")

        if rbyga.isdigit():
            a = int(rbyga)
        else:
            a = 0
        return ResRBYGA(a, ResRBYG.FromText(rbyga))

