from . import *

# Frog of Thunder — AMELIORATION, cout 2, [energy]. ASGARD. TITLE.
# Hero Resource: Exhaust Frog of Thunder -> generate a [energy] resource.
#   If you paid for a Throg card this way, deal 1 damage to an enemy.
#
# CARTE DE REFERENCE
#  - `54002` * Cybernetic Arm : MOT POUR MOT le meme montage — une
#    `CanGenerateResources` a cout d'inclinaison, plus un `ex_operation` qui
#    se declenche quand la ressource EST DEPENSEE et qui lit la carte payee
#    sur `message.for_effect`. C'est la recette « ressource + effet differe
#    sur la carte payee » de RECETTES-MOTEUR §4.
#  - `br005` Star Jump : `IsDeckBuildingClass(SET_HEROS)` pour « a <heros>
#    card », la primitive du moteur (helper `EstCarteDeThrog`).
#  - `08013` / `16155` : `ChooseAbilities` + `ForChoiceAbility(...).SetTarget()`
#    pour choisir l'ennemi.
#
# TEXTE CONTRE CODE
#  ⚠ « generate a [energy] resource » — UNE seule, et de couleur ENERGIE.
#    L'icone imprimee en bas a gauche de la carte est elle aussi [energy] :
#    les deux ont ete comparees au scan de tg005 Lightning Leap, qui porte la
#    meme (leçon Lockjaw, on ne nomme pas une icone a vue).
#  ⚠ AUCUN `for_card` : la ressource paie N'IMPORTE QUOI. Le texte ne
#    restreint pas ce qu'on peut payer, il conditionne seulement le BONUS.
#    C'est la difference avec `br010` Stormbreaker (« for an EVENT ») et avec
#    `54002` (« for an ATTACK event »), dont on copie le montage mais pas le
#    filtre.
#  ⚠ « a THROG card » -> `IsDeckBuildingClass`, jamais une comparaison de nom :
#    « Throg » est AUSSI le nom de la face heros, et un filtre par nom ne
#    verrait qu'elle. Le test porte sur la classe de deckbuilding, donc sur
#    les onze cartes du set heros.
#  « THIS WAY » -> seulement si c'est CETTE ressource qui a paye. C'est ce que
#    garantit `ex_operation`, appele par la fabrique au moment ou la ressource
#    est effectivement depensee.
#  « HERO Resource » -> indisponible en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def grenouille_du_tonnerre(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)

        payee = getattr(message.for_effect, "this", None)
        if not EstCarteDeThrog(payee):
            return

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 1, effect),
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
            ex_operation=grenouille_du_tonnerre,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
