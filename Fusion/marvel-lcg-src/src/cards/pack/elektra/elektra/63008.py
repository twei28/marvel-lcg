from . import *

# Move Unseen — EVENEMENT, cout 2, [mental]. ACROBATIC. THWART. x2 (Elektra 6-7/15).
# Hero Action (thwart): Remove up to 4 threat from a scheme. Shuffle the top card of the NINJA deck into the encounter deck.
#
# CARTES DE REFERENCE
#  - « Remove N threat from a scheme » : `01012` Crisis Interdiction (`this.RemoveThreatFromSchemes(effect.targets, n, effect)`,
#    `SetPlay().SetLabel('thwart').SetTarget(Scheme2)`).
#  - « up to N » choisi par le joueur : `venus/tv003` (`joueur.DeclareNumber(0, N)`).
#
# TEXTE CONTRE CODE
#  ⚠ « UP TO 4 » : le joueur choisit de 0 a 4 menaces. Le melange Ninja est une phrase SEPAREE, sans condition : il part meme si 0
#    menace est retiree (la carte est jouee, son effet s'applique en entier).
#  ⚠ « a scheme » : n'importe quelle manigance (principale, annexe, de joueur) : `Scheme2`.
#  Chiffres : cout 2, 4 menaces maximum, 1 carte Ninja.


def GetAbilities() -> Sequence['Ability']:

    def move_unseen(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        menaces = joueur.DeclareNumber(0, 4)
        if menaces > 0:
            this.RemoveThreatFromSchemes(effect.targets, menaces, effect)
        MelangerDessusNinja(joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            move_unseen,
        ).SetPlay().SetLabel('thwart').SetTarget(Scheme2),
    ]
