from cards.pack import *

# ===========================================================================
# Pack THE VAULT — scenario custom de « Kajislav » (« MC Custom Content By: Kajislav »), 25/10/2026. Prefixe `vt`
# (tools/prefixes_fanmade.json), set 215. UN SEUL set `The Vault` (vt001-vt034), dossier the_vault/the_vault/.
#
# LE SCENARIO EN UNE PHRASE : HUIT VILAINS QUI S'ECHAPPENT D'UNE PRISON.
# Deck de vilains (les 8 de meme stade, melanges), plusieurs vilains en jeu, chacun avec un « Activation Order » qui fixe
# l'ordre (et le joueur visé) de leur activation ; brique `Villains` du 20/10/2026 + extension du 25/10/2026
# (`Rule(the_villain="LowestActivationOrder", activation_order=True)`, `Enemies.ActivationVillainsParOrdre`). Les
# vilains et les sbires uniques VAINCUS... ne le sont pas : les sbires uniques vont SOUS l'environnement The Vault (face
# cachee) ; un vilain vaincu est retire de la partie ; les joueurs gagnent quand tous les vilains sont sous le Vault ou
# vaincus, et perdent s'il n'en reste AUCUN dessous. Inspection of the Vault (obligation mise de cote) aggrave plusieurs
# cartes tant qu'elle est en jeu.
#
# ⚠ Les modules du set font `from . import *` : tout helper appele par une carte vit dans the_vault/the_vault/__init__.py,
# jamais dans celui du PACK (NameError avale par le moteur, lecon hk005).
# ===========================================================================
