from . import *

# My Love (Crise Mentale) : OBLIGATION, boost 2. A donner au joueur de Raven Darkhölme.
# You may flip to alter-ego form. Choose:
# • Exhaust Raven Darkhölme and Destiny -> remove My Love from the game. Any player may help pay the cost for this ability.
# • Discard Destiny. If no card was discarded this way, this card gains surge. Discard this obligation.
#
# CARTES DE REFERENCE
#  - `dy013` Seizure / `mt011` Psychic Tremor : meme gabarit (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`).
#  - `sk280` / `cr016` : `ability.cout_en_groupe = True` pour « any player may help pay the cost » (lu par `CheckAnyPlayerMayHelpPay`).
#
# TEXTE CONTRE CODE
#  « Exhaust RAVEN DARKHOLME AND DESTINY » : DEUX inclinaisons dans le cout, l'alter-ego (donc seulement en forme alter-ego, apres l'eventuelle bascule) ET l'allie Destiny (ready, sous le controle du joueur) ; sinon la
#    branche n'est pas offerte. « remove My Love FROM THE GAME » : la carte quitte la partie. « Any player may help pay » : le cout ne comporte aucune ressource (que des inclinaisons), le marquage `cout_en_groupe` est
#    pose par fidelite au texte, sans effet visible. « Discard DESTINY » : l'allie ; sans allie, la branche reste offerte, aucune carte n'est defaussee et la carte gagne le surge. « If NO card was discarded this way, this
#    card gains surge. Discard this obligation » appartient a la SECONDE branche.
#  Chiffres : boost 2.


def GetAbilities() -> Sequence['Ability']:

    def my_love(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        destinys = [f for f in joueur.allies.Get() if f.IsName(NOM_DESTINY)]

        def defausser_destiny_et_celle_ci(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(cibles, effect)
            if not cibles:
                this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)

        seconde = AbilityFactory.ForChoiceAbility(
            "Discard Destiny. Discard this obligation",
            defausser_destiny_et_celle_ci,
        )
        if destinys:
            seconde.SetTarget(Ally, name=NOM_DESTINY, from_where=["YouControlCards"], canbe_discard=True)
        else:
            seconde.SetHasNoTargetEffect()

        premiere = AbilityFactory.ForChoiceAbility(
            "Exhaust Raven Darkhölme and Destiny → remove My Love from the game",
            lambda cibles:
                Faces.RemoveAllFromGame([this], effect),
            condition=joueur.IsAlterEgo() and any(d.CanExhaust() for d in destinys),
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")) \
            .SetCostFunc(CostFunc.Exhaust("YouControlCards", name=NOM_DESTINY))
        premiere.cout_en_groupe = True

        joueur.ChooseAbilities(effect, premiere, seconde)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            my_love,
        ),
    ]
