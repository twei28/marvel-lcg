from . import *

# Endless Rage — ATTACHEMENT (set signature de Zombie Hulk, carte 3/3, derniere du set). Trait CONDITION.
# Attach to Zombie Hulk.
# Zombie Hulk gains Steady and gets +1 ATK.
# Hero Action: Spend 3 resources -> discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[steady]] (mots-cles/steady.md) : mot-cle normalement NATIF (`desc.Steady`, aucun script si imprime sur
#   la carte elle-meme), mais ici c'est une ATTACHE qui l'OCTROIE a une AUTRE carte (Zombie Hulk) : la voie
#   dynamique s'impose, `AbilityFactory.GiveKeywordToAttached(..., steady=1)` (fiche, derniere ligne « si une
#   future carte cumule Steady avec une capacite imprimee distincte » -- exactement ce cas). Modele EXACT
#   `ld007` Reaver Commander (pack lady_deathstrike, « Attach to Lady Deathstrike. Lady Deathstrike gains
#   steady » -> `*AbilityFactory.GiveKeywordToAttached(Enemy, steady=1)`).
# - « Hero Action » : sous-type dedie de base (PROCESSUS-CARTE.md etape 5, « Hero Response/Hero Action : sous-
#   type dedie, pas le type nu »), pas une fiche de `mots-cles/` (absent de `README.md`, c'est une regle de
#   base du jeu, pas un mot-cle imprime sur une carte) : `AbilityType.HeroAction`, aucune fiche a ouvrir.
# - « +1 ATK » : ici ecrit EN PROSE dans le texte imprime de l'attache (pas un badge chiffre dans `desc`, qui
#   est vide pour `hg026` dans `cards_custom.json`) : contrairement a `27147`/`gs083` (badge natif + mot-cle
#   d'attaque separe), le bonus d'ATQ fait partie de la MEME phrase que Steady et doit donc etre octroye par
#   le MEME helper dynamique (`attack=1` sur le meme appel `GiveKeywordToAttached`, qui accepte les deux
#   parametres simultanement -- `game/ability/factory/asset.py` / `asset_helper.py`).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : cette carte est elle-meme une carte du deck
#   signature de Zombie Hulk (`commun.DECKS_SIGNATURE["Zombie Hulk"]` contient `hg026`, en derniere position),
#   revelee seulement quand son propre deck signature est consulte (`commun.RevelerLeDessusDuDeckSignature`,
#   appelee sur `LeMetazombieActif(effect)` -- cf. `hg046` Metazombie Power!, pas encore ecrite). Zombie Hulk
#   est donc EN JEU au moment ou cette carte se revele (son deck signature n'existe que lie a sa propre
#   `Card`, `commun._DeckSignatureAttr`), ce qui rend la cible de l'attache quasi garantie en pratique -- voir
#   piege plus bas sur le filet natif en cas d'echec malgre tout.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to Zombie Hulk. Zombie Hulk gains Steady and gets +1 ATK. » (triplet attache + capacite passive
#   dynamique) : modele EXACT `ld007` Reaver Commander (`AttachToFaceWhenPutIntoPlay(CardFinder(...)) +
#   *GiveKeywordToAttached(..., steady=1)`), et `sk148` Electricity Projection (Paibok, meme triplet avec
#   `retaliate=1` au lieu de `steady`) pour la variante « nom du vilain en dur, card_type=Villain ».
# - « Hero Action: Spend 3 resources -> discard this card » (chiffre NU, aucune icone de ressource precise,
#   donc N'IMPORTE quel type) : modele `sf014` Silver Samurai's Katana (« Spend 3 resources of any type ->
#   discard this card » -> `PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("3"))`,
#   `element/cost.py:35-41` -- un chiffre dans `Cost` ne demande qu'un NOMBRE de ressources, toutes couleurs
#   confondues, par opposition a une lettre qui imposerait une couleur). `hg018` Dented Vibranium Shield
#   (texte « Spend 2 resources -> discard this card », meme famille sur ce set) confirme la meme lecture.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Hulk » -> `AttachToFaceWhenPutIntoPlay(CardFinder(name="Zombie Hulk", card_type=Villain))`
#   -- nom UNIQUE au depot (`grep "\"name\": \"Zombie Hulk\"" data/cards.json data/cards_custom.json` : une
#   seule occurrence), aucune etoile a retirer (piege `sf014`, sans objet ici : pas de `*` imprime).
# « Zombie Hulk GAINS Steady AND gets +1 ATK » -> UN SEUL appel `GiveKeywordToAttached(..., steady=1,
#   attack=1)` sur le MEME `CardFinder`, pas deux appels distincts ni deux ablities separees : les deux
#   bonus partagent la meme condition d'attache (celle-ci meme), exactement comme `GiveKeywordToAttachWhenApply
#   ThisInternal` (`asset_helper.py`) les applique ensemble via `face.Gain(..., steady=.., attack=..)`.
# « Hero Action: Spend 3 resources -> discard this card » -> `PlayerActionToDiscardThis(AbilityType.HeroAction)
#   .SetCost(Cost("3"))` ; pas de qualificatif « (any player) » imprime sur CETTE carte (a la difference de
#   `hg027` Rotten Web, « Hero Action (any player) ») -> PAS de `.AnyPlayerCanDoThis()` : seul le joueur
#   normalement habilite (modele par defaut de la fabrique, identique a `gs083`/`ld007`/`sf014`, aucun des
#   trois n'appelle `AnyPlayerCanDoThis()` non plus) peut defausser la carte.
#
# ⚠ Mots-pieges :
#  - Si la revelation echoue a attacher (Zombie Hulk deja vaincu/absent au moment precis de la revelation,
#    cas defensif deja documente par `hg023` comme non garanti par le livret) : le filet NATIF du type
#    Attachment (`game/card/face/card_type/attachment.py`, `OnWhenCardRevealed` -> si `PutIntoPlay` echoue,
#    `Faces.DiscardAll`) s'applique tel quel, SANS garde supplementaire a coder ici -- aucune clause « if you
#    cannot » n'est imprimee sur cette carte (contrairement a `hg023`/`hg008`), donc rien a brancher sur ce
#    cas, qui n'a d'ailleurs aucun effet observable connu dans ce scenario (la carte va alors a la defausse de
#    rencontre generique au lieu du fond du deck signature -- ecart theorique, a verifier en partie reelle si
#    jamais observe).
#  - « gets +1 ATK » : bonus DYNAMIQUE tant que l'attache est en jeu (retire automatiquement si l'attache est
#    defaussee, via le meme mecanisme `WhileValid`/`GiveKeywordToAttached` que Steady) -- pas un bonus permanent
#    pose une fois pour toutes.
#  - Trait imprime « CONDITION » : trait de carte (catégorisation), pas un mot-cle moteur a part -- rien a
#    coder pour lui, comme `hg027` Rotten Web (meme trait sur une autre attache du scenario).


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Hulk", card_type=Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            cible,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            cible,
            steady=1,
            attack=1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3")),
    ]
