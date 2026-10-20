from . import *

# Sentry Awakens (1A) — MANIGANCE PRINCIPALE, stade 1 (Kree Sentry).
# Contents: Kree Sentry (I) and Kree Sentry (II) (Kree Sentry (II) and Kree Sentry (III) instead for expert mode).
#   Kree Sentry, and Standard encounter sets. One modular encounter set (Imperial Guard).
# Setup: Put Rick Jones into play under the first player's control. Set 1 copy of Sentry's Grasp aside and attach the
#   other to Rick Jones.
#
# Cartes de reference :
#  - « Setup » d'une face 1A : `WhenCardSetup("This")`, modele gs117a (Majestrix) / OFFICIEL 50087a Batroc ;
#    `SetupCards.PutIntoPlay(.., under_control=True)` met en jeu une carte mise de cote sous le controle du premier
#    joueur (modele 50088b).
#  - « attach the other to Rick Jones » : `AttacherUnePoigne` (modele sunfire `AttacherUneBrulure`).
#  - « Contents » : composition du scenario, portee par data/scenarios/gs_kree_sentry*.json.
#
# ⚠ Mots-pieges : les DEUX Poignes commencent mises de cote (donnees du scenario) : « set 1 copy aside » est donc deja
# fait et seule « the other » est attachee a Rick Jones ; la phrase demande Rick EN JEU avant l'attache.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        rick = SetupCards.PutIntoPlay(effect, "FirstPlayer", True, name=RICK, card_type=Ally)
        if rick is None:
            rick = RickJones(effect)
        AttacherUnePoigne(effect, rick)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
