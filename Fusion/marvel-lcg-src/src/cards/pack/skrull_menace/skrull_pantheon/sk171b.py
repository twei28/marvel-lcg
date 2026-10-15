from . import *

# * Sl'gur't (II) — MECHANT, stade 2 (une face de la carte double face sk171a/sk171b). SCH 1, ATQ 3, 18 PV par joueur. GOD. SKRULL.
# When Revealed: Place 1 faith counter on Sl'gur't.
# Forced Response: After resolving step one of the villain phase, discard the top card of the encounter deck for each faith counter on Sl'gur't. Deal the players each treachery card discarded this way as a facedown encounter card in player order.
#
# Cartes de reference :
#  - Reponse apres l'etape 1 de la phase du mechant : `hunting_season/hs226` Master Trapper
#    (`AbilityFactory.AfterResolveVillainPhaseStep(ForcedResponse, 1, op)`) ; defausse du dessus du
#    deck rencontre : `Worlds.DiscardEncounterCards(n, effect)` (modele sk106 / sk139, rend les
#    cartes defaussees) ; distribution face cachee : `player.DealEncounterCard(face, effect)`
#    (modele 27087b / 53031).
#  - Carte double face : `fne/typhoid_mary/60110a` (vilain recto-verso, `"villain": ["a,b"]`) ;
#    jeton : `Faces.PlaceCountersOn([this], 1, 'faith', effect)` (compteur maison, card_face.py) ;
#    statut : `Faces.GiveStatus([this], "Tough", effect)` (modele sk151 Metallic Skin).
#
# ⚠ Mots-pieges : « for each FAITH counter ON Sl'gur't » (le compteur de CETTE carte, partage par les
# deux faces) ; « treachery card » (seules les traitrises sont distribuees, les autres restent defaussees) ; « in player order » (une carte a la fois, du premier joueur
# au dernier, puis on recommence) ; « AFTER resolving step one » (Reponse apres l'etape 1, avant les
# activations) ; « pas de carte d'etat a ce stade ».


def GetAbilities() -> Sequence['Ability']:
    return [
        RevelationDuMechant(False),
        ReponseFoi(True),
    ]
