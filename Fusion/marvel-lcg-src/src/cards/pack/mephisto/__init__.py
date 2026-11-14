from cards.pack import *

# ===========================================================================
# Pack MEPHISTO : scenario custom de « Neptune » (« MC Custom Content by: Neptune »), 09/11/2026. Set 254, prefixe `mp`
# (tools/prefixes_fanmade.json). Zip : A creer/import-mephisto/. Plan et decisions : A creer/import-mephisto/PLAN-DAMNATION.md,
# questions-createur.md ; memoire de projet `mephisto-pack`.
#
# LE SCENARIO EN UNE PHRASE : Mephisto propose des pactes (attachements BARGAIN) ; accepter ou refuser, chacun coute des cartes du deck
# du joueur, envoyees dans la Damnation (zone maison, DeckType.DamnationArea, une pile par joueur) ; 10 cartes par joueur = defaite.
#
# card_id = `mp` + numero IMPRIME (n/28) pour le scenario ; les modulaires ont leur centaine :
#   mp001-mp028 Mephisto (faces a/b pour les complots 004-006 et l'environnement 007) ; mp101-105 Blackheart ;
#   mp111-116 Corruptive Offers ; mp121-132 Damned ; mp141-145 Mother of Demons ; mp151-157 Mephisto Standard ;
#   mp161-163 Mephisto Expert.
# Un dossier par SET (le nom du dossier est set_name en minuscules, espaces -> `_`) : sinon l'import est avale sans erreur.
