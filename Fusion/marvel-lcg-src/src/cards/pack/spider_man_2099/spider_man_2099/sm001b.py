from . import *

# * Miguel O'Hara — ALTER-EGO. REC 4, main 6, 10 PV. CIVILIAN. GENIUS.
# [star] Accelerated Healing — Response: After you make a basic recovery,
#   discard 1 card from your hand -> ready Miguel O'Hara.
#   (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `45015`, `tg007` Wart : « After you make a basic recovery » =
#    `AfterUnitMakeRecovery(type, "You", op, is_basic_recovery=True)`
#    (RECETTES §1). Le type est `AlterEgoResponse` parce que le texte parle de
#    la RECUPERATION, qui n'existe qu'en forme civile — sans quoi un allie qui
#    recupere declencherait aussi (piege note dans la recette).
#  - `45014` : « discard a card from your hand » en COUT =
#    `CostFunc.Discard("YourHandCards")`.
#  - `an001a`, `31009`, `ho011` : `Faces.ReadyAll([...], effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « ready MIGUEL O'HARA », un NOM PROPRE, pas « ready your identity » : la
#    capacite ne vaut que sur CETTE face. On redresse `this`, jamais
#    `joueur.GetIdentity()` — qui rendrait la face heros si le joueur avait
#    change de forme entre-temps. (Meme piege que `an002` Sera, RECETTES §3 :
#    un nom propre ne designe qu'UNE face.)
#  ⚠ « discard 1 card from your hand → » : la fleche en fait un COUT. Sans
#    carte en main, la capacite n'est pas payable et n'est donc pas offerte.
#  ⚠ « Limit once per round » -> `LimitOncePerRound()`. Temoin d'epuisement
#    exige (PROCESSUS-CARTE 7 bis) : deux recuperations de base dans le meme
#    round, et la TAILLE DE MAIN mesuree au second (elle ne doit plus baisser).
#  ⚠ Le `[star]` imprime est une convention d'impression, pas un
#    `NonKeywordStar` (RECETTES §1).
#  ⚠ L'etoile imprimee a cote de REC n'est pas une valeur de jeu : chez Rainy
#    elle pointe la statistique visee par la capacite etoile de la carte.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)
        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterUnitMakeRecovery(
            AbilityType.AlterEgoResponse,
            "You",
            redresser,
            is_basic_recovery=True,
        ).SetName("Accelerated Healing")
        .SetCostFunc(CostFunc.Discard("YourHandCards"))
        .LimitOncePerRound(),
    ]
