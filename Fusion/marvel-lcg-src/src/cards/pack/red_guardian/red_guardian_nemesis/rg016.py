from . import *

# "I Don't Want You" — traitrise nemesis de Red Guardian
# When Revealed: Choose to either spend a [physical] resource or discard 1
#   random card from your hand.
#
# Gabarit : Energy Drain (spdr/spdr_nemesis/31028), la traitrise officielle qui
# oppose une depense de ressources a un autre effet. « Spend a [physical]
# resource » est un COUT, pas un effet : c'est
# `AbilityFactory.ForChoiceAbilityWithCost(Cost("R"))`, sans operation — payer
# EST l'option. Le moteur genere lui-meme le libelle « Spend [physical] ».
#
# "R" = physical (`game/element/rbyg.py:16` : r phySiCal, b mental, y energy,
# g wild). Une ressource [wild] paie donc bien ce cout, comme sur table.
#
# Note de moteur : la presence d'un `ForChoiceAbilityWithCost` met
# `forced=False` dans `ChooseAbilitiesHelper` (player_action.py:224). C'est le
# comportement officiel partage avec 31028 et Running Interference (02046), pas
# une particularite de cette carte.
#
# Autre note de moteur, verifiee en partie : main sans aucune ressource
# [physical], l'option « Spend [physical] » reste AFFICHEE, mais le moteur
# n'offre aucun moyen de la payer (`target_payment.payment == []`) ; la choisir
# est rejetee ("... WhenPlayerChooseAbility failed") et le joueur se rabat sur
# la defausse au hasard, ce qui est bien le resultat attendu. Energy Drain
# (31028), carte OFFICIELLE au montage identique, se comporte exactement pareil
# avec une main sans [energy] : c'est le moteur, pas cette carte. Le cout est
# donc reellement exige — seul l'affichage de l'option morte differe.


def GetAbilities() -> Sequence['Ability']:

    def i_dont_want_you(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("R"),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 random card from your hand",
                lambda targets:
                    joueur.DiscardRandomHandCards(1, effect),
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            i_dont_want_you,
        ),
    ]
