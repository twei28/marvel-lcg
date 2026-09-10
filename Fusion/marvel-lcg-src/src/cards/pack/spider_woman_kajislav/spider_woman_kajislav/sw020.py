from . import *

# Separation from the Child — OBLIGATION de Julia Carpenter. Boost 2.
# Give to the Julia Carpenter player.
# You may flip to alter-ego form. Choose:
#  • Exhaust Julia Carpenter -> remove Separation from the Child from the game.
#  • Remove all psionic web counters from your identity. If less than 5
#    counters were removed this way, this card gains surge. Discard this
#    obligation.
#
# ⚠ ELLE VIT DANS LE DOSSIER DU SET HEROS, PAS DANS `_nemesis`. Son bandeau
# imprime dit « SPIDER-WOMAN », pas « SPIDER-WOMAN NEMESIS » : son `set_name`
# est celui du heros, et le moteur cherche le module dans le dossier du
# `set_name` (database.py:195). Rangee dans `_nemesis`, elle ne serait JAMAIS
# chargee, EN SILENCE. Quatorzieme fois que le piege se presente.
#
# ⚠ Le pack livre DEUX sets nemesis alternatifs, et celui-ci n'a d'obligation
# QUE pour le set A « Man-Bull » : le set B « verze 2 » a la sienne, `sw027`
# Fugitive.
#
# CARTES DE REFERENCE
#  - `su014` Crisis of Conscience / `ip015` Exposed Insanity : le calque exact —
#    `WhenThisObligationGiveToYou`, `YouMayFlipToYourAlterEgoForm`, un choix a
#    deux branches, `Faces.RemoveAllFromGame` sous `CostFunc.Exhaust(
#    "YourIdentity")`, et une branche de repli qui defausse l'obligation.
#
# TEXTE CONTRE CODE
#  ⚠ « Give to the Julia Carpenter player » est une BASE NATIVE, `desc.GiveTo`.
#    Sans elle le montage du deck tombe sur une `AssertionError` (mesure du
#    09/09/2026 sur `ip015`).
#  ⚠ « YOU MAY flip » : optionnel, et AVANT le choix — le joueur peut vouloir
#    passer civil pour pouvoir payer la premiere branche.
#  ⚠ « Exhaust JULIA CARPENTER » : l'ALTER-EGO. En forme heros la branche
#    mentirait, d'ou la condition de forme.
#  ⚠⚠ « If LESS THAN 5 counters were removed THIS WAY » : on compte ce qui est
#    VRAIMENT parti, pas le stock d'avant. 5 en retire exactement 5 : pas de
#    deferlement. 4 en retire 4 : deferlement. Le temoin de test porte sur
#    cette frontiere.
#  ⚠ « remove from the game » n'est PAS une defausse : `Faces.RemoveAllFromGame`
#    (⚠ `Faces.RemoveFromGame` au singulier n'existe pas).
#  ⚠ La seconde branche VIDE le stock : c'est la vraie punition du pack, elle
#    coute tout ce que Julia a accumule.


def GetAbilities() -> Sequence['Ability']:

    def obligation(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Faces.RemoveAllFromGame([this], effect)

        def tout_perdre(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            retire = RetirerDesToiles(joueur, ToilesDe(joueur), effect)
            if retire < 5:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Julia Carpenter → remove Separation from the Child from the game",
                retirer,
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Remove all psionic web counters from your identity",
                tout_perdre,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(obligation),
    ]
