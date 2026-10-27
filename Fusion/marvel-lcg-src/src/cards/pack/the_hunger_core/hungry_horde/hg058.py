from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076, cas `[hg] hg058 Bite en ALTER-EGO` rouge) : la note
# ci-dessous affirme que `GetHero()` « renvoie toujours la face Heros imprimee » : FAUX, `Player.GetHero()`
# (`player_get.py:223`) fait `assert False` quand l'identite est en alter-ego -- la carte plantait en silence
# (aucun compteur pose) des qu'elle etait revelee a un joueur en alter-ego. Les degats vivent sur la CARTE
# d'identite, partages par ses deux faces : « your hero has damage on it » se lit donc sur
# `joueur.GetIdentity().sustained`, valable dans les deux formes.
#
# Bite — TRAITRISE (set partage « Hungry Horde », module du scenario « The Hunger Core »). Pas de trait
# imprime. [star] Boost: 2.
# When Revealed: Place 1 infection counter (2 if your hero has damage on it).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « infection counter » : PAS une fiche `mots-cles/` dediee -- tranche par hg037 Widow's Bite (meme pack,
#   commentaire detaille), reconduit par hg002/hg003/hg057 : compteur de carte/scenario ordinaire, mecanisme
#   deja documente dans le docstring de `commun.PoserInfection`.
# - [star] Boost (icone) : badge natif (`desc.Boost`), aucun script requis.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Charpente « When Revealed: <effet de base>, cible = le joueur a qui la carte est revelee » : modele hg037
#   Widow's Bite, qui utilise `message.GetToPlayer()` (jamais « each player » : Bite ne dit que « your hero »,
#   pas « each player », a la difference de hg002/hg003/hg057).
# - « if your hero has damage on it » : lecture retenue = le heros du joueur a deja subi des degats (ses PV
#   courants sont inferieurs a son maximum). Idiome DEJA UTILISE dans ce moteur pour « a deja subi des degats »
#   via la propriete `sustained` (`src/game/card/face/attribute/can_health.py`, `sustained = max_health -
#   health`, lignes 90-94) : `raza/raza/rl002.py` (`if this.sustained > 0`), `raza/raza/__init__.py`
#   (`identite.sustained >= SEUIL_DEGATS`), `mut_gen/sabretooth/32070.py` (`if villain.sustained == 0`). Ici,
#   « has damage on it » = `sustained > 0` (au moins 1 point de degat present), traduction directe sans
#   inventer de seuil. Sujet = « YOUR HERO » precisement (pas l'identite generique) : meme distinction que
#   hg037 Widow's Bite, branche Hero (« your hero is stunned » -> `joueur.GetHero()`, jamais
#   `joueur.GetIdentite()`/`GetIdentity()`) -- ici `joueur.GetHero().sustained > 0`
#   (`src/game/player/action/player_get.py:223`, `GetHero()`).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5)
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed(None, ...)`, forme non precisee : a la difference de
#   hg037 (deux branches Alter-Ego/Hero distinctes), Bite ne distingue PAS la forme du joueur -- « your hero
#   has damage on it » reste lisible quelle que soit la forme COURANTE (`GetHero()` renvoie toujours la face
#   Heros imprimee, independamment de la forme active) : une seule branche, aucun filtre de forme a passer a
#   la fabrique.
# « Place 1 infection counter » -> `PoserInfection(effect, joueur, 1)`, cas de base.
# « (2 if your hero has damage on it) » -> branche alternative, mutuellement exclusive avec le cas de base :
#   SI `joueur.GetHero().sustained > 0`, poser 2 AU LIEU DE 1 (la parenthese REDEFINIT le nombre a poser, elle
#   ne s'additionne pas au « 1 » qui la precede -- lecture standard d'une clause de clarification entre
#   parentheses sur une carte a valeur variable, deja la lecture retenue pour Rupture X/Hinder X dans ce
#   depot). Code en if/else strict, jamais 1 puis +2 (ce qui donnerait 3, non imprime).
# « YOUR hero » -> le heros DU JOUEUR a qui la carte est revelee (`message.GetToPlayer()`), jamais un heros
#   choisi au hasard ni tous les heros de la partie (mot-piege « each »/« your » de l'etape 5 : ce texte ne
#   dit PAS « each player », contrairement a hg002/hg003/hg057 du meme pack).
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# cards_custom.json hg058 : {"Boost": "2"} -- native, non reecrite ici. Les deux seules autres valeurs
# imprimees sont dans le texte lui-meme : « 1 » (cas de base) et « 2 » (cas endommage), codees en dur dans la
# branche if/else ci-dessous, conformes mot pour mot au texte imprime.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Lecture de « (2 if ... ) » comme un REMPLACEMENT (2 au lieu de 1) plutot qu'un AJOUT (1 + 2 = 3) : lecture
# naturelle de cette formulation de clarification entre parentheses, deja appliquee ailleurs dans ce depot
# pour des cartes a valeur variable, confiance elevee -- mais aucune AUTRE carte du MEME scenario « The
# Hunger Core » ne partage exactement cette syntaxe « valeur de base (valeur alternative si condition) » pour
# verification croisee directe (hg037 Widow's Bite, le plus proche, utilise deux BRANCHES separees selon la
# FORME du joueur, pas une parenthese conditionnelle sur une seule branche). A CONFIRMER en partie reelle si
# ce point precis preoccupe ; ne bloque pas l'ecriture du script (regle « mode accelere » de cette tache).


def GetAbilities() -> Sequence['Ability']:

    def morsure(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        if joueur.GetIdentity().sustained > 0:
            PoserInfection(effect, joueur, 2)
        else:
            PoserInfection(effect, joueur, 1)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            morsure,
        ),
    ]
