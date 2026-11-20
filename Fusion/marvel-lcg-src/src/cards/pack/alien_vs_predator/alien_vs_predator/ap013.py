from . import *

# Thermal Target — ATTACHEMENT. CONDITION. YAUTJA. Boost ★ (+1). Deux exemplaires (13, 14).
# Attach to your identity.
# Forced Response: After your turn ends, take 2 damage and place 2 threat on the main scheme.
# Alter-Ego Action: Find a [[YAUTJA]] minion and reveal it → discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - attachement a l'identite + Reponse forcee de fin de tour + action pour s'en defaire : 21029 Sap Power (`AttachToFaceWhenPutIntoPlay
#    ("YourIdentity")`, `AfterPlayerTurnEnd(ForcedResponse, "You")`, `PlayerActionToDiscardThis(AlterEgoAction)`) ;
#  - « Find a minion » : `Find.Find` (regle Find, pd008), « reveal it » : `Reveal` (son « When Revealed » part) ;
#  - « Boost: Reveal this card » : `WhenCardBecomeBoost("This", RevealThisCard)` (tk BoostReveleCetteCarte).
#
# ⚠ Mots-pieges :
#  - « take 2 damage » (pas indirect) ET « place 2 threat on the MAIN scheme » : les deux ;
#  - « Find ... → discard » : trouver est le COUT ; sans sbire YAUTJA hors jeu, l'action n'est pas proposee ;
#  - « thiis » sur le scan : coquille de l'auteur, aucun effet.


def GetAbilities() -> Sequence['Ability']:
    return [
        *CibleMarquee("YAUTJA",
                      lambda effect, joueur: TrouverEtReveler(effect, joueur, "YAUTJA"),
                      lambda effect: SbireTrouvable(effect, "YAUTJA")),
        BoostReveleCetteCarte(),
    ]
