from . import *

# Honorary Avenger
#
# ERRATA RRG 1.7 / 1.8 (Annexe V) : « Attach to a friendly character. Max 1 per character. » (ajout de « Max 1 per character »).
#   Le comportement est DEJA celui du nouveau texte : `desc.MaxPerUnit = 1` (cards.json) est lu par `CanPlayThisUpgradeCard` (`game/ability/factory/play.py`,
#   `max_per_unit`) et par `Upgrade.CanAttachTo` ; l'audit du 03/11/2026 le croyait « ancien » parce que le TEXTE affiche n'avait pas la ligne.
#   Preuve : cas `03025` de `tools/cas/errata_rrg.py` (la 2e copie n'a aucune cible legale sur le meme personnage, et se pose sur un autre).

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Friend
        ).SetPlay(only_if_your_identity_has_trait="AVENGER"),
        *AbilityFactory.GiveKeywordToAttached(
            Friend,
            health=1,
            trait="AVENGER",
        ),
    ]

