from . import *

# CORRECTIF (27/10/2026, passe de fusion hg028-hg076) : l'ancienne lecture « Attach to Zombie Magik -> AUCUN code »
# etait FAUSSE (bloc CARTES DE REFERENCE reecrit en consequence). `commun.DefausserJusquaUneAmeliorationDuDeckSignature` n'est appelee QUE par hg008
# Zombie Iron Man et hg023 (son propre deck) ; Zombie Magik (hg015) n'imprime aucun mecanisme d'attache. Ses
# cartes signature sortent par la voie GENERIQUE (`commun.RevelerLeDessusDuDeckSignature`, appelee par hg046
# Metazombie Power! / hg064 Zombie Mister Fantastic) : `Reveal` -> `PutIntoPlay`, exactement comme hg018/hg026/
# hg031/hg034. Sans `AttachToFaceWhenPutIntoPlay`, Soulsword revelee ne s'attachait a rien (defaussee, aucun
# bonus). Ajoute, avec le meme `CardFinder(name=..., card_type=Villain)` que hg031/hg034. Prouve par les cas
# `[hg] hg043` (Puzzle.Reveal('hg043') avec hg015 en jeu -> accrochee, +1 ATK, Piercing).
#
# Soulsword — ATTACHMENT (deck signature de Zombie Magik, carte 1/3). Traits WEAPON, MYSTIC.
# Attach to Zombie Magik.
# Zombie Magik gets +1 ATK. Her attacks gain Piercing.
# Hero Action: Spend 3 resources → discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[piercing]] (mots-cles/piercing.md) : propriete booleenne de l'attaque, accordee ici de facon
#   PERMANENTE (tant que la carte est en jeu), pas sur une seule attaque declenchee par un cout. Fiche lue :
#   deux chemins possibles (statique `piercing=True` d'une fabrique d'attaque, ou dynamique
#   `message.GainPiercing(effect)`) — le chemin retenu ici est le 3e, deja employe par `hg019` Necrotic
#   Repulsors (meme deck, meme patron « <Nom>'s attacks gain Piercing » depuis un attachement TIERS, pas
#   depuis « This » qui attaque) : `AbilityFactory.UnitAttackGainKeyword(CardFinder(name=...), piercing=True)`
#   (do_attack.py:828), qui pose une Ability `NonKeyword` ecoutant `Message.CheckIfAttackMessageHasKeyword` et
#   appelle `message.GainPiercing(effect)` des que l'attaquant correspond au nom cible — exactement la fiche
#   piercing.md, cote « variante maison » (ho016 * Bullseye) sauf que la pose est PERMANENTE, pas conditionnee
#   a une capacite etoile.
# - « Hero Action » n'est PAS une fiche mots-cles dediee (absente du README, sous-type d'Ability de base —
#   PROCESSUS-CARTE.md etape 5, ligne « Hero Response/Hero Action : sous-type dedie, pas le type nu »). Rien a
#   ouvrir, mais bien choisir `AbilityType.HeroAction` et pas `AbilityType.Action`.
# - « gets +1 ATK » : pas un mot-cle, un BONUS DE STATISTIQUE statique pose par un attachement sur son hote —
#   fabrique `AbilityFactory.GiveKeywordToAttached(..., attack=1)`, modele officiel `01074` Inspired
#   (« Attached ally gets +1 THW and +1 ATK » -> `attack=1`). Rien a ouvrir dans `mots-cles/` (absent du
#   README, bonus chiffre nu).
# - Traits imprimes « WEAPON », « MYSTIC » : traits DE SAVEUR (classement officiel des armes/objets mystiques
#   du jeu, ex. `01036` Mjolnir porte aussi WEAPON ; cf. deja note sur `hg016` pour le trait ATTACK), pas des
#   mots-cles moteur — absents de `docs/reference/mots-cles/README.md`, rien a coder pour eux.
# - « Soulsword » lui-meme n'est le nom d'AUCUN mot-cle imprime sur cette carte (contrairement a l'arme
#   officielle « Soul Sword » de Magik qui porte parfois un mot-cle « Darkchilde » sur d'autres editions —
#   absent ici, cf. note de fin de hg015 qui renvoyait justement a hg043-045 pour un eventuel mot-cle
#   « Portal » : hg043 n'imprime NI « Portal » NI aucun autre mot-cle maison, seul Piercing, deja fiche).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to Zombie Magik » : `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Magik",
#   card_type=Villain))`, modele hg031/hg034 (voir le CORRECTIF en tete : la carte sort par la voie generique
#   `RevelerLeDessusDuDeckSignature` -> `Reveal` -> `PutIntoPlay`, jamais par
#   `DefausserJusquaUneAmeliorationDuDeckSignature`, reservee a Zombie Iron Man).
# - « Zombie Magik gets +1 ATK » : `01074` Inspired (pack `core`) : `AbilityFactory.GiveKeywordToAttached(
#   Ally, thwart=1, attack=1)` — MEME fabrique pour le bonus de statistique statique tant que l'attachement
#   est en jeu. Difference avec `01074` : la cible n'est pas generique (« an ally »/« your hero »), le texte
#   NOMME Zombie Magik -- `GiveKeywordToAttached` applique de toute facon le bonus a QUELLE QUE SOIT la face a
#   laquelle `this` est reellement attachee (`this.GetBindFace()`, asset_helper.py), jamais a une autre, donc
#   `card_finder=None` suffirait seul ; `CardFinder(name="Zombie Magik")` est ajoute en PLUS par coherence
#   avec la restriction par nom deja posee sur le second effet (voir plus bas) et par securite si un bug
#   d'attache venait un jour a coller cette carte sur un autre Metazombie.
# - « Her attacks gain Piercing » : `hg019` Necrotic Repulsors (« His attacks gain Piercing », MEME texte au
#   pronom pres, MEME deck signature, MEME position carte 1/N) : `AbilityFactory.UnitAttackGainKeyword(
#   CardFinder(name="Zombie Iron Man"), piercing=True)`. Modele repris au mot pres, seul le nom change :
#   `CardFinder(name="Zombie Magik")`. Cas officiel source de la fabrique elle-meme deja cite par hg019 :
#   `sk077`/`sk078`/`sk076` * Empress R'Klll (Ability vivant sur l'attaquant) et `27078` "Now We're Angry!"
#   (pack `sm/venom`, Ability vivant sur l'ATTACHEMENT comme ici, cible NOMMEE plutot que "This").
# - « Hero Action: Spend 3 resources → discard this card » : `hg019`/`hg020` (meme deck du scenario, meme
#   patron « Spend N resources -> discard this card », cout NU sans icone de ressource) : `
#   AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("N"))` ; modele officiel
#   source deja identifie par hg019 : `sq017` Revealed Identity (« Spend 2 resources of any type », cout
#   generique `Cost("2")`, pas de qualificatif colore). Ici seul le montant change : `Cost("3")`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Magik » -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Magik",
#   card_type=Villain))` (voir CARTES DE REFERENCE).
# « Zombie Magik gets +1 ATK » -> `AbilityFactory.GiveKeywordToAttached(CardFinder(name="Zombie Magik"),
#   attack=1)`. Bonus permanent tant que la carte reste attachee (retire automatiquement si Soulsword quitte
#   le jeu, nature de `GiveKeywordToAttached`/`WhileValid` -- pas de nettoyage manuel a coder).
# « HER attacks gain Piercing » -> `AbilityFactory.UnitAttackGainKeyword(CardFinder(name="Zombie Magik"),
#   piercing=True)`. « Her » = Zombie Magik (antecedent de la phrase precedente), jamais un autre Metazombie :
#   `CardFinder(name=...)` filtre par NOM exact, aucune attaque d'un AUTRE Metazombie (meme portant une
#   amelioration similaire) n'est touchee.
# « attacks GAIN Piercing » -> toutes ses attaques, pas seulement les attaques de base : `is_basic_attack`
#   laisse au defaut (`None`) de la fabrique = aucun filtre, comme `hg019`/`27078`.
# « HERO Action » -> `AbilityType.HeroAction`, pas `AbilityType.Action` (sous-type distinct, PROCESSUS-CARTE
#   etape 5).
# « Spend 3 resources » -> `.SetCost(Cost("3"))` (3 ressources, n'importe quel type, modele `sq017`/`hg019`).
# « → discard this card » -> `AbilityFactory.PlayerActionToDiscardThis`, qui defausse `effect.this` (Soulsword
#   elle-meme, PAS Zombie Magik) ; aucune action complementaire au-dela de la defausse (rien d'autre n'est
#   imprime apres).
#
# A CONFIRMER (reprend l'arbitrage deja pose sur hg019/20/21, meme deck du scenario, meme origine TTS) : le
# texte source (`data/cards_custom.json`, hg043) dit juste « Spend 3 resources », sans qualificatif « of any
# type ». Lecture retenue, identique a hg019-hg022 : « of any type » (cout generique `Cost("3")`), la version
# TTS/livret fan-made elidant systematiquement ce qualificatif partout dans ce scenario. Aucune regle ne
# depend du choix inverse ici non plus : ne bloque pas le script.
#
# Bloc nombres texte <-> code : « +1 ATK » -> `attack=1` ; « Spend 3 resources » -> `Cost("3")`. Aucune valeur
# dans `desc` de `data/cards_custom.json` (hg043 : `"desc": {}`, comme hg019) : les deux nombres n'existent
# QUE dans le texte imprime et ce script, aucun second endroit a recouper.


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Magik", card_type=Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            cible,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            cible,
            attack=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            cible,
            piercing=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3")),
    ]
