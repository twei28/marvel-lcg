from . import *

# Buzz Off — TRAITRISE (Cyber Swarm 5/6, x2). 1 boost.
# When Revealed: Choose:
#  • Place 3 threat on the main scheme.
#  • Take 2 damage.
#
# Cartes de reference : `tx008` (« Choose » = `ChooseAbilities` + `ForChoiceAbility`) ; « Take N damage » =
# les degats a l'IDENTITE du joueur (modele wd111 Pit Trap : `this.DealDamage([identite], n, effect)`).
#
# Mots-pieges : « Choose » = UNE des deux puces ; « TAKE 2 damage » : l'identite du joueur a qui la carte
# est revelee, pas un allie.


def GetAbilities() -> Sequence['Ability']:

    def choisir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place 3 threat on the main scheme",
                lambda cibles: this.PlaceThreatOnSchemes("MainScheme", 3, effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Take 2 damage",
                lambda cibles: this.DealDamage([joueur.GetIdentity()], 2, effect),
            ),
        )

    return [AbilityFactory.WhenThisRevealed(None, choisir)]
