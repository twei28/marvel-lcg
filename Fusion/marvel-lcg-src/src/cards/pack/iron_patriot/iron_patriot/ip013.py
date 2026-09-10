from . import *

# Call to Arms — EVENEMENT, cout 3, RES [wild]. TACTIC.
# Alter-Ego Action: Choose any number of REGISTERED allies in play. Ready each
#   of those characters, and they take +1 consequential damage (✧) after they
#   thwart or attack this round.
#
# CARTE DE REFERENCE
#  - `vz015` Stronger Together (pack venomized) : redresser plusieurs
#    personnages d'un coup, par `Faces.ReadyAll`.
#  - `GainUntilRoundEnd` : le bonus qui dure « this round ». Le +1 consecutif
#    est un MALUS, donc une valeur POSITIVE sur
#    `attack_consequential_damage` / `thwart_consequential_damage`.
#
# TEXTE CONTRE CODE
#  ⚠ « ANY NUMBER » : de zero a tous. La borne basse est zero, il faut donc
#    `range=("Zero", ...)` — sans quoi le moteur exigerait au moins une cible
#    et la carte deviendrait injouable sans allie.
#  ⚠ « REGISTERED ALLIES IN PLAY », pas « you control » : en multijoueur, ceux
#    des autres joueurs comptent aussi.
#  ⚠ Le +1 consecutif porte sur LES DEUX pouvoirs, contre et attaque.


def GetAbilities() -> Sequence['Ability']:

    def appel_aux_armes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        cibles = [c for c in effect.targets if c is not None]
        if not cibles:
            return
        Faces.ReadyAll(cibles, effect)
        for allie in cibles:
            allie.GainUntilRoundEnd(
                effect,
                attack_consequential_damage=1,
                thwart_consequential_damage=1,
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            appel_aux_armes,
        ).SetPlay()
        .SetTarget(CardFinder(trait=TRAIT_REGISTERED, card_type=Ally),
                   range=("Zero", "All")),
    ]
