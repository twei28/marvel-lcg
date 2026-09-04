from . import *

# * Firebird (Bonita Juarez) — ALLIE JUSTICE, cout 3, PV 3, CTR 2* / ATQ 1*.
#   AERIAL. RANGER. [energy].
# [star] Interrupt: When Firebird thwarts, discard the top card of your deck.
#   For each [energy] printed resource discarded this way, reduce all
#   consequential damage Firebird takes by 1 for this use.
#
# CARTES DE REFERENCE
#  - `40049` Probability Field : LE modele, ligne pour ligne — une
#    interruption sur un pouvoir de base, `CostFunc.DiscardDeckTopCards` en
#    cout, et le comptage des icones sur les cartes rendues par
#    `effect.cost_func.Get(...).return_discarded_cards`.
#  - `33016` Coordinated Attack : `GainForThisActive(..., 
#    thwart_consequential_damage=-1)`, la reduction « pour cet usage ».
#
# TEXTE CONTRE CODE
#  « discard the top card » N'EST PAS UN COUT ICI (pas de fleche) : c'est le
#    premier effet de l'interruption. Mais le moteur n'a qu'un seul montage
#    pour « defausser puis compter ce qui est sorti », et c'est le cout
#    (`return_discarded_cards`). ⚠ CONSEQUENCE ASSUMEE : l'interruption ne
#    part pas si le deck ET la defausse sont vides, la ou le texte la ferait
#    partir sans effet. Cas de bord sans portee pratique.
#  « For each [energy] PRINTED resource » -> l'imprime, pas la couleur
#    courante : `GetPrintedResourcesCount(faces, "Y", deck)`.
#  « reduce ALL consequential damage ... FOR THIS USE » -> `GainForThisActive`
#    sur le message du pouvoir en cours, pas un bonus de phase.
#  ⚠ « When Firebird THWARTS » -> `powers=["THW"]` seulement. Son attaque, elle,
#    lui coute toujours son degat consequent.


def GetAbilities() -> Sequence['Ability']:

    def oiseau_de_feu(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        faces = effect.cost_func.Get(CostFunc.DiscardDeckTopCards).return_discarded_cards
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        energie = FacesCounter.GetPrintedResourcesCount(faces, "Y", joueur.player_deck)
        if energie > 0:
            this.GainForThisActive(
                effect, message,
                thwart_consequential_damage=-energie,
            )

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            oiseau_de_feu,
            powers=["THW"],
        ).SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 1)),
    ]
