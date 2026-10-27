from . import *

# Zombie Magik — METAZOMBIE (Horde deck). MUTANT. MYSTIC. SCH 1. ATK 2. PV 10[per_hero].
# Portal to Limbo — Forced Response: After Zombie Magik activates against you, if you are not engaged with
# any minions, discard cards from the encounter deck until a minion is discarded and put it into play engaged
# with you. Then shuffle the encounter discard pile into the encounter deck. If no minion is discarded and
# there are fewer than 3 Metazombies in play, put a Metazombie into play.
#
# Cartes de reference :
#  - « After Zombie Magik ACTIVATES against you » : `AbilityFactory.AfterEnemyActivatesAgainstYou(
#    ForcedResponse, "This", func)` + `message.GetAgainstPlayer()`, modele EXACT `hg012` Zombie Thor
#    (meme fabrique, meme commentaire deja laisse par ce pack : « ACTIVATES couvre attaque ET manigance »,
#    a distinguer d'un filtre qui ne couvrirait que l'une des deux) et `nt013` Terrax the Tamer.
#  - « if you are not engaged with any minions » : `joueur.engaged_minions.GetSize() == 0`, modele EXACT
#    `fne/kingpin/__init__.py:CapacitesDeKingpin2` (`sans_sbire`, « if you are not engaged with a minion »
#    sur `60159b`/`60160b` Kingpin face 2) -- MEME verification, le pluriel imprime sur hg015 (« any
#    minions ») ne change rien : `engaged_minions` est deja la liste ENTIERE des sbires engages avec ce
#    joueur, sa taille est nulle ssi aucun sbire n'y est engage, qu'il y en ait zero, un ou plusieurs a
#    tester.
#  - « discard cards from the encounter deck until a minion is discarded and put it into play engaged with
#    you » : `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` puis `minion.PutIntoPlay(joueur,
#    effect)` (engage AUTOMATIQUEMENT ce sbire avec `joueur`, commentaire natif de
#    `face_on_event.py:PutIntoPlay` : « Will auto engage if this is a Minion »), modele EXACT `32109`
#    Master Mold (« discard cards from the encounter deck until a [[Sentinel]] minion is discarded. Put that
#    minion into play engaged with you » -> meme fabrique, meme `PutIntoPlay`, seul le filtre `trait=
#    "SENTINEL"` disparait puisque hg015 ne restreint a aucun trait).
#  - « Then shuffle the encounter discard pile into the encounter deck » : `Worlds.GetEncounterDiscardPileCards
#    (effect)` + `Faces.ShuffleAllTo(defausse, "EncounterDeck", effect)`, modele EXACT `60161b` The King's
#    Gambit (« Shuffle the encounter discard pile into the encounter deck, then discard cards... » -- meme
#    paire d'appels, seul l'ORDRE differe : 60161b melange AVANT la fouille, hg015 melange APRES ; voir
#    piege ci-dessous).
#  - « If no minion is discarded and there are fewer than 3 Metazombies in play, put a Metazombie into play » :
#    `NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU` + `MettreUnMetazombieEnJeu(effect, joueur)`
#    (`commun.py`, deja ecrit pour `hg047` Rise of the Horde! qui porte MOT POUR MOT la meme clause -- « If
#    there are fewer than 3 Metazombies in play, put one into play » -- et deja plafonne nativement a
#    `MAX_METAZOMBIES_EN_JEU` en interne, la verification ici est donc redondante avec celle du helper mais
#    reprend quand meme le texte imprime pour que le TEXTE-CONTRE-CODE ait un token a pointer).
#
# ⚠ Mots-pieges :
#  - « Portal to Limbo » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel (absent de
#    `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne le reprend comme mot-cle, aucun
#    vilain officiel ne l'imprime) : meme statut que « Storm » (hg012), « Hex » (hg014), « Absorption »
#    (hg011), « Ambush » (hg013, arbitrage utilisateur du 27/10/2026 deja documente dans hg013.py) -- rien a
#    ouvrir avant de coder, le texte qui suit EST la regle complete. Les references officielles « Magik »
#    (Sorcery Supreme, Galaxy's Most Wanted) emploient un VRAI mot-cle « Portal » sur certaines de leurs
#    cartes (gestion d'un jeton/amelioration persistante) ; hg015 n'imprime PAS ce mot-cle lui-meme (seul le
#    NOM de la capacite y ressemble), donc aucune fiche `mots-cles/portal.md` n'est a ouvrir ni a creer pour
#    CETTE carte -- voir note de fin de rapport si une autre carte Zombie Magik (hg043-045, deck signature)
#    imprime un jour le mot-cle lui-meme.
#  - « ACTIVATES », pas « attacks » : couvre AUSSI la manigance (forme alter-ego). Utiliser
#    `AfterEnemyActivatesAgainstYou`/`Message.AfterEnemyActivationEnd`, jamais `AfterUnitAttackUnit` seul
#    (meme piege deja documente sur hg012/nt013).
#  - « against YOU », contrairement a hg012 (« against A PLAYER ») : les deux textes resolvent en pratique
#    le MEME joueur via `message.GetAgainstPlayer()` (le joueur reellement vise par cette activation
#    precise) -- le moteur ne distingue pas « you » et « a player » sur ce message (deja note sur hg012),
#    seule la formulation anglaise differe (un texte de vilain « parle a la table », l'autre decrit l'effet
#    du point de vue du joueur vise).
#  - « if you are NOT engaged with any minions » : condition posee AVANT toute action -- si le joueur vise
#    EST deja engage avec au moins un sbire, RIEN ne se passe : ni fouille, ni remelange de la defausse de
#    rencontre, ni mise en jeu d'un Metazombie. Les trois phrases qui suivent (« discard... », « Then
#    shuffle... », « If no minion... ») sont donc toutes a l'INTERIEUR de la meme garde `if`, pas trois
#    effets independants qui partageraient seulement la premiere clause -- lecture confirmee par le modele
#    Kingpin (`sans_sbire` est un `conditions=[...]` qui empeche l'ability ENTIERE de se declencher, pas
#    seulement son premier effet).
#  - « put IT into play engaged with you » (« it » = LE sbire qui vient d'etre defausse, pas un sbire
#    quelconque) : `minion` est la valeur de retour DIRECTE de `DiscardEncounterCardsUntil`, jamais une
#    nouvelle recherche -- piege « that <nom> » du gabarit PROCESSUS-CARTE (verifier que la cible visee est
#    bien LA MEME carte que celle nommee plus haut).
#  - ORDRE « Then shuffle... » APRES la fouille-et-mise-en-jeu, a la difference du modele 60161b (qui
#    melange AVANT) : coder le remelange EN DERNIER, apres l'appel a `PutIntoPlay` -- sinon le sbire
#    nouvellement defausse reviendrait DANS le deck avant d'avoir ete pose en jeu, ce qui est interdit par
#    `DiscardEncounterCardsUntil` lui-meme (il travaille sur la face DEJA retiree du deck, donc l'ordre du
#    code n'aurait de toute facon pas pu la faire disparaitre a tort) mais surtout a CONTRESENS du texte
#    imprime, qui place explicitement « Then » apres la pose en jeu. Le remelange se fait SANS condition sur
#    le resultat de la fouille (meme si un sbire a ete trouve ET pose, la defausse de rencontre -- qui
#    contient d'ailleurs deja les cartes NON-sbires defaussees pendant la fouille elle-meme -- repart quand
#    meme dans le deck) : « Then shuffle » n'est pas une clause alternative a « discard cards... », c'est une
#    SUITE systematique a l'interieur de la meme garde.
#  - « shuffle the encounter discard pile into the encounter deck » : `Faces.ShuffleAllTo` ne fait rien
#    (natif, pas de garde a ecrire) si la defausse de rencontre est VIDE -- cas possible si la fouille a
#    elle-meme epuise deck ET defausse sans jamais trouver de sbire (`DiscardEncounterCardsUntil` remelange
#    deja lui-meme en interne dans ce cas precis, cf. commentaire du 23/10/2026 dans `worlds.py`) ; on prend
#    donc systematiquement un NOUVEL instantane de la defausse APRES la fouille (`Worlds.
#    GetEncounterDiscardPileCards(effect)`), jamais une liste capturee avant.
#  - « If NO minion is discarded » : condition sur le RESULTAT de la fouille (`minion is None`), pas sur
#    l'absence du mot-cle sbire sur la carte trouvee -- `DiscardEncounterCardsUntil(card_type=Minion)` rend
#    soit un VRAI Minion, soit `None` (deck et defausse de rencontre tous deux epuises sans aucun sbire a
#    trouver), aucune troisieme valeur possible.
#  - « there are fewer than 3 Metazombies in play » : relit `NbMetazombiesEnJeu(effect)` et
#    `MAX_METAZOMBIES_EN_JEU` (commun.py, deja = 3) AU MOMENT de cette resolution, pas une valeur figee a
#    l'entree de l'ability -- si Zombie Magik elle-meme compte dans ces 3 (elle y est forcement, elle vient
#    d'activer), un quatrieme Metazombie ne doit PAS entrer meme si la fouille n'a rien trouve ; `
#    MettreUnMetazombieEnJeu` replafonne d'ailleurs lui-meme en interne (coherent, redondant par securite).
#  - « put A Metazombie into play » (indefini, pas « the next one » ni un nom precis) : `
#    MettreUnMetazombieEnJeu` prend toujours le DESSUS du Horde deck courant (remelange avec sa defausse s'il
#    est vide), jamais un choix du joueur ni un Metazombie nomme -- coherent avec le texte, qui ne nomme
#    personne.
#
# Bloc nombres texte <-> code : SCH 1 / ATK 2 / PV 10[per_hero] -> `desc` de `data/cards_custom.json` (aucune
# valeur numerique dans CE script, l'ability ne lit/n'ecrit aucun nombre imprime sur Zombie Magik elle-meme) ;
# seule constante numerique touchee par le script est `MAX_METAZOMBIES_EN_JEU = 3` (commun.py), qui correspond
# au « 3 » imprime mot pour mot sur hg015 ET sur hg047 Rise of the Horde! (meme valeur, meme source).


def GetAbilities() -> Sequence['Ability']:

    def portal_to_limbo(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        if joueur.engaged_minions.GetSize() > 0:
            return

        minion = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if minion is not None:
            minion.PutIntoPlay(joueur, effect)

        defausse = Worlds.GetEncounterDiscardPileCards(effect)
        if defausse:
            Faces.ShuffleAllTo(defausse, "EncounterDeck", effect)

        if minion is None and NbMetazombiesEnJeu(effect) < MAX_METAZOMBIES_EN_JEU:
            MettreUnMetazombieEnJeu(effect, joueur)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            portal_to_limbo,
        ),
    ]
