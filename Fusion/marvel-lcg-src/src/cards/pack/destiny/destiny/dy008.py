from . import *

# Prescience (x2) : AMELIORATION (PSIONIC.), cout 1, [energy]. Classe Hero.
# Forced Interrupt: When you reveal a treachery card, cancel its "When Revealed" effects and discard it. Then, discard Prescience.
#
# CARTES DE REFERENCE
#  - `21036` Cosmic Ward (Adam Warlock) : clone exact (`WhenPlayerRevealCard(ForcedInterrupt, "You", Treachery, "WhenRevealed", op)` + `CancelWhenRevealedEffect`).
#
# TEXTE CONTRE CODE
#  « Forced » : obligatoire, des qu'une traitrise est revelee a ce joueur. « cancel its When Revealed effects AND discard it » : les deux ; « Then, discard Prescience » : la carte part apres.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def prescience(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        message.CancelWhenRevealedEffect(effect)
        Faces.DiscardAll([message.trigger], effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.ForcedInterrupt,
            "You",
            Treachery,
            "WhenRevealed",
            prescience,
        ),
    ]
