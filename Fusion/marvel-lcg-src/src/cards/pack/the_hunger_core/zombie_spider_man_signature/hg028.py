from . import *

# Dead Spider-Sense — TRAITRISE (deck signature de Zombie Spider-Man, carte 2/3). Trait ATTACK.
# When Revealed: Zombie Spider-Man activates against the player with the most cards in hand. If tied, he
# activates against you.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « activates » n'est PAS un mot-cle maison/officiel a fiche dediee (absent de
#   `docs/reference/mots-cles/README.md`) : terme de regle de base, couvert par la fabrique moteur
#   `Enemy.DoActivate` elle-meme (choisit Attaque ou Manigance selon la forme du joueur vise) -- deja constate
#   mot pour mot sur `hg012`/`hg014`/`hg015`/`hg017`, meme pack.
# - « the player with the most cards in hand. If tied, he activates against you » : AUCUN mot-cle ni fabrique
#   dediee trouve dans tout le depot (grep exhaustif sur « most » + « hand », et sur « tied »/« tie » : zero
#   resultat ailleurs que ce fichier) -- la comparaison et le partage de match nul sont donc ecrits a la main
#   ici, sans module `AbilityFactory` specialise. Rien a ouvrir dans `mots-cles/` : ce n'est pas un mot-cle
#   imprime, c'est une clause de ciblage en langage naturel.
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : mecanique de scenario « The Hunger Core ». Le
#   jeton actif (« only one activates ») ne s'applique QU'A l'activation automatique de la phase mechant
#   native (hook `GettingVillainsToActivate`) -- cette carte declenche une activation EXPLICITE par une
#   capacite (When Revealed), hors de ce hook, donc sans lien avec le jeton (meme constat deja fait sur hg017).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Zombie Spider-Man » (le Metazombie, carte `hg010`, `commun.CARD_ID_HORDE["Zombie Spider-Man"]`) retrouve
#   PAR NOM : modele exact `night_thrasher_nemesis/22031` Old Rivals (`Worlds.FindCardOnField(effect,
#   name="Gamora")`) -- rend `None` si la carte n'est pas actuellement en jeu (elle peut etre dans le Horde
#   deck ou la defausse, seuls 3 Metazombies sur 9 sont en jeu a la fois, page 3 du livret). Contrairement a
#   `hg020`/`hg021` (meme pack, qui passent par `CardFinder(name="Zombie Spider-Man")` a l'INTERIEUR d'une
#   fabrique `AttachToFaceWhenPutIntoPlay`/`GiveKeywordToAttached`), ce script a besoin de la carte elle-meme
#   en main pour lui appeler `DoActivate` -- `Worlds.FindCardOnField` est le bon outil pour un lookup direct.
# - « activates against <un joueur choisi par une regle> » (pour UN SEUL vilain, contre UN SEUL joueur) :
#   modele structurel `hg017` Avengers, Feast! (meme pack : `metazombie.DoActivate(joueur, effect)`) et
#   `shadow_labyrinth/sl039b.py` (« activates against each player » -> boucle sur `DoActivate`) ; ici une
#   seule cible (pas une boucle sur tous les joueurs), donc un seul appel `villain.DoActivate(cible, effect)`.
#   `DoActivate` choisit lui-meme Attaque ou Manigance selon la forme (Heros/Alter-Ego) de `cible` -- exactement
#   ce que recouvre « activates » (couvre les deux, meme lecon que `nt013`/`27158`/`hg012`/`hg014`/`hg015`).
# - « the player with the most cards in hand » : taille de main lue par `joueur.hand_cards.GetSize()`
#   (`game/deck/deck.py:140`), modele `sm/personal_nightmare/27156.py`/`27157.py` (`player.hand_cards.GetSize()`)
#   -- comparee ici entre TOUS les joueurs de la partie (`Worlds.GetPlayers(effect)`, modele `players.py:
#   ForEachPlayer`, qui ne lit que les joueurs reellement dans la partie), pas seulement le joueur revele.
# - « If tied, he activates against you » : « you » = le joueur a qui CETTE carte a ete revelee, c-a-d
#   `message.GetToPlayer()` -- modele exact `night_thrasher_nemesis/22031` Old Rivals (meme message
#   `Message.WhenCardRevealed`, meme appel pour designer « you » dans le texte d'une Traitrise).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique).
# « Zombie Spider-Man » -> `Worlds.FindCardOnField(effect, name="Zombie Spider-Man", card_type=Villain)`. Si
#   `None` (Metazombie pas actuellement en jeu), rien ne se passe -- garde explicite, aucune activation
#   fantome sur un Villain absent du plateau.
# « ACTIVATES against » -> `villain.DoActivate(cible, effect)`, PAS `DoAttackYou`/`DoAttack` seul : couvre
#   Attaque (cible en forme Heros) ET Manigance (cible en forme Alter-Ego), meme piege documente sur
#   `hg012`/`hg014`/`hg015`/`hg017` (« ACTIVATES couvre l'attaque ET la manigance »).
# « THE PLAYER with the MOST cards in hand » -> parmi `Worlds.GetPlayers(effect)`, on releve le maximum de
#   `joueur.hand_cards.GetSize()`, puis la liste des joueurs qui atteignent EXACTEMENT ce maximum.
# « If TIED » -> s'il y a plus d'UN joueur a ce maximum (deux ou plus a egalite, « you » inclus ou pas), la
#   regle de « the player with the most » ne designe personne de UNIQUE : la phrase suivante prend le relais.
# « he activates against YOU » -> dans ce cas (et SEULEMENT dans ce cas), la cible devient
#   `message.GetToPlayer()`, le joueur a qui cette Traitrise a ete revelee -- pas un joueur fixe ni le premier
#   de la liste des a-egalite.
#
# A CONFIRMER : aucune autre carte du depot ne compare le nombre de cartes en main ENTRE joueurs pour choisir
# une cible d'activation (grep exhaustif « most »+« hand » et « tied »/« tie » : zero resultat ailleurs) --
# lecture retenue, au mot pres du texte imprime : maximum strict, departage systematique vers le joueur
# revele en cas d'egalite (quel que soit le nombre de joueurs a egalite, y compris si « vous » en faites
# partie). Aucune autre lecture plausible du texte imprime n'a ete identifiee.
#
# Bloc nombres texte <-> code : aucune valeur numerique imprimee sur cette carte (ni `desc`, ni coefficient
# dans le script) -- rien a verifier a l'etape 6.


def GetAbilities() -> Sequence['Ability']:

    def dead_spider_sense(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        villain = Worlds.FindCardOnField(effect, name="Zombie Spider-Man", card_type=Villain)
        if villain is None:
            return

        joueurs = Worlds.GetPlayers(effect)
        if not joueurs:
            return

        plus_grande_main = max(joueur.hand_cards.GetSize() for joueur in joueurs)
        a_egalite = [joueur for joueur in joueurs if joueur.hand_cards.GetSize() == plus_grande_main]

        if len(a_egalite) == 1:
            cible = a_egalite[0]
        else:
            cible = message.GetToPlayer()

        villain.DoActivate(cible, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            dead_spider_sense,
        ),
    ]
