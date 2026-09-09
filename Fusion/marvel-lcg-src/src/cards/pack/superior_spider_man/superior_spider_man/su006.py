from . import *

# * Anna Maria Marconi — SOUTIEN, cout 1 [mental]. GENIUS. PERSONA.
# Alter-Ego Action: Exhaust Anna Maria Marconi -> choose to either heal 3
#   damage from your identity or reduce the cost of the next upgrade played
#   this round by 1.
#
# CARTES DE REFERENCE
#  - `ab007`, `ma005` : un SOUTIEN paye par `CostFunc.Exhaust("This")`.
#  - `08013` Stealth Strike, `22005` : le choix a deux branches dans
#    l'operation.
#  - `bk009` Portal (RECETTES §4ter) : `ReduceCostToPlayFaceWhen(which_card,
#    valeur, which_player, ...)` pour une reduction de cout.
#
# TEXTE CONTRE CODE
#  ⚠ « ALTER-EGO Action » : sous-type dedie, la carte ne sert qu'en forme
#    civile (piege `27009` Web-Bracelet, PROCESSUS-CARTE §5).
#  ⚠ « heal 3 damage from YOUR IDENTITY » : l'identite du joueur, pas un
#    personnage au choix — donc pas de `SetTarget`.
#  ⚠ « THE NEXT upgrade played THIS ROUND » : UNE seule carte, et la reduction
#    expire a la fin du round meme si elle n'a pas servi. D'ou
#    `until_round_end=True` ET `unregister_after_exec=True` : le premier qui
#    tombe l'emporte.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet — l'inclinaison borne, et
#    un cas doit le montrer.


def GetAbilities() -> Sequence['Ability']:

    def anna_maria(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if joueur is None or identite is None:
            return

        def soigner(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite.HealHealth(3, effect)

        def reduire(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.effect.RegisterTemp(
                AbilityFactory.ReduceCostToPlayFaceWhen(
                    CardFinder(card_type=Upgrade),
                    1,
                    "You",
                ),
                unregister_after_exec=True,
                until_round_end=True,
            )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Heal 3 damage from your identity", soigner),
            AbilityFactory.ForChoiceAbility(
                "Reduce the cost of the next upgrade played this round by 1", reduire),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            anna_maria,
        ).SetName("Anna Maria Marconi")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
