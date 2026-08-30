from . import *

# * Star Light — AMELIORATION signature, custom « jakxin »
# Cout 2, [energy], trait SUPERPOWER.
#
# Hero Resource: Exhaust Star Light → generate a [wild] resource. You may
#   change the printed resource of the played card to a [wild] resource.
#
# C'EST LA COMBO CENTRALE DU PACK, et l'insert de l'auteur la recommande :
# payer une carte SUPERPOWER avec Star Light rend la branche [wild] de
# Star-Gaze accessible depuis n'importe quelle carte — donc « redresser
# Ms. America », le plus fort des quatre effets.
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# `kb013` Kate's Quiver (pack kate_bishop) : meme structure « Resource:
# Exhaust X → generate a [wild] resource ET un second effet », meme montage
# `AbilityFactory.CanGenerateResources(..., Resources("G"),
# ex_operation=...)` + `.SetCostFunc(CostFunc.Exhaust("This"))`. Le second
# effet passe OBLIGATOIREMENT par `ex_operation=` : c'est le seul point
# d'entree, et son oubli cote MOTEUR avait rendu Sue Storm et Reed Richards
# a moitie muets (GUIDE §8).
#
# ⚠ UNE SEULE `CanGenerateResources` PAR CARTE (assert card_player.py:50) :
# les deux phrases tiennent donc dans une seule fabrique, la seconde dans son
# `ex_operation`.
#
# ---------------------------------------------------------------------------
# « YOU MAY CHANGE THE PRINTED RESOURCE OF THE PLAYED CARD »
#
# La phrase n'a d'effet que sur ce que Star-Gaze LIT. Voir le grand
# commentaire de ms_america/__init__.py (`ForcerRessourceImprimeeEnWild`) :
# ecart technique assume, on pose un drapeau plutot que de muter la valeur
# par `Message.WhenCountingResourcesOnCards`, parce que cette mutation
# changerait AUSSI ce que la carte vaut si elle etait ensuite depensee comme
# ressource.
#
# « the PLAYED card » -> `message.paying_card` (sender_player.py:281-285),
#   la carte pour laquelle on est en train de payer. Elle peut etre absente
#   (on paie le cout d'une capacite, pas d'une carte) : on garde.
# « YOU MAY » -> `player.MayChooseOneAbility` : le joueur peut refuser.
#   ⚠ Le pilote du harnais DECLINE systematiquement les choix optionnels ;
#   le cas de test correspondant porte `accepter_choix: True` (GUIDE §8).
# « to a [wild] resource » -> une seule couleur possible, aucun choix a
#   proposer au-dela du oui/non.
#
# LA FLECHE EST UN COUT : `CostFunc.Exhaust("This")` porte par la capacite.
# Star Light inclinee ne finance plus rien.


def GetAbilities() -> Sequence['Ability']:

    def star_light(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        carte_payee = message.paying_card
        if carte_payee is None:
            return

        player = message.GetToPlayer()
        if player is None:
            return

        player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Change the printed resource of the played card to [wild]",
                lambda targets:
                    ForcerRessourceImprimeeEnWild(effect, carte_payee),
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            ex_operation=star_light,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
