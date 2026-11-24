from . import *

# Hunger Pulse. TREACHERY. HIVE. Boost 1 (icone).
# When Revealed: Place 1* threat on the main scheme (2* if the Core is exposed).
# [star] Boost: Place 1 infection counter.
#
# Cartes de reference :
#  - « When Revealed: Place X threat on the main scheme » : modele `27157` Deepest Fears
#    (pack sm, personal_nightmare), `Worlds.FindMainScheme(this)` + `PlaceThreatOnSchemes([scheme], X, effect)` ;
#    ici on utilise directement le raccourci `PlaceThreatOnSchemes("MainScheme", valeur, effect)`
#    (`card_face.py:1010`, memes la meme chose : il appelle `Worlds.FindMainScheme` en interne).
#  - Valeur « 1* »/« 2* » (asterisque = par heros, pas un renvoi de note) : meme convention que
#    « Rupture 1 [per_hero] » sur hg001-003 (`commun.py`, `Villain.DealDamage(..., rupture_x * NombreDeJoueurs(...))`) ;
#    ici le moteur fait la multiplication lui-meme via `Worlds.ConvertPerPlayerIconToInt`
#    (`game/operate/worlds.py:706`), qui sait lire un `str` du type `"1*"`/`"2*"`.
#  - « [star] Boost : Place 1 infection counter » : fiche mots-cles/boost.md, modele `an013` Hel-Wolf
#    (pack angela_nemesis) pour le gabarit `AbilityFactory.WhenCardBecomeBoost("This", operation)`
#    (type `AbilityType.Boost` deja pose par la fabrique, aucun autre champ a fournir) ; le joueur vise
#    est `message.GetToPlayer()`, modele `60062` (pack fne/echo_nemesis) et `62029` (pack luke_cage_nemesis).
#    Le compteur d'infection lui-meme est deja code au niveau du scenario : `commun.PoserInfection`
#    (place sur l'identite du joueur, "a second health bar... next to your identity card", page 6 du livret).
#
# ⚠ Mot-cle A CONFIRMER (mais avec un fort indice en faveur de la lecture retenue) : « if the Core is
# exposed » n'est DEFINI NULLE PART dans le texte imprime d'une autre carte deja scriptee (ni hg001/hg002/
# hg003, qui portent seulement « Shielded by the Horde », l'etat INVERSE, ni hg004a/hg004b/hg005a/hg005b, ni
# le livret retranscrit dans commun.py). Lecture retenue, par symetrie avec « Shielded by the Horde »
# (bouclier actif tant qu'il y a au moins un Metazombie en jeu, cf. `CapacitesDuCoeur.bouclier` dans
# `__init__.py` du set) : le Coeur est « exposed » quand ce bouclier est TOMBE, c'est-a-dire quand
# `NbMetazombiesEnJeu(effect) == 0`. INDICE : `tools/cas/the_hunger_core.py` nomme DEJA un cas existant
# « hg001 exposed : aucun Metazombie en jeu -> le heros peut attaquer et blesser le Coeur normalement »
# (ligne ~35) -- c'est le vocabulaire choisi par l'auteur precedent du pack pour EXACTEMENT cette situation,
# avant meme que hg049 n'existe. A confirmer face au livret officiel (TTS) si une definition plus explicite
# s'y trouve ; ne bloque pas le script dans l'intervalle.
#
# Autres mots-pieges verifies :
#  - « the main scheme » (singulier, PAS « each scheme ») : seule LA manigance principale est visee, jamais
#    une manigance annexe eventuellement en jeu (The Hive Calls, hg050) -- d'ou le raccourci "MainScheme" et
#    pas "EachScheme"/"EachMainScheme".
#  - Boost ICONE (1, en bas a droite, `desc.Boost = "1"`) et effet Boost ETOILE (le texte sous le trait) sont
#    deux choses distinctes qui coexistent sur cette carte (fiche mots-cles/boost.md) : l'icone est purement
#    declarative (`desc.Boost`, deja dans data/cards_custom.json, rien a coder), seul l'effet etoile a un module.


def _coeur_expose(effect: 'Effect') -> bool:
    """« if the Core is exposed » -- A CONFIRMER (voir commentaire d'entete) : lu ici comme l'inverse du
    bouclier « Shielded by the Horde » (hg001-003), donc vrai quand plus aucun Metazombie n'est en jeu."""
    return NbMetazombiesEnJeu(effect) == 0


def GetAbilities() -> Sequence['Ability']:

    def hunger_pulse_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        valeur = "2*" if _coeur_expose(effect) else "1*"
        this.PlaceThreatOnSchemes("MainScheme", valeur, effect)

    def hunger_pulse_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(effect)

        joueur = message.GetToPlayer()
        if joueur is not None:
            PoserInfection(effect, joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hunger_pulse_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            hunger_pulse_boost,
        ),
    ]
