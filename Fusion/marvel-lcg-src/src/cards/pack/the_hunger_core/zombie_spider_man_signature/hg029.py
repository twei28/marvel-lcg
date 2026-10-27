from . import *

# Rooftop to Rooftop — SIDE SCHEME (deck signature de Zombie Spider-Man, carte 3/3, derniere du set,
#   hg027-029). Menace de depart 2[per_hero] (`desc.StartingThreat = "2*"`). Aucun trait imprime.
# While this scheme is in play, Zombie Spider-Man gets +1 SCH and cannot be attacked by allies.
#
# ---------------------------------------------------------------------------
# ETAPE 1 : cards_custom.json
#
# `card_id hg029, type SideScheme, name "Rooftop to Rooftop", desc.StartingThreat "2*", traits [],
# set_name "Zombie Spider-Man (Signature)"` -- entree deja presente (portee depuis TTS le 27/10/2026),
# rien a y modifier pour cette tache.
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - « Zombie Spider-Man GETS +1 SCH » (bonus constant tant que CETTE manigance est en jeu, sur un Metazombie
#   NOMME, sans attache) : modele `wd049` Dark Matter Conversion (pack web_of_deceit/electro -- manigance
#   annexe qui porte « The villain gets +2 ATK and gains retaliate 1 ») :
#   `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Villain), attack=2, retaliate=1)`.
#   Repris ici avec `CardFinder(name="Zombie Spider-Man", card_type=Villain)` (cible NOMMEE, pas « the
#   villain » generique) et `scheme=1` a la place de `attack=2, retaliate=1` -- meme fabrique que `hg007`
#   Zombie Captain America (« Each other Metazombie gets +1 ATK » ->
#   `GiveKeywordToInPlayWhenApplyThis(CardFinder(traits=["METAZOMBIE"], ...), attack=1, ...)`), qui
#   confirme que cette fabrique est deja utilisee et testee dans CE MEME scenario.
# - « CANNOT BE ATTACKED BY ALLIES » : exactement le texte de `hg021` Rotten Thrusters (meme Metazombie,
#   deck signature voisin Zombie Iron Man -- « Zombie Iron Man gets +1 SCH and cannot be attacked by
#   allies »), qui emploie `AbilityFactory.UnitCannotBeAttacked(<qui>, conditions=[attaquant_est_un_allie])`
#   avec un filtre `Ally.IsType(message.attacker)` sur `message.attacker` (`CheckIfUnitCanBeAttackBy`,
#   sender.py:116). Seule difference : `hg021` cible `"AttachedVillain"` (l'attache est COLLEE a Zombie Iron
#   Man) ; ici il n'y a AUCUNE attache -- `hg029` est une manigance annexe, pas une amelioration -- donc la
#   cible est un `CardFinder(name="Zombie Spider-Man", card_type=Villain)`, modele `tg012` Adorable
#   Distraction (pack throg_nemesis, meme fabrique visant une carte NOMMEE plutot que « This » ou le litteral
#   d'attache) : « Alligator Loki cannot be attacked » -> `UnitCannotBeAttacked(CardFinder(name=NOM_SBIRE,
#   card_type=Minion))`.
# - « WHILE THIS SCHEME IS IN PLAY » : ne se code PAS comme une condition supplementaire. `tg012` (meme
#   commentaire, reporte ici) : « la condition est portee par l'EXISTENCE de ce complot, pas par une
#   condition supplementaire : tant qu'il est en jeu, l'interdiction vaut » -- une capacite enregistree sur
#   une carte en jeu n'existe QUE tant que cette carte est en jeu (comportement natif du moteur, deja
#   observe sur `wd049`, qui ne porte lui non plus aucune clause de garde pour « tant que la manigance est en
#   jeu »). Rien a brancher sur un signal « cette manigance a-t-elle ete defaussee ».
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « +1 SCH » et « cannot be attacked by allies » : ni l'un ni l'autre n'est un terme EN GRAS imprime sur
#   cette carte (le texte imprime est en prose simple, aucun mot-cle officiel ou maison a catalogue) --
#   absents de `docs/reference/mots-cles/README.md`, meme constat deja fait sur `hg021`/`hg026` (le trait
#   CONDITION de leurs cartes-soeurs, et les bonus de stats en prose, n'ont jamais declenche de fiche).
#   Rien a ouvrir, rien a creer.
# - Pas de mot-cle imprime en gras du tout sur `hg029` : la carte ne contient qu'une seule phrase descriptive.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# - « Zombie Spider-Man » (nommement, pas « each Metazombie » ni « the villain ») -> `CardFinder(
#   name="Zombie Spider-Man", card_type=Villain)` : nom UNIQUE au depot
#   (`grep '"name": "Zombie Spider-Man"' data/cards.json data/cards_custom.json` : une seule occurrence,
#   dans `cards_custom.json`, meme verification que celle documentee par `hg026` pour « Zombie Hulk »).
# - « gets +1 SCH » : exactement UN bonus de manigance, aucun bonus d'attaque ni de defense -- ne pas copier
#   le `attack=2, retaliate=1` de `wd049` ni le `attack=1` de `hg007` : seul `scheme=1` est imprime ici.
# - « cannot be attacked BY ALLIES » : seuls les ALLIES sont vises, pas les heros -- meme piege que `hg021`,
#   le filtre `Ally.IsType(message.attacker)` est OBLIGATOIRE (sans lui, un heros serait bloque a tort).
# - « While this scheme is in play » : aucune clause separee a coder (voir Etape 2 ci-dessus) -- NE PAS
#   ajouter de condition `effect.this.IsInPlay()` : elle serait toujours vraie quand l'ability s'evalue
#   (une ability d'une carte hors jeu ne s'evalue pas), donc redondante, et risquerait de masquer un vrai
#   defaut si jamais elle etait fausse par erreur ailleurs.
# - Pas de « unless »/« otherwise »/« instead »/« if you cannot »/surge dans le texte imprime : rien d'autre
#   a coder.
# - Carte DEFENSIVE pour Zombie Spider-Man (buff + protection), elle n'attaque ni ne maniganche jamais
#   elle-meme : pas de `WhenThisRevealed`, pas de `WhenRevealed` -- aucune clause de revelation imprimee sur
#   cette carte (contrastant avec `hg023`/`hg024`/`hg028`, qui en portent une).
#
# ---------------------------------------------------------------------------
# ETAPE 6 : NOMBRES, TEXTE <-> CODE
#
# - « +1 SCH » -> `scheme=1` (`cards_custom.json` ne porte aucun badge chiffre dans `desc` pour cette valeur,
#   elle n'existe qu'en prose dans `text` -- comme `hg021`/`hg026`).
# - « StartingThreat: "2*" » (menace de depart « 2 par heros ») : lu NATIVEMENT par le moteur depuis `desc`
#   (`game/card/face/base/scheme.py:18`, `RegisterAttribute("StartingThreat", "start_threat")`), comme
#   `01108`/`01150` (autres manigances annexes « 2* » officielles) -- AUCUN script necessaire, base
#   automatique au meme titre que Toughness/Restricted (PROCESSUS-CARTE.md etape 6).
#
# A CONFIRMER EN JEU REEL : comme pour tout le deck signature (hg027/hg028 deja notes ainsi), aucun outil de
# ce lot ne verifie l'ENTREE EN JEU de cette manigance depuis le deck signature de Zombie Spider-Man (le
# mecanisme qui revele le dessus de ce deck, `hg046 Metazombie Power!`, n'est pas encore ecrit -- note deja
# posee par `hg026`). Les deux capacites codees ci-dessous ne peuvent donc etre prouvees qu'une fois la carte
# placee en jeu par l'API Puzzle directement (`Puzzle.PutIntoPlay`/equivalent), pas par un scenario complet.


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Spider-Man", card_type=Villain)

    def attaquant_est_un_allie(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        Unused(effect)
        return Ally.IsType(message.attacker)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            cible,
            scheme=1,
        ),
        AbilityFactory.UnitCannotBeAttacked(
            cible,
            conditions=[attaquant_est_un_allie],
        ),
    ]
