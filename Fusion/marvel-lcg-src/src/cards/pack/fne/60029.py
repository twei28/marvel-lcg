from . import *

# * Stick — Interrupt: When a friendly [[Martial Artist]] character uses a basic power, choose:
#   • Exhaust Stick → that character gets +1 to that basic power for this use.
#   • That character gets -1 to that basic power for this use. Ready Stick.
#
# CORRECTIF (16/10/2026, reskin ub053 Splinter de l'aspect TMNT Basic) : les deux options etaient DEUX
# Interruptions distinctes sur le meme declencheur ; le joueur (et le pilote des tests) pouvait donc
# declencher les DEUX sur la meme utilisation (+1 en inclinant, puis -1 en redressant : Stick revenait
# pret, bonus net nul). « choose » = UNE capacite, UN choix : une seule Interruption qui fait choisir
# (modele du choix a cout `ht014` Tidal Surge, `ForChoiceAbility(...).SetCostFunc(...)`).


def GetAbilities() -> Sequence['Ability']:
    def stick(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Support)

        def minus_one(targets: Sequence['CardFace']) -> None:
            message.GainValue(-1, effect)
            Faces.ReadyAll([this], effect)

        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust this card: +1 to that basic power",
                lambda targets: message.GainValue(1, effect)
            ).SetCostFunc(CostFunc.Exhaust("This")),
            AbilityFactory.ForChoiceAbility(
                "-1 to that basic power, ready this card",
                minus_one
            ),
        )
    finder = CardFinder2('MARTIAL ARTIST', Friend)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, finder, stick).SetTarget('Trigger')]
