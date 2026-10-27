from . import *

# Zombie Invisible Woman — METAZOMBIE (Fallen Heroes, modulaire). FANTASTIC. SCH 1. ATK 2. HP 4.
# Guard.
# This minion cannot be dealt damage by attacks from allies.
# When Revealed: Your identity and each ally you control are confused.
#
# Cartes de reference :
#  - « Guard » (mots-cles/guard.md) : cle native `desc.Guard`, aucun script -- meme statut que hg059.
#  - « This minion cannot be dealt damage by attacks from allies » : grep de `data/cards.json` sur
#    « cannot be dealt damage by attacks from » : AUCUN resultat, aucune carte officielle n'imprime ce
#    texte mot pour mot -- fabrique generique la plus proche : `AbilityFactory.WhenUnitWouldTakeDamage`
#    (bas niveau, deja utilisee par la fabrique-fille `UnitCannotTakeDamageWhile`, `damage.py`) avec ses
#    parametres natifs `is_from_attack=True` (restreint aux degats D'ATTAQUE, pas a tout degat) et
#    `who_deal_damage=Ally` (restreint a un ATTAQUANT de type Ally, verifie sur `message.source` -- la face
#    a l'origine des degats). `message.PreventDamage("All", effect)` annule integralement les degats, modele
#    de methode `PreventAllDamageTo` (meme fichier, meme appel) et de `UnitCannotTakeDamageWhile` (branche
#    « sinon » de `cannot_take_more_than_damage`, c'est la MEME ligne qu'elle appelle par defaut).
#  - « When Revealed: Your identity and each ally you control are confused » : `Faces.GiveStatus(cibles,
#    "Confused", effect)` sur `[joueur.GetIdentity(), *joueur.GetControlAllies()]`, modele `tk022` Lay the
#    Beatdown (« Your identity ... confused » -> `Faces.GiveStatus([joueur.GetIdentity()], "Confused",
#    effect)`) etendu a la liste complete « identite + chaque alliee », meme principe de concatenation de
#    cibles que `hg065` elle-meme n'a pas besoin de separer (`GiveStatus` accepte une liste heterogene de
#    `CardFace`).
#
# ⚠ Mots-pieges :
#  - « BY ATTACKS from allies » : uniquement les degats D'ATTAQUE (`is_from_attack=True`) dont la SOURCE
#    (`message.source`, PAS `effect.this` ni `message.by_effect.this`) est une Ally -- une attaque du HEROS
#    ou de l'IDENTITE passe normalement (seul `who_deal_damage=Ally` est filtre), et un degat INDIRECT ou
#    une capacite d'une alliee (hors attaque) passe aussi normalement (`is_from_attack=True` l'exclut).
#  - Protection PERMANENTE, sans condition de « while » ni de phase -> `AbilityType.NonKeyword`, pas de
#    `conditions=[]` supplementaire, pas de `LimitOncePerRound`/`Phase` (le texte n'en impose aucune, a la
#    difference de `hg007` Zombie Captain America -- Shield, qui limite « the first time each phase »).
#  - « Confused » est un statut DE BASE du moteur (comme Stunned, Tough), pas un mot-cle maison ni officiel
#    a ficher -- meme heuristique deja appliquee sur `hg010` pour Stunned (README.md mots-cles, § « Officiels
#    ») : seul `GiveStatus` est requis, `CanbeConfused()` est verifiee NATIVEMENT par le moteur a l'interieur
#    de `GainStatus` (pas de garde manuelle a ecrire si une cible ne peut pas etre confuse).
#  - « YOUR identity AND EACH ally YOU control » : le joueur a qui CETTE carte est revelee
#    (`message.GetToPlayer()`), jamais un joueur fixe ni « chaque joueur » (pas de « each player » imprime
#    ici, a la difference de `hg002`/`hg003`) -- une seule cible-joueur par revelation.
#  - « AND » entre « your identity » et « each ally » : les DEUX recoivent le statut dans le MEME appel, pas
#    deux capacites separees ; une liste vide d'allies (joueur sans allie) laisse simplement l'identite seule
#    dans la liste, sans erreur (`GiveStatus` sur une liste a un seul element fonctionne normalement).
#  - Deux capacites DISTINCTES sur cette carte (statique « cannot be dealt damage... » + declenchee « When
#    Revealed... ») : deux entrees separees dans `GetAbilities()`, pas une seule fabrique combinee -- aucune
#    des deux ne depend de l'autre pour se declencher.
#
# Bloc nombres texte <-> code : SCH 1 / ATK 2 / HP 4 / Guard 1 -> `desc` ; aucune valeur numerique propre au
# script (ni seuil de degats, ni compteur, ni limite imprimee sur cette carte).


def GetAbilities() -> Sequence['Ability']:

    def pas_de_degats_par_les_allies(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)

    def invisible_woman(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        cibles = [joueur.GetIdentity(), *joueur.GetControlAllies()]
        Faces.GiveStatus(cibles, "Confused", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.NonKeyword,
            "This",
            pas_de_degats_par_les_allies,
            is_from_attack=True,
            who_deal_damage=Ally,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            invisible_woman,
        ),
    ]
