from cards.pack import *

# ===========================================================================
# Pack BEAST — contenu custom. Set 134, prefixe `bt`.
#
# Hank McCoy, savant des X-Men. Deux sets : `Beast` (bt001a-bt018, dont les
# CINQ cartes « Discovery » bt014-bt018 qui vivent hors du deck) et
# `Beast Nemesis` (bt019-bt023, Dark Beast).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : LE POOL « DISCOVERY » SE MERITE
#
#   bt001b Scientific Discovery -> repasser en alter-ego melange 1 carte
#                                  Discovery au hasard dans le deck
#   bt006 In The Heat Of Battle -> vider une manigance en amene une de plus
#
# Les cinq Discovery ne sont donc JAMAIS dans le deck de depart : elles sont
# mises de cote (`BeginGameWithSetAside`, meme mecanique que les climats de
# Storm 36001b et les Squirrels de sg001b) et entrent une par une. Le pool
# s'epuise : cinq passages en alter-ego au maximum sur une partie.
#
# L'autre moitie du pack recompense la DEFENSE, la ou le heros est le plus
# fort (DEF 3 imprime) :
#
#   bt001a Thick Skinned      -> encaisser 0 degat repeche n'importe quelle carte
#   bt004 Experimental Warfare-> incline les ameliorations pour monter la DEF
#   bt012 Civilian Disguise   -> pioche a chaque defense, trois fois
#   bt013 Hunter Gear         -> +1 DEF
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES PREEXISTANTS (aucune collision d'id, mais la regle d'unicite
# les depart en jeu — a NE PAS mettre dans le deck de depart) :
#  - « Beast » : allie Leadership officiel 33011 (pack Cyclops). Notre bt001a
#    est une IDENTITE : les deux coexistent legalement, mais l'allie 33011
#    n'a rien a faire dans le deck de Beast lui-meme ;
#  - « Wonder Man » (bt002) : allie Leadership officiel 03014, HEROS officiel
#    58001a ;
#  - « Phoenix » (bt003) : allie signature 33002 (Cyclops), HEROS officiel
#    34001a, allie Leadership officiel 49014 ;
#  - « Peter Parker » (bt014) : ALTER-EGO 01001b (Spider-Man) et sr001b
#    (Spider-Man Rainy). Notre bt014 est un allie « Lab Assistant » : en
#    multijoueur avec un Spider-Man a la table, deux cartes du meme nom
#    peuvent se retrouver en jeu (une identite, un allie). Le moteur ne
#    l'interdit pas ; c'est le meme cas de figure que 15007/aa001a ;
#  - « Ambush » (bt016) : amelioration 'Pool officielle 44051 ;
#  - « Dark Beast » (bt022) : VILAIN officiel 45118/45119/45120 (Age of
#    Apocalypse). Notre bt022 est un SBIRE nemesis.
# ===========================================================================


def GetDiscoveryDeck(effect: 'Effect') -> List['CardFace']:
    """Les cartes Discovery encore mises de cote chez le joueur initiateur.

    Meme acces que `GetWeatherDeck` du pack storm : le `set_aside_deck` est
    un alias de `additional_discard_pile` (player.py:100), et
    `BeginGameWithSetAside` y depose les cinq cartes a la selection du heros.
    """
    initiator = effect.GetInitiator()
    if initiator is None:
        return []
    return initiator.set_aside_deck.Get()
