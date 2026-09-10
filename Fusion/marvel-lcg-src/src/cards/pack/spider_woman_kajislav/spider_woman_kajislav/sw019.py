from . import *

# Past and Future — EVENEMENT BASIQUE, cout 2, RES [wild]. 1 max par deck.
# Team-Up (Cassandra Webb and Julia Carpenter).
# Alter-Ego Action: Draw up to your printed hand size. Place 2 psionic web
#   counters on Julia Carpenter.
#
# ⚠⚠ UN TEAM-UP ENTRE UNE IDENTITE ET SON PROPRE ALLIE, ce qui est rare : les
# cartes officielles nomment deux HEROS. Ici « Cassandra Webb » est le
# SOUS-TITRE de `sw002` * Madame Web, une ALLIEE. Le moteur le gere deja :
# `GetTeamUpUnits` (has_teamup.py:21) parcourt les personnages AMIS et teste
# `unit.IsName(name) or unit.IsSubName(name)`, donc identite OU allie, par nom
# OU par sous-titre. Rien a coder, et rien a arbitrer.
#
# CARTES DE REFERENCE
#  - `12020` Swarm Tactics (pack ant) : le montage d'un Team-Up —
#    `desc.TeamUp` en donnee et `.SetTarget("TeamUp")` sur la capacite. Le
#    second n'est pas facultatif : `CardsDB.FindAbilities` en fait une
#    ASSERTION pour tout evenement portant `TeamUp` (database.py:220).
#  - `01025` Split Personality : la pioche jusqu'a la main, calculee comme
#    `hand_size - hand_cards.GetSize()`.
#
# TEXTE CONTRE CODE
#  ⚠ Le separateur de `desc.TeamUp` est le POINT-VIRGULE, pas la virgule
#    (has_teamup.py:16, `value.split(";")`). Une virgule ferait une liste d'un
#    seul element et le second personnage ne serait jamais cherche.
#  ⚠ « your PRINTED hand size » : la main IMPRIMEE, pas la courante. Une
#    amelioration qui augmente la main ne change donc rien ici — d'ou
#    `printed_hand_size`, jamais `hand_size`.
#  ⚠ « on JULIA CARPENTER » : l'identite, et l'Action est d'alter ego, donc
#    elle est bien sous cette face. Le stock reste le meme de toute facon.
#  ⚠ Main deja pleine : on ne pioche rien, mais les 2 compteurs tombent quand
#    meme — les deux phrases sont independantes.


def GetAbilities() -> Sequence['Ability']:

    def passe_et_avenir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        identite = IdentiteDe(joueur)
        if joueur is None or identite is None:
            return
        manque = identite.printed_hand_size - joueur.hand_cards.GetSize()
        if manque > 0:
            joueur.DrawUp(manque, effect)
        PoserDesToiles(joueur, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            passe_et_avenir,
        ).SetPlay()
        .SetTarget("TeamUp"),
    ]
