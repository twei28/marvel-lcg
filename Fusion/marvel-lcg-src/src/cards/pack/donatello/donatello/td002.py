from . import *

# * Metalhead — ALLIE, cout 2, [energy]. ANDROID. PV 1, ATQ 2*, CTR 2*.
# Toughness.
# Interrupt: When Donatello defends against an attack, spend a [mental]
#   resource -> play Metalhead from your hand or Donatello's Shell without
#   paying his resource cost.
#
# CARTES DE REFERENCE
#  - `dd003` Doombot (et `45031` Colossus) : un allie qui se joue en
#    INTERRUPTION depuis la main, `CanPlayThisAllyCard()` +
#    `PlayCardsLikeInTurn([this], effect, ignore_resources_cost=True,
#    forced=True)`.
#  - `27012`/`03033` : la fenetre « when X defends against an attack » est
#    `WhenUnitDefendAgainstAttack(Interrupt, "YourHero", ...)`.
#  - `td012` (meme pack) + `60030` : la zone de cartes posees fournit
#    `IsLikeInHand()`, qui rend l'allie jouable depuis la Carapace.
#
# TEXTE CONTRE CODE
#  « spend a [mental] resource » est DEVANT la fleche : un COUT, `Cost("B")`.
#  ⚠ On ne peut PAS utiliser `.SetPlay()` : il fixe le cout a PAYER au cout
#    imprime de la carte (card.py:328 `SetPlayCost(printed cost)`), alors que
#    le texte dit « WITHOUT paying his resource cost » et ne demande qu'une
#    ressource [mental]. L'interruption est donc une capacite ORDINAIRE (hors
#    `Play`) a cout `B`, et c'est elle qui joue la carte avec
#    `ignore_resources_cost=True`.
#  « from your hand OR Donatello's Shell » -> `IsLikeInHand()` : main, ou zone
#    de cartes posees sous la Carapace (insert : « You may play Metalhead using
#    his interrupt ability while tucked under Donatello's shell »).
#  « When DONATELLO defends » -> forme HEROS uniquement ("YourHero").
#  « Toughness » est lu dans `desc` : aucun module.
#
# TODO-QUESTION : aucune, MAIS montage non prouve — une capacite hors `Play`
# portee par une carte en MAIN n'est offerte que si le moteur enregistre ses
# effets hors jeu (`NoOutOfPlayLimit`, idiome aa002/dz014/tt013). A TESTER en
# phase C (cas : Metalhead en main, Donatello se defend, option proposee ?).


def GetAbilities() -> Sequence['Ability']:

    def en_main_ou_sous_la_carapace(effect: 'Effect',
                                    message: 'Message.WhenUnitWouldDefend') -> bool:
        Unused(message)
        return effect.this.IsLikeInHand()

    def metalhead(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.PlayCardsLikeInTurn([this], effect,
                                   ignore_resources_cost=True, forced=True)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "YourHero",
            metalhead,
            conditions=[en_main_ou_sous_la_carapace],
        ).SetCost(Cost("B"))
        .NoOutOfPlayLimit(),
    ]
