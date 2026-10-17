from . import *

# Gaslight — EVENEMENT 1 [mental], Ninjutsu (TMNT Shinobi, Inkwire). THWART.
# Hero Action (thwart): Discard a cloaked status card from your hero -> choose:
#  • Remove 3 threat from a scheme.
#  • Confuse an enemy.
# « You must have imagined that... » —Donatello
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md).
#
# Cartes de reference :
#  - `sk049` The Thing / `CoutDefausserCloaked("hero")` : cout « discard a <statut> status card from your hero » ;
#  - `ud004` / `up024` : « choose: • ... • ... » = `joueur.ChooseAbilities(effect, ForChoiceAbility(..).SetTarget(..), ...)` ;
#  - `10019` To the Rescue! : « Remove N threat from a scheme » = `RemoveThreatFromSchemes` ; `08003` Covert Ops : « Confuse the
#    villain » = `Faces.GiveStatus(.., "Confused", effect)` avec `canbe_confused=True`.
#
# TEXTE CONTRE CODE
#  ⚠ « Discard a cloaked status card FROM YOUR HERO -> » est le COUT (devant la fleche) : sans Cloaked sur le heros,
#    l'evenement n'est pas jouable.
#  ⚠ « choose: » : UNE seule branche, pas les deux ; « 3 threat from A scheme » : un complot, 3 au plus ; « Confuse AN enemy » :
#    un ennemi (vilain ou sbire) qui peut etre desoriente.


def GetAbilities() -> Sequence['Ability']:

    def gaslight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 3 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 3, effect),
            ).SetLabel('thwart')
            .SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gaslight,
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CoutDefausserCloaked("hero")),
    ]
