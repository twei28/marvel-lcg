from . import *
# Shi'ar Bodyguard. Sbire SHI'AR, Guard, Toughness (cles `desc`), x2.
#
# Players cannot attack ELITE minions.
# [star] Boost: Give the villain and all ELITE minions a tough status card.
#
# Cartes de reference : `AbilityFactory.UnitCannotBeAttacked` (do_attack.py:990, message `CheckIfUnitCanBeAttackBy` :
# la cible est retiree des choix, pas seulement refusee a la resolution), gb018 (boost : `WhenCardBecomeBoost`),
# `Faces.GiveStatus(..., "Tough")` (RECETTES §2).
# ⚠ « Players cannot attack ELITE MINIONS » : les sbires ELITE, pas le vilain (meme ELITE). Le Bodyguard n'est pas ELITE
# lui-meme (trait SHI'AR seul).
def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        cibles = []
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            cibles.append(vilain)
        cibles += [f for f in Worlds.FindCardsOnField(effect, card_type=Minion) if f.IsInPlay() and EstElite(f)]
        if cibles:
            Faces.GiveStatus(cibles, "Tough", effect)
    return [
        AbilityFactory.UnitCannotBeAttacked(CardFinder(trait="ELITE", card_type=Minion)),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
