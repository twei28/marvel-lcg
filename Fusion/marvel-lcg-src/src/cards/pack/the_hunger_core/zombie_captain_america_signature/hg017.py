from . import *

# Avengers, Feast! — TRAITRISE (deck signature de Zombie Captain America, carte 2/3). Trait ATTACK.
# When Revealed: Each Metazombie in play activates against each player. Do not deal boost cards for these
# activations.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « activates » n'est PAS un mot-cle maison/officiel a fiche dediee (absent de
#   `docs/reference/mots-cles/README.md` comme entree a part) : c'est un terme de regle de base (une
#   activation de sbire/vilain = son attaque OU sa manigance, selon la forme du joueur vise), couvert par la
#   fabrique moteur `Enemy.DoActivate` elle-meme (voir plus bas), pas par une fiche a ouvrir.
# - [[boost]] (mots-cles/boost.md) : « Do not deal boost cards » = parametre `do_not_give_boost=True` de
#   `DoActivate`/`AttackProperty`/`SchemeProperty`. Rien a faire sur les ICONES de boost des Metazombies
#   eux-memes (elles ne sont jamais piochees comme carte de boost ici, le texte dit juste qu'on ne pioche PAS
#   la rencontre pour cette activation).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : mecanique de scenario « The Hunger Core ».
#   Rappel important : le jeton actif (« only one activates » en phase mechant normale) ne s'applique QU'A
#   l'activation automatique de la phase mechant native (hook `GettingVillainsToActivate`). Cette carte
#   declenche une activation EXPLICITE par une capacite (When Revealed), hors de ce hook : elle active donc
#   bien TOUS les Metazombies en jeu, jeton ou pas — la fiche ne documente aucune exception pour ce cas et
#   aucune ligne du livret ne restreint les activations DECLENCHEES PAR CARTE au seul Metazombie actif
#   (seule la phase mechant normale est concernee par la regle du jeton).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Each Metazombie in play » : helper DEJA EXISTANT du scenario, `Metazombies(effect)`
#   (`cards/pack/the_hunger_core/commun.py:81`) : « Les Metazombies VIVANTS en jeu, dans l'ordre d'entree
#   (gauche -> droite de la rangee) », filtre sur `v.HasTrait(TRAIT_METAZOMBIE)` parmi `Villains.All(effect)`.
#   Reutilise tel quel plutot que de refiltrer a la main (les Metazombies sont des `Villain`, page 3 du
#   livret : « A Metazombie is a villain for all purposes » — deja documente dans la fiche horde-metazombies).
# - « activates against each player » (pour UN SEUL vilain) : modele exact `shadowland/shadow_labyrinth/
#   sl039b.py` (« In expert mode, the villain activates against each player ») :
#   `Players.ForEachPlayer(effect, lambda joueur: vilain.DoActivate(joueur, effect))`. `DoActivate` choisit
#   lui-meme Attaque ou Manigance selon que le joueur vise est en forme Heros ou Alter-Ego — exactement ce que
#   recouvre « activates » (couvre les deux, meme lecon que `nt013`/`27158`/`hg012` : ne jamais la retreindre a
#   une Attaque seule).
# - « Do not deal boost cards for these activations » : parametre `do_not_give_boost=True` de `DoActivate`,
#   modele `gorr/gorr_the_god_butcher/gb020.py` (« Deal him no boost cards for this attack » ->
#   `vilain.DoActivate(joueur, effect, do_not_give_boost=True)`) et `cw/defenders/56187.py`
#   (`leader.DoActivate(player, effect, do_not_give_boost=True)`, boucle sur plusieurs entites/joueurs comme
#   ici).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « EACH Metazombie IN PLAY » -> `Metazombies(effect)`, PAS `Villains.All(effect)` brut (qui inclurait Le
#   Coeur, sans trait METAZOMBIE) ; un Metazombie deja vaincu PENDANT la resolution (ex. Reponse Forcee d'un
#   joueur) est revalide par `metazombie.IsInPlay()` avant chaque activation, cf. le meme garde-fou que
#   `DoActivateAgainstYouInternal` (enemies.py) applique a toute boucle d'activations multiples.
# « ACTIVATES against each player » -> `DoActivate`, PAS `DoAttackYou` seul : couvre Attaque (joueur en
#   forme Heros) ET Manigance (joueur en forme Alter-Ego), meme piege documente sur `hg012` (« ACTIVATES
#   couvre l'attaque ET la manigance »).
# « against EACH PLAYER » -> `Players.ForEachPlayer`, qui ne lit que les joueurs reellement dans la partie
#   (`Worlds.GetPlayers`, filtre deja sur `area_hero` non vide).
# « Do not deal boost cards for THESE activations » -> `do_not_give_boost=True` sur CHAQUE appel
#   `DoActivate`, aucune exception.
#
# A CONFIRMER (ordre de resolution, aucune regle imprimee ni aucune fiche ne le fixe) : la phrase « Each
# Metazombie ... activates against each player » a pour SUJET grammatical « Each Metazombie » — lecture
# retenue ici : chaque Metazombie (dans l'ordre d'entree en jeu, gauche -> droite) resout la totalite de ses
# activations contre chaque joueur (dans l'ordre des joueurs) avant de passer au Metazombie suivant. L'autre
# lecture possible (pour chaque joueur, chaque Metazombie s'active, comme le fait la regle NATIVE du jeton
# pour « both villains activate against each player » sur `tk006a`, ou le premier joueur choisit l'ordre
# entre deux entites simultanees contre le MEME joueur) change l'ordre mais, ici, aucun effet connu de ce
# scenario ne depend de cet ordre (aucun gain/perte conditionnel entre deux activations). A trancher a la
# verification groupee si une carte future rend cet ordre observable.


def GetAbilities() -> Sequence['Ability']:

    def festin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        for metazombie in Metazombies(effect):
            if Worlds.IsGameOver(effect):
                break

            def active_contre(joueur: 'Player', metazombie: 'Villain' = metazombie) -> None:
                if metazombie.IsInPlay():
                    metazombie.DoActivate(joueur, effect, do_not_give_boost=True)

            Players.ForEachPlayer(effect, active_contre)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            festin,
        ),
    ]
