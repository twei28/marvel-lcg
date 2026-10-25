from . import *

# Chop-Shop Cybernetics — MANIGANCE ANNEXE (module Reaver Resources). Menace de depart 3, Amplify 1, Hinder 1 par joueur, Boost 3.
# Hinder 1[per_hero].
# Forced Response: After a TECH attachment enters play, give the villain and the attached enemy a tough status card.
#
# Cartes de reference :
#  - `Hinder`, `Amplify` : natifs de `desc` (fiches mots-cles/hinder.md, amplify.md ; `16066` Blockade, `16054` Vendetta) ;
#  - « After an attachment attaches » : `AfterCardAttachTo(ForcedResponse, CardFinder(card_type=Attachment, trait="TECH"), ..., op)`
#    (`message.upgrade` = l'attachement, `message.to_face` = le porteur) ; `Faces.GiveStatus(cibles, "Tough", effect)`.
#
# ⚠ Mots-pieges :
#  - icone du coin = AMPLIFY (glyphe `F`, comparee a Vendetta 16054) : chaque icone Boost d'une carte boost recoit +1 par manigance Amplify ;
#  - DECISION UTILISATEUR (25/10/2026) : « the attached enemy » = l'ENNEMI sur lequel le TECH vient de s'attacher, s'il y en a un ; un TECH
#    pose sur une IDENTITE (Inhibitor Collar) ne donne Tough qu'au VILAIN ; si le porteur EST le vilain, il n'a qu'UN statut ;
#  - « the VILLAIN » : le vilain en jeu (Lady Deathstrike), pas un sbire.


def GetAbilities() -> Sequence['Ability']:

    def robustesse(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        cibles: List['CardFace'] = list(Worlds.GetAllVillains(effect.world))
        porteur = message.to_face
        if Enemy.IsType(porteur) and porteur not in cibles:
            cibles.append(porteur)
        Faces.GiveStatus(cibles, "Tough", effect)

    return [
        AbilityFactory.AfterCardAttachTo(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Attachment, trait="TECH"),
            None,
            robustesse,
        ),
    ]
