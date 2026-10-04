from . import *

# Hyborian Havoc (x2) — evenement, cout 3 [physical]. ATTACK. THWART.
# Hero Action (attack/thwart): Deal 5 damage to an enemy or remove 4 threat
#   from a scheme. If you are:
#   • Conan the Thief, confuse an enemy.
#   • Conan the Barbarian, stun an enemy.
#   • King Conan, all of the above.
#
# CARTES DE REFERENCE
#  - « deal X or remove Y » : 44043 Bob, Agent of Hydra (ChooseAbilities a
#    deux ForChoiceAbility), helper `ChoisirDegatsOuMenace`.
#  - « (attack/thwart) » : bk004 (`SetLabel('attack', 'thwart')`).
#
# TEXTE CONTRE CODE
#  « confuse AN enemy » / « stun AN enemy » : un ennemi CHOISI, pas forcement
#    celui qu'on vient de frapper. King Conan : les deux.


def GetAbilities() -> Sequence['Ability']:

    def havoc(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        ChoisirDegatsOuMenace(joueur, this, effect, 5, 4)
        forme = joueur.GetIdentity().paper.card_id
        if forme in (ID_VOLEUR, ID_ROI):
            DonnerStatutAUnEnnemi(joueur, effect, "Confused", "Confuse an enemy")
        if forme in (ID_BARBARE, ID_ROI):
            DonnerStatutAUnEnnemi(joueur, effect, "Stunned", "Stun an enemy")

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            havoc,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
