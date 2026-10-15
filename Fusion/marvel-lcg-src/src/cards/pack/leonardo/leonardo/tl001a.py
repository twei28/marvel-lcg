from . import *

# * Leonardo (face heros) — NINJA. TURTLE.
# CTR 2 / ATQ 2 / DEF 2 — HS 5 / PV 12
# Kenjutsu — Action: Ready a [[WEAPON]] upgrade you control.
#   (Limit once per round.)
#
# Cartes de reference :
#  - `04001a` * Hawkeye : `AbilityType.Action` sur une face HEROS, redressement
#    d'une amelioration par `SetTarget(Upgrade, ..., canbe_ready=True)` +
#    `Faces.ReadyAll(effect.targets, effect)` ;
#  - `41011` Weapons Training / `harry_osborn/ho009` : filtre de trait WEAPON
#    + `from_where=["YouControlCards"]` ;
#  - `ls001b` pour `.LimitOncePerRound()` (« once per ROUND », pas par phase).
#
# Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - le type imprime est `Action` NU (pas `Hero Action`) : on ecrit ce qui est
#    imprime. La face n'existe qu'en forme de heros, donc aucune consequence ;
#  - « a [[WEAPON]] upgrade YOU CONTROL » : `from_where=["YouControlCards"]`,
#    jamais une arme d'un autre joueur ;
#  - TOUTE amelioration WEAPON, pas seulement KATANA (tl011/tl012 portent les
#    deux traits, mais un WEAPON officiel en jeu est aussi une cible) ;
#  - `canbe_ready=True` : une arme deja prete n'est pas une cible legale
#    (sinon l'action se propose pour ne rien faire).


def GetAbilities() -> Sequence['Ability']:

    def kenjutsu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        Faces.ReadyAll(list(effect.targets), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kenjutsu,
        ).SetName("Kenjutsu")
        .LimitOncePerRound()
        .SetTarget(Upgrade, trait="WEAPON", from_where=["YouControlCards"],
                   canbe_ready=True),
    ]
