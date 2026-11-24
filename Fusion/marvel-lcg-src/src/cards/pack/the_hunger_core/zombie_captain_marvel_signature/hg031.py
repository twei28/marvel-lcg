from . import *

# VERIFIE (27/10/2026, passe de fusion hg028-hg076) : `commun.DECKS_SIGNATURE["Zombie Captain Marvel"]` =
# [hg030, hg031, hg032, hg033, hg033, hg033] N'EST PAS une erreur de recopie. Le livret (p. 4, repris en tete
# de `DECKS_SIGNATURE` dans commun.py) dit « 3 cards; 5 for Zombie Iron Man and 6 for Zombie Captain Marvel »,
# et `data/encounter_sets/the_hunger_core_sig_zombie_captain_marvel.json` liste hg033 en TROIS exemplaires :
# 4 cartes distinctes, 6 cartes au total. Liste laissee telle quelle.
#
# Photon Fist — ATTACHEMENT (set signature Zombie Captain Marvel, carte 2/4). Trait COSMIC (saveur, pas de
# mot-cle moteur).
# Attach to Zombie Captain Marvel.
# Her attacks gain Overkill.
# Hero Action: Spend 2 resources → discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[overkill]] (mots-cles/overkill.md) : propriete booleenne de l'attaque. Deux voies possibles (fiche,
#   §Mecanisme moteur) : statique (`overkill=True` d'une fabrique `DoAttack`, reservee aux cartes JOUEUR) ou
#   DYNAMIQUE (`message.GainOverKill(effect)` via `AbilityFactory.UnitAttackGainKeyword`). Ici voie dynamique,
#   exactement comme `hg019` Necrotic Repulsors (meme pack, meme forme de phrase « <Nom>'s attacks gain
#   <mot-cle> », mais Piercing au lieu d'Overkill) et `hg022` Necrotic Unibeam (Overkill, meme deck Iron Man).
#   `UnitAttackGainKeyword` pose une Ability `NonKeyword` qui ecoute `Message.CheckIfAttackMessageHasKeyword`
#   et appelle `message.GainOverKill(effect)` des que l'attaquant correspond a la cible fournie — l'Ability
#   vit sur l'ATTACHEMENT (`hg031`), pas sur Zombie Captain Marvel, comme `hg019`/`hg022`/`27078`.
# - « Hero Action » : sous-type dedie de base (PROCESSUS-CARTE.md etape 5, « Hero Response/Hero Action :
#   sous-type dedie, pas le type nu »), absent de `docs/reference/mots-cles/README.md` -- rien a ouvrir,
#   juste choisir `AbilityType.HeroAction`.
# - « Attach to <nom> » : pas un mot-cle, regle de base des ameliorations (`AttachToFaceWhenPutIntoPlay`),
#   deja documentee en commentaire sur hg007-hg030.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Point capital (different d'`hg019`/`hg022`, meme mecanique Overkill mais DIFFERENT chemin d'attache) :
#   Zombie Captain Marvel (`hg011`) n'imprime AUCUN texte « discard cards from her signature deck until an
#   attachment is discarded and attach it to her » -- contrairement a Zombie Iron Man (`hg008`), qui EST le
#   seul Metazombie a porter ce mecanisme explicite (`commun.DefausserJusquaUneAmeliorationDuDeckSignature`,
#   appelee UNIQUEMENT par `hg008` et par sa propre carte signature `hg023`). Les cartes du deck signature de
#   Zombie Captain Marvel (comme celles de Zombie Captain America, Zombie Hulk, Zombie Spider-Man...) ne
#   sortent du deck signature que par la voie GENERIQUE : `commun.RevelerLeDessusDuDeckSignature` (appelee
#   sur `LeMetazombieActif(effect)`), qui `Reveal()` la carte normalement -- flux standard
#   Reveal -> PutIntoPlay -> `Message.WhenCardPutIntoPlay` pour une Attachment, EXACTEMENT comme n'importe
#   quelle amelioration revelee depuis le deck de rencontre officiel. C'est pourquoi `hg018` Dented Vibranium
#   Shield (Captain America, meme famille de carte : Attachment + deck signature generique, sans mecanisme
#   de pioche dediee sur son Metazombie) ET `hg026` Endless Rage (Hulk, meme famille) posent bien un
#   `AbilityFactory.AttachToFaceWhenPutIntoPlay`, modele retenu ICI -- a l'inverse de `hg019`/`hg022` (Iron
#   Man) qui n'en posent AUCUN, puisque leur attache passe par le canal prive
#   `DefausserJusquaUneAmeliorationDuDeckSignature` et n'est jamais revelee via le flux normal. Zombie
#   Captain Marvel est EN JEU au moment ou son propre deck signature est consulte (deck lie a sa propre
#   `Card`, `commun._DeckSignatureAttr`), donc la cible de l'attache est quasi garantie en pratique (meme
#   lecture que `hg026`) ; si jamais l'attache echoue (Metazombie deja vaincu), le filet natif du type
#   Attachment (`game/card/face/card_type/attachment.py`, defausse si `PutIntoPlay` echoue) s'applique sans
#   garde supplementaire -- aucune clause « if you cannot » n'est imprimee sur cette carte.
# - « Attach to Zombie Captain Marvel » -> `CardFinder(name="Zombie Captain Marvel", card_type=Villain)`,
#   modele exact `hg026` Endless Rage (`CardFinder(name="Zombie Hulk", card_type=Villain)`) : nom UNIQUE au
#   depot (`grep '"name": "Zombie Captain Marvel"' data/cards.json data/cards_custom.json` : une seule
#   occurrence, dans `cards_custom.json`), aucune collision avec le heros officiel « Captain Marvel » (nom
#   different).
# - « Her attacks gain Overkill » -> `AbilityFactory.UnitAttackGainKeyword(cible, overkill=True)`, cible =
#   le MEME `CardFinder` que l'attache (coherence avec `hg019`, qui emploie `CardFinder(name="Zombie Iron
#   Man")` pour l'attaquant plutot que le literal `"AttachedVillain"` -- ce dernier n'est utilise que par
#   `hg022`, dont l'attache ne passe jamais par `AttachToFaceWhenPutIntoPlay` et n'a donc pas de `CardFinder`
#   nomme deja pose ailleurs dans le script). `target` laisse a `None` (defaut) : aucune cible imprimee,
#   « her attacks » couvre toutes ses attaques quelle que soit la cible, comme `hg019`/`hg022`.
# - « Hero Action: Spend 2 resources → discard this card » : chiffre NU, aucune icone de ressource precisee
#   -> `Cost("2")` (n'importe quel type), modele `hg018`/`hg026` (meme famille « Spend N resources -> discard
#   this card » sans qualificatif « (any player) » ni icone coloree) -> `AbilityFactory.
#   PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("2"))`. Pas de `.AnyPlayerCanDoThis()` :
#   le texte imprime ne porte pas « (any player) », a la difference de `hg027` Rotten Web.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5, mots-pieges)
#
# « Attach to Zombie Captain Marvel » -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(cible)`. Hook REEL :
#   `AttachToFaceWhenPutIntoPlayInternal` (asset.py:153) ecoute `Message.WhenCardPutIntoPlay`, envoye par le
#   flux standard de revelation d'une Attachment (`CardFace.Reveal` -> entree en jeu -> `PutIntoPlay`),
#   jamais par `commun.DefausserJusquaUneAmeliorationDuDeckSignature` (canal prive d'Iron Man uniquement,
#   sans objet ici).
# « HER attacks gain Overkill » -> `AbilityFactory.UnitAttackGainKeyword(cible, overkill=True)`. « Her » =
#   Zombie Captain Marvel (antecedent de la phrase precedente « Attach to Zombie Captain Marvel »), jamais un
#   autre Metazombie : `CardFinder(name=...)` filtre par NOM exact, donc aucune attaque d'un AUTRE
#   Metazombie (meme Zombie Iron Man portant une amelioration Overkill similaire, `hg022`) n'est touchee.
# « attacks GAIN Overkill » -> toutes ses attaques, pas seulement ses attaques de base : `is_basic_attack`
#   laisse a `None` (defaut de la fabrique) = aucun filtre, comme `hg019`/`hg022`.
# « HERO Action » -> `AbilityType.HeroAction`, pas `AbilityType.Action` (sous-type distinct, PROCESSUS-CARTE
#   etape 5).
# « Spend 2 resources » -> `.SetCost(Cost("2"))` (2 ressources, n'importe quel type, modele `hg018`/`hg026`).
# « → discard this card » -> `AbilityFactory.PlayerActionToDiscardThis`, qui defausse `effect.this` (cette
#   carte elle-meme, PAS Zombie Captain Marvel) ; aucune action complementaire au-dela de la defausse (pas
#   de degats/cout annexe imprime, contrairement a `hg022` qui ajoute « take 1 damage » -- absent ici).
# Trait imprime « COSMIC » : trait DE SAVEUR (meme statut que sur `hg030` Rotten Binary, meme set), rien a
#   coder pour lui.
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# « Spend 2 resources » (texte imprime, `data/cards_custom.json` hg031) <-> `Cost("2")`. Une seule valeur
# numerique sur cette carte (Overkill est une propriete booleenne, pas un montant), verifiee, OK.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Aucun point ambigu identifie sur le TEXTE de cette carte : trois phrases courtes, chacune avec un modele
# deja present dans le moteur sur ce meme scenario (`hg018`/`hg026` pour l'attache + le cout de defausse,
# `hg019`/`hg022` pour le gain dynamique d'Overkill). (Le triple `hg033` de `commun.DECKS_SIGNATURE["Zombie
# Captain Marvel"]` est voulu : livret « 6 for Zombie Captain Marvel », voir l'en-tete de ce fichier.)


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Captain Marvel", card_type=Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            cible,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            cible,
            overkill=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2")),
    ]
