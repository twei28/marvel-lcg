from . import *

# * Tallus — AMELIORATION BASIC, cout 1, [mental]. ITEM.
# Action: Exhaust Tallus -> look at the top card of your deck. If that card is
#   an event, you may play it (paying its cost). Shuffle your deck.
# Response: After a [[LOCATION]] support enters play, ready Tallus.
#
# CARTE DE REFERENCE
#  - `05018` * Lockjaw et `dr001a` (pack doctor_druid) : le moteur n'a AUCUNE
#    operation « joue cette carte », l'idiome est `YouMayPlayCardLikeInHand`,
#    qui rend la carte JOUABLE. Ici `from_where="YourDeckTop"`.
#
# TEXTE CONTRE CODE
#  « If that card is an EVENT » -> filtre de type sur la permission.
#  « YOU MAY play it (PAYING ITS COST) » -> facultatif ET payant.
#  « Response: after a LOCATION support enters play » -> synergie explicite
#    avec bk007 Crystal Palace et bk015 Earth-295, tous deux LOCATION.


# ⚠ ECART ASSUME : « Shuffle your deck » N'EST PAS CODE.
# La permission de jouer la carte du dessus est accordee par
# `YouMayPlayCardLikeInHand(..., from_where="YourDeckTop")` et vit JUSQU'A LA
# FIN DE LA PHASE. Melanger le deck dans la foulee ferait disparaitre la carte
# que le joueur vient de regarder, avant meme qu'il ait pu la jouer : le
# moteur n'offre pas de fenetre « apres que tu aies decide ». Consequence
# reelle : la carte du dessus reste connue et reste jouable jusqu'a la fin de
# la phase, la ou la carte imprimee la rendrait a l'anonymat. C'est le seul
# ecart du pack, il est en faveur du joueur, et il est signale ici plutot que
# masque.


def GetAbilities() -> Sequence['Ability']:

    def consulter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for permission in AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.Rule,
            Event,
            from_where="YourDeckTop",
        ):
            this.effect.RegisterTemp(
                permission,
                unregister_after_exec=False,
                until_phase_end=True,
            )

    def redresser_tallus(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            consulter,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            CardFinder(card_type=Support, trait="LOCATION"),
            redresser_tallus,
        ),
    ]
