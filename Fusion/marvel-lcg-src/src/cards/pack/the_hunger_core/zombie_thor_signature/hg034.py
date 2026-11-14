from . import *

# Bloodied Mjolnir — ATTACHEMENT (set signature Zombie Thor, carte 1/3). Traits WEAPON, ASGARD.
# Attach to Zombie Thor.
# Zombie Thor gets +1 ATK. His attacks gain Overkill and Piercing.
# Storm deals 1 additional damage to each ally.
# Hero Action: Spend 3 resources -> discard this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[overkill]] (mots-cles/overkill.md) : voie DYNAMIQUE (« this attack gains overkill » via
#   `message.GainOverKill(effect)`), pas la voie statique `overkill=True` d'une fabrique `DoAttack` (reservee
#   aux cartes JOUEUR, cf. note deja laissee par `hg022`/`hg009`, meme pack). Ici l'attache accorde le gain a
#   TOUTES les attaques de Zombie Thor tant qu'elle est en jeu -> `AbilityFactory.UnitAttackGainKeyword`.
# - [[piercing]] (mots-cles/piercing.md) : meme voie dynamique, `message.GainPiercing(effect)`, meme fabrique
#   que l'Overkill ci-dessus (elle accepte les deux parametres simultanement).
# - « Storm » : PAS un mot-cle maison a part — c'est le NOM PROPRE de la capacite deja imprimee sur Zombie Thor
#   lui-meme (`hg012`, « Storm — Forced Response: After Zombie Thor activates against a player, deal 1 damage
#   to each ally that player controls »), confirme par `grep` sur `data/cards_custom.json` (une seule autre
#   occurrence du mot « Storm », exactement ce texte, sur `hg012`). Cette carte CITE ce nom pour dire qu'elle
#   AJOUTE 1 degat a ce que « Storm » fait deja, pas qu'elle definit une nouvelle regle nommee « Storm » :
#   absent de `docs/reference/mots-cles/README.md`, rien a creer — a NE PAS confondre avec le mot-cle officiel
#   « Surge » ni avec le heros Tornade (Storm, pack X-Men), aucun rapport.
# - « Hero Action » : sous-type dedie de base (PROCESSUS-CARTE.md etape 5), pas une fiche `mots-cles/`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Attach to Zombie Thor. Zombie Thor gets +1 ATK. » (triplet attache + bonus d'ATQ en prose, PAS un badge
#   `desc` -- `desc` est vide `{}` pour `hg034` dans `cards_custom.json`) : modele EXACT `hg026` Endless Rage
#   (meme pack signature, meme scenario : « Attach to Zombie Hulk. Zombie Hulk gains Steady and gets +1 ATK »
#   -> `AttachToFaceWhenPutIntoPlay(cible) + *GiveKeywordToAttached(cible, steady=1, attack=1)`), ici sans le
#   Steady (pas imprime sur cette carte) : `*GiveKeywordToAttached(cible, attack=1)` seul.
# - « His attacks gain Overkill and Piercing » : modele EXACT `21103` * Proxima's Spear (« Attach to Proxima
#   Midnght. Proxima Midnight's attacks gain overkill and piercing » -> `AbilityFactory.UnitAttackGainKeyword(
#   CardFinder(name="Proxima Midnight"), overkill=True, piercing=True)`), et variante `hg022` Necrotic Unibeam
#   (meme pack, « His attacks gain Overkill » -> `UnitAttackGainKeyword("AttachedVillain", overkill=True)`) :
#   ici avec la MEME `CardFinder` que les autres abilities de cette carte (`cible`), par coherence avec le
#   style deja choisi par `hg026` (reutilisation d'un seul `CardFinder` nomme sur toutes les capacites d'une
#   attache, plutot que de melanger `CardFinder` et litteral `"AttachedVillain"` sur une seule carte).
# - « Storm deals 1 additional damage to each ally » : modele de PORTEE et de fabrique EXACT `hg012` Zombie
#   Thor lui-meme (meme declencheur, meme cible, meme fabrique : `AbilityFactory.AfterEnemyActivatesAgainstYou(
#   ForcedResponse, cible, op)` + `message.GetAgainstPlayer().GetControlAllies()` + `this.DealDamage(allies, 1,
#   effect)`), seule la carte PORTEUSE de l'ability change : `cible` (CardFinder Zombie Thor) au lieu de "This"
#   (hg012 EST Zombie Thor ; hg034 est une carte ATTACHEE distincte, qui doit donc nommer explicitement le
#   vilain plutot que de se designer elle-meme). Implementee comme une SECONDE reponse forcee independante,
#   greffee sur le MEME message (`Message.AfterEnemyActivationEnd`) que celle de `hg012` -- pas une modification
#   du code de `hg012` (interdit : fichier partage hors scope de cette tache) -- ce qui produit le meme total
#   observable (2 degats au lieu de 1 a chaque allie du joueur vise), en deux increments distincts plutot qu'un
#   seul. Modele de ce patron (« une attache ajoute un degat sur le MEME declencheur qu'une ability deja
#   imprimee sur son hote, sans toucher au script de l'hote ») : aucun exact trouve dans le depot a ce jour ;
#   le plus proche est `hg022` Necrotic Unibeam, qui AJOUTE un effet de degats sur un declencheur PARTAGE avec
#   une autre capacite de la meme attache (son propre gain d'Overkill), pas avec une carte separee -- principe
#   transposable (deux abilities independantes sur le meme message, effets additifs), **A CONFIRMER** en partie
#   reelle si jamais une carte du scenario reagit au NOMBRE de fois ou « Storm » degat (plutot qu'au total) ;
#   aucune carte connue a ce jour (hg001-hg033) ne le fait.
# - « Hero Action: Spend 3 resources -> discard this card » : modele EXACT `hg026` Endless Rage / `sf014`
#   Silver Samurai's Katana -> `PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("3"))`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Attach to Zombie Thor » -> `AttachToFaceWhenPutIntoPlay(cible)` -- nom UNIQUE au depot (`grep
#   "\"name\": \"Zombie Thor\"" data/cards.json data/cards_custom.json` : une seule occurrence), aucune etoile
#   a retirer (pas de `*` imprime sur cette carte).
# « Zombie Thor gets +1 ATK » -> `*GiveKeywordToAttached(cible, attack=1)`.
# « His attacks gain Overkill and Piercing » -> `UnitAttackGainKeyword(cible, overkill=True, piercing=True)`.
# « Storm deals 1 additional damage to each ally » -> `AfterEnemyActivatesAgainstYou(ForcedResponse, cible,
#   storm_plus)` avec `storm_plus` = `this.DealDamage(message.GetAgainstPlayer().GetControlAllies(), 1, effect)`.
# « Hero Action: Spend 3 resources -> discard this card » -> `PlayerActionToDiscardThis(HeroAction)
#   .SetCost(Cost("3"))`.
#
# ⚠ Mots-pieges :
#  - « His attacks », PAS « his activation »/« engages » (contrairement a « Storm », plus bas, qui elle COUVRE
#    aussi la manigance) : Overkill/Piercing seulement sur les ATTAQUES -> `UnitAttackGainKeyword`, pas de lien
#    avec `AfterEnemyActivatesAgainstYou`.
#  - « Storm deals 1 additional damage », PAS « Storm's attacks deal » : le degat supplementaire suit la
#    PORTEE de « Storm » telle qu'imprimee sur `hg012` (« ACTIVATES against a player », couvre attaque ET
#    manigance), pas seulement les attaques -- a NE PAS reduire a `AfterUnitAttackUnit` par analogie trompeuse
#    avec la ligne « His attacks gain... » juste au-dessus, qui ELLE est bien restreinte aux attaques.
#  - « to EACH ALLY » (sans « that player controls » explicite dans CETTE phrase, contrairement a `hg012`) :
#    le texte de `hg034` est elliptique parce qu'il complete « Storm », dont la portee complete (« each ally
#    THAT PLAYER controls ») reste celle de la capacite nommee -- pas « each ally in play » (portee de `hg016`
#    Thrown Shield, carte differente du meme recueil, ecartee ici volontairement).
#  - « additional » : s'AJOUTE au degat de `hg012` (1 + 1 = 2 au total par allie vise), ne le REMPLACE pas --
#    les deux abilities restent actives independamment, aucune ne doit lire/ecraser la valeur de l'autre.
#  - « gets +1 ATK » / « gain Overkill and Piercing » / le degat « Storm » supplementaire : bonus DYNAMIQUES
#    tant que l'attache est en jeu, retires automatiquement si elle est defaussee (meme mecanisme que `hg026`/
#    `hg022` : rien a coder pour la retombee a la defausse, native au triplet attache).
#  - Traits imprimes « WEAPON », « ASGARD » : purement declaratifs (`desc`), rien a coder pour eux.
#  - Aucune limite imprimee (« once per round »/« per attack »), aucun « unless »/« otherwise »/« if you
#    cannot » dans le texte : rien d'autre a coder.
#
# ⚠ Attaque/activation REELLE (DoActivate) dans un futur cas de test : ajouter la cle
# `"passer_sur_option": "Defense"` (bug deja rencontre sur `hg017`, a ne pas repeter).


def GetAbilities() -> Sequence['Ability']:

    cible = CardFinder(name="Zombie Thor", card_type=Villain)

    def storm_plus(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetAgainstPlayer()
        this.DealDamage(joueur.GetControlAllies(), 1, effect)

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
            overkill=True,
            piercing=True,
        ),
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            cible,
            storm_plus,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3")),
    ]
