from . import *

# Atlantean Amulet — ATTACHEMENT (ensemble Attuma). ATLANTIS. ITEM. Badge +1 SCH.
# Attach to an ATLANTIS enemy. Otherwise, attach to the villain.
# Attached character gets +5 hit points.
# Hero Action: Spend [energy][mental] resources → discard this card.
#
# Cartes de reference :
#  - « Attach to an ATLANTIS enemy. Otherwise, attach to the villain » : `AttachToFaceWhenPutIntoPlay`
#    avec `otherwise_attach_to` (modele standard « attach to X, otherwise Y »).
#  - « Attached character gets +5 hit points » : `AbilityFactory.GiveKeywordToAttached(health=5)`.
#  - « Hero Action: Spend [...] resources -> discard this card » : `PlayerActionToDiscardThis(HeroAction)`.
#
# ⚠ Mots-pieges : « an ATLANTIS ENEMY » (sbire ou mechant portant le trait, pas n'importe quel ennemi) ;
# icones de ressource DECISION UTILISATEUR (20/10/2026, pas de carte du meme pack a RES connue pour
# trancher par decoupe) : eclair bleu = energie, grappe de 3 disques = mentale -> Cost("YB").


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(trait="ATLANTIS", card_type=Enemy),
            otherwise_attach_to=Villain,
        ),
        *AbilityFactory.GiveKeywordToAttached(health=5),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YB")),
    ]
