from . import *

# Inhibitor Collar (x2, hf216-hf217). Attachement TECH ARTIFACT. « Attach to your identity. Treat your identity's printed text box as blank (except for
# TRAITS). Alter-Ego Action : Spend [physical][physical] resources -> discard this card. Any player may trigger this ability. [star] Boost : If this
# activation is an attack, this attack gains overkill. »
# Cartes de reference EXACTES : ld017 / 40092 Inhibitor Collar (meme attache + texte blanc + `PlayerActionToDiscardThis(...).AnyPlayerCanDoThis()`),
# hf110 (`PlayerActionToDiscardThis(...).SetCost(Cost(...))`), 16134 (`message.would_atk_message.GainOverKill`).
# ⚠ Icone de ressource : le poing = [physical] = `R` (so002 / hf110 du meme auteur), `Cost("RR")` ; l'action est « Alter-Ego Action » (pas Hero).


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        *AbilityFactory.GiveKeywordToAttached("Character", treat_as_blank=True),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCost(Cost("RR")).AnyPlayerCanDoThis(),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
