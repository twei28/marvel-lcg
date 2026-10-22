from . import *

# Dark Shroud — ATTACHEMENT. SPELL. ATQ +1, Boost 1.
# Attach to Krahllak.
# Interrupt : When you or an ally you control would deal 4 or more damage to Krahllak with an attack, instead prevent all of that damage, place 1 corruption counter on your Creeping
#   Corruption, and discard this card.
#
# Cartes de reference : 01100 Enhanced Ivory Horn (attacher a un vilain nomme, `ATK+` lu dans `desc` par `HasModify`, rien a coder), 27077a Bell Tower (Interrupt sur
# `WhenUnitWouldTakeDamage` du vilain, `is_from_attack=True`), im007 (`message.PreventDamage`), hs112 (Interrupt d'un attachement de vilain ouvert aux joueurs).
# ⚠ Mots-pieges : « YOU OR AN ALLY YOU CONTROL » : l'identite OU un allie du joueur qui repond (`YouControlCharacter`), pas un sbire ni un autre joueur ; « 4 OR MORE » : le seuil se lit
#  sur les degats de CETTE attaque (`at_least_damage=4`) ; « WITH AN ATTACK » : degats d'attaque seulement (`is_from_attack`) ; « PREVENT ALL of that damage » : tout, pas seulement l'exces ;
#  « YOUR Creeping Corruption » : celle du joueur qui repond ; les TROIS effets (prevenir, jeton, defausse) partent ensemble.


def GetAbilities() -> Sequence['Ability']:

    def voile(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        joueur = effect.GetInitiator()
        message.PreventDamage(message.will_take_damage, effect)
        if joueur is not None:
            PlacerCorruption(effect, joueur)
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=KRAHLLAK)),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "AttachedVillain",
            voile,
            is_from_attack=True,
            who_deal_damage="YouControlCharacter",
            at_least_damage=4,
        ),
    ]
