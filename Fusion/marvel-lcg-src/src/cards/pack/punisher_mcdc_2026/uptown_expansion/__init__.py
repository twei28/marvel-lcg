from ..commun import *
from ..leads_the_big_apple import Joueur, EnLieu, ControlePar, PisteTerminee, CompteurPuisFin
from ..locations_the_big_apple import JoueurDuPersonnage
from ..the_big_apple import LeVilain

# Set Uptown Expansion (extension OPTIONNELLE de The Big Apple, p045-p057) : 3 lieux U1 U2 U3 (une 4e rangee AU-DESSUS de la grille) et 3 pistes de plus.
# Les lieux et les pistes se comportent comme ceux de la grille (`locations_the_big_apple`, `leads_the_big_apple`) : on n'interagit qu'avec le lieu occupe,
# les pistes se lisent « While in <lieu> ». La rangee, le 4e CAPO et les 12 pistes sont mis en place par `the_big_apple.MettreEnPlaceLaVille`.
LIEU_U1, LIEU_U2, LIEU_U3 = "pu023", "pu024", "pu025"
