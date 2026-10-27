from . import *

# Teleportation Disc — TRAITRISE (deck signature de Zombie Magik, carte 2/3). Trait ATTACK.
# When Revealed: Zombie Magik activates against each player. Do not deal boost cards for these
# activations.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « activates » n'est PAS un mot-cle maison/officiel a fiche dediee (absent de
#   `docs/reference/mots-cles/README.md` comme entree a part) : terme de regle de base (une activation de
#   sbire/vilain = son attaque OU sa manigance, selon la forme du joueur vise), couvert par la fabrique
#   moteur `Villain.DoActivate` elle-meme, pas par une fiche a ouvrir. Meme lecture que `hg012` Zombie Thor,
#   `hg017` Avengers, Feast! et `hg023` Hunger Protocol : ne jamais la restreindre a une Attaque seule.
# - [[boost]] (mots-cles/boost.md) : « Do not deal boost cards » = parametre `do_not_give_boost=True` de
#   `DoActivate`. Rien a faire sur les ICONES de boost de Zombie Magik elle-meme (jamais piochee comme
#   carte de boost ici : le texte dit qu'on ne pioche pas la rencontre pour CETTE activation).
# - [[horde-metazombies]] (mots-cles/horde-metazombies.md) : mecanique de scenario « The Hunger Core ».
#   Rappel important (deja documente sur `hg017`) : le jeton actif (« only one activates » en phase mechant
#   normale) ne s'applique QU'A l'activation automatique de la phase mechant native
#   (`GettingVillainsToActivate`). Cette carte declenche une activation EXPLICITE par une capacite (When
#   Revealed), hors de ce hook : elle active donc Zombie Magik qu'elle porte ou non le jeton.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Zombie Magik activates against each player » (UN SEUL vilain NOMME, boucle sur TOUS les joueurs) :
#   fusion de deux modeles deja en place dans ce meme scenario -
#   * `hg017` Avengers, Feast! pour la boucle `Players.ForEachPlayer(effect, lambda joueur:
#     metazombie.DoActivate(joueur, effect, do_not_give_boost=True))` (texte « against EACH player », pas
#     « against you » comme `hg012`/`hg023`) ;
#   * `hg023` Hunger Protocol pour l'identification du Metazombie par son NOM PROPRE (pas « chaque
#     Metazombie », pas « le Metazombie actif ») : `next((v for v in Metazombies(effect) if
#     v.IsName("Zombie Magik")), None)`, modele `commun.LeCoeur` (`v.IsName(CORE)`).
# - « Do not deal boost cards for these activations » : parametre `do_not_give_boost=True` de `DoActivate`,
#   meme modele que `hg017` (`gorr/gorr_the_god_butcher/gb020.py`, `cw/defenders/56187.py`).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « Zombie Magik activates » -> sujet = LE Metazombie nomme (pas « each Metazombie in play » comme `hg017`,
#   pas « the active Metazombie ») : identification par nom parmi `Metazombies(effect)` (liste deja filtree
#   sur le trait METAZOMBIE et sur « vivant/en jeu »), garde defensive si introuvable (voir fiche
#   horde-metazombies ci-dessous : ne devrait pas arriver en pratique, cette carte n'est revelee que depuis
#   le deck signature DE Zombie Magik, donc lie a SA Card, mais rien dans le livret ne garantit ce lien pour
#   une revelation future hors de ce chemin, ex. un effet qui piocherait une signature card au hasard).
# « ACTIVATES against each player » -> `DoActivate`, PAS `DoAttackYou` seul : couvre Attaque (joueur en
#   forme Heros) ET Manigance (joueur en forme Alter-Ego), meme piege documente sur `hg012`/`hg017`.
# « against EACH PLAYER » -> `Players.ForEachPlayer`, qui ne lit que les joueurs reellement dans la partie
#   (`Worlds.GetPlayers`, filtre deja sur `area_hero` non vide).
# « Do not deal boost cards for THESE activations » -> `do_not_give_boost=True` sur CHAQUE appel
#   `DoActivate`, aucune exception.
# Pas de clause « if you cannot »/« otherwise » sur cette carte (contrairement a `hg023`) : pas de branche
#   Surge a coder, l'activation ne peut pas « echouer » au sens de cette carte.
#
# A CONFIRMER (aucune regle imprimee ni aucune fiche ne le fixe) : l'ORDRE des joueurs lorsque Zombie Magik
# active contre plusieurs d'entre eux n'est precise nulle part dans le livret. Lecture retenue ici (identique
# a `hg017`) : `Players.ForEachPlayer` resout dans l'ordre natif des joueurs (`Worlds.GetPlayers`). Aucun
# effet connu de ce scenario ne depend de cet ordre. A trancher a la verification groupee si une carte future
# le rend observable.


def GetAbilities() -> Sequence['Ability']:

    def disque(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)

        magik = next((v for v in Metazombies(effect) if v.IsName("Zombie Magik")), None)
        if magik is None:
            # Garde defensive (voir fiche horde-metazombies ci-dessus) : ne devrait pas arriver en pratique.
            # Aucune clause « if you cannot » n'est imprimee sur cette carte : rien d'autre a faire.
            return

        def active_contre(joueur: 'Player') -> None:
            if Worlds.IsGameOver(effect):
                return
            if magik.IsInPlay():
                magik.DoActivate(joueur, effect, do_not_give_boost=True)

        Players.ForEachPlayer(effect, active_contre)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            disque,
        ),
    ]
