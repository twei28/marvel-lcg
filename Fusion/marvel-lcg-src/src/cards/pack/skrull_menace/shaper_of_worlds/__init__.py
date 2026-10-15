from cards.pack.skrull_menace.communs_modulaires import *

# ===========================================================================
# Set modulaire SHAPER OF WORLDS (Skrull Menace, Kajislav) — sk228, sk229, sk230a-d.
# Six cartes : le sbire Shaper of Worlds, le complot annexe Cosmic Cube Creation et
# QUATRE exemplaires de la ressource Cosmic Cube Fragment (3 icones : YYY, BBB, RRR, RBY).
#
# Insert du set : « During setup, set Shaper of Worlds minion and all four Cosmic Cube
# Fragment resources aside, out of play. Cosmic Cube Creation side scheme is shuffled into
# the encounter deck as usual. »
# Le fichier du set (data/encounter_sets/sk_shaper_of_worlds.json) liste les SIX cartes ;
# Cosmic Cube Creation, seule carte du set qui reste dans le deck rencontre, remet les cinq
# autres de COTE a la fin de la mise en place (`MettreDeCoteLeSet`, WhenGameWouldBegin).
# ===========================================================================

NOM_SET = "Shaper of Worlds"
NOM_SHAPER = "Shaper of Worlds"
NOM_FRAGMENT = "Cosmic Cube Fragment"


def MettreDeCoteLeSet(effect: 'Effect') -> List['CardFace']:
    """Le sbire et les quatre fragments, melanges au deck rencontre par le chargement du set,
    partent en zone « mis de cote » (insert du set)."""
    a_ecarter = [f for f in Worlds.GetEncounterDeckCards(effect)
                 if f.paper.set_name == NOM_SET and not SchemeSide2.IsType(f)]
    if not a_ecarter:
        return []
    return Faces.SetAside(a_ecarter, effect)


def ShaperMisDeCote(effect: 'Effect') -> 'CardFace|None':
    faces = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_SHAPER, card_type=Minion))
    return faces[0] if faces else None


def FragmentsMisDeCote(effect: 'Effect') -> List['CardFace']:
    return list(Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_FRAGMENT)))
