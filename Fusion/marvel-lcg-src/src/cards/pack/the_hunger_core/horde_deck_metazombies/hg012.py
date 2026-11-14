from . import *

# Zombie Thor — METAZOMBIE (Horde deck). AVENGER. ASGARD. SCH 1. ATK 3. PV 13[per_hero].
# Storm — Forced Response: After Zombie Thor activates against a player, deal 1 damage to each ally that
# player controls.
#
# Cartes de reference :
#  - « After Zombie Thor ACTIVATES against a player » : `AbilityFactory.AfterEnemyActivatesAgainstYou(
#    ForcedResponse, "This", op)` (activate.py:93), modele `nt013` Terrax the Tamer (meme commentaire deja
#    laisse par ce pack : « ACTIVATES couvre l'attaque ET la manigance », a distinguer d'un filtre qui ne
#    couvrirait que l'une des deux) et `27158` Doctor Octopus (meme fabrique, meme forme a une cible pres).
#    Le modele le plus proche pour « contre UN JOUEUR » (donc pas forcement « contre VOUS » au sens propre
#    du mot) reste la MEME fabrique : elle porte deja `message.GetAgainstPlayer()` (sender_enemy.py:186),
#    qui donne le joueur reellement vise par CETTE activation precise -- l'anglais imprime « a player »
#    plutot que « you » uniquement parce que le texte d'un vilain/sbire PARLE a la table, pas a un joueur
#    fixe ; le moteur ne distingue pas les deux formulations (meme message, meme joueur resolu).
#  - « deal 1 damage to each ally that player controls » : `joueur.GetControlAllies()` (player_get.py:99,
#    liste les Allies CONTROLES par ce joueur precis, pas tous les allies de la table) + `this.DealDamage(
#    allies, 1, effect)` (degats natifs HORS attaque, card_face.py:950), modele EXACT `24044` Boomerang
#    (« After Boomerang attacks you, deal 1 damage to each ally you control » -> `player.GetControlAllies()`
#    puis `this.DealDamage(cible, 1, effect)`), seule la source du joueur differe (`GetAgainstPlayer()` ici
#    au lieu de `GetToPlayer()` sur un message d'attaque).
#
# ⚠ Mots-pieges :
#  - « Storm » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel (absent de
#    `docs/reference/mots-cles/README.md`, aucune autre carte du moteur ne le reprend comme mot-cle) : rien
#    a ouvrir avant de coder, le texte qui suit EST la regle complete.
#  - « ACTIVATES », pas « attacks » : couvre AUSSI la manigance (forme alter-ego). Utiliser
#    `AfterEnemyActivatesAgainstYou`/`Message.AfterEnemyActivationEnd`, jamais `AfterUnitAttackUnit` seul,
#    sous peine d'amputer la carte de la moitie de ses declenchements (meme piege deja documente sur nt013).
#  - « against A PLAYER », generique, pas « you » au sens d'un joueur fixe par le code : le joueur resolu
#    est celui que `message.GetAgainstPlayer()` rend pour CETTE activation, jamais un joueur en dur.
#  - « to EACH ally THAT PLAYER controls » : uniquement les allies du joueur VISE par l'activation (celui
#    qui a ete active contre), jamais tous les allies de la table ni ceux d'un autre joueur -- important en
#    multijoueur, ou `GetControlAllies()` est bien appele sur `message.GetAgainstPlayer()`, pas sur un
#    joueur quelconque (ex. `world.GetCurrentPlayer()`, qui pourrait differer en de rares cas de capacite
#    annexe deplacant l'activation).
#  - « deal 1 damage », SANS lien avec les degats de l'attaque elle-meme : ce sont des degats directs,
#    indifferents a Toughness/Shielded/reduction eventuelle de l'attaque de Thor, et qui ne touchent PAS
#    l'identite du joueur vise (le texte dit « each ally », jamais « each character » ni « you ») -- a NE
#    PAS confondre avec `18746` Radioactive Man (« deal 1 damage to each CHARACTER you control »), modele
#    ecarte volontairement car il inclurait l'identite, que cette carte ne vise pas.
#  - « deal 1 damage », SANS condition sur le nombre d'allies : `DealDamage` sur une liste vide (joueur sans
#    allie) ne fait rien (natif, pas de garde manuelle a ecrire) ; sur plusieurs allies, CHACUN recoit
#    separement 1 degat (pas 1 degat partage), comme sur le modele `24044` Boomerang.


def GetAbilities() -> Sequence['Ability']:

    def storm(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Villain)
        joueur = message.GetAgainstPlayer()
        this.DealDamage(joueur.GetControlAllies(), 1, effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            storm,
        ),
    ]
