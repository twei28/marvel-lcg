from . import *

# * Kirigi — SBIRE. HAND. NINJA. ATQ 2 / MNG 1 / PV 3, Boost ★. Teamwork (NINJA).
# When Defeated : The defeating player either spends 2 resources of any type or shuffles Kirigi into the encounter deck.
# [star] Boost : If an ally is defending against this attack, this card gains [boost][boost] and this attack gains overkill.
#
# Cartes de reference : fne/art_museum_heist/60127 + shadows_in_the_night/sl004a (choix payant `ForChoiceAbilityWithCost` + `PeutCouvrirLeCout`), spdr/31036 Spot (`Faces.ShuffleAllTo([this], "EncounterDeck")`
#  sur When Defeated), sm/guerrilla_tactics/27145 (`message.GainBoostIcon(2)`), anachronauts/an013 (`attaque.GainOverKill` sur le message d'attaque du boost).
# ⚠ Mots-pieges : « either ... or » = UN choix, le joueur (pas le moteur) tranche ; « 2 resources of ANY type » = Cost("2") ; la branche payante n'est offerte que si
#  payable (le moteur reduirait sinon le choix au plus gros morceau payable) ; « the defeating player » = qui a vaincu Kirigi ; boost : les DEUX effets exigent qu'un allie defende
#  (« this card gains [boost][boost] » compte dans l'ATQ de cette attaque), l'overkill va sur CETTE attaque. Teamwork est lu dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = JoueurQuiVainc(effect, message)
        if joueur is None:
            return

        def depenser(targets: Sequence['CardFace'], res: 'Resources') -> None:
            pass                                                             # le cout est la depense ; Kirigi reste defait

        def melanger(targets: Sequence['CardFace']) -> None:
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(Cost("2"), "Spend 2 resources of any type", depenser,
                                                    conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("2"))]),
            AbilityFactory.ForChoiceAbility("Shuffle Kirigi into the encounter deck", melanger),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if not UnAllieDefend(effect, message):
            return
        message.GainBoostIcon(2, effect)
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
