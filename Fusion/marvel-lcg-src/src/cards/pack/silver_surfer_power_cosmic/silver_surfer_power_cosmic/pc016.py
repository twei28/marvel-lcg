from . import *

# Black Hole — SOUTIEN SIGNATURE. PLAYER ENVIRONMENT. POWER COSMIC. PLANET.
# SINGULARITY. Cout 3. (3/17)
#
# Texte imprime : « When this card enters play, choose a player. The villain
# and each minion engaged with that player arrive here and take 3 damage.
# At the start of the next player phase, remove this card from the game. »
#
# CARTES DE REFERENCE
#  - `bt010.py` Beast's Lab : `SetTarget(<fonction qui rend les identites de
#    joueurs>)` + `Players.ForEachTargets` pour « choose a player ».
#  - helpers `ArriverA`/`Departir` (__init__.py du pack).
#  - `player.GetEngagedMinions()` (player_get.py) + `Worlds.FindVillain`
#    (operate/worlds.py) pour « the villain and each minion engaged with
#    that player ».
#  - `AbilityFactory.AfterCardEnterPlay` pour « When this card enters play » ;
#    `AbilityFactory.WhenPlayerPhaseBegin` + `this.effect.RegisterTemp(...,
#    unregister_after_exec=True)` (modele pc004, degat de fin de phase) pour
#    « At the start of the NEXT player phase » (une seule fois, pas a
#    chaque phase pour toujours).
#  - `Faces.RemoveAllFromGame` (operate/faces.py) pour « remove this card
#    from the game ».
#
# DECISION UTILISATEUR (05/11/2026, QUESTIONS-AUTEUR.md Q2) : le texte
# imprime ne dit jamais que le mechant/les sbires envoyes ici REPARTENT --
# a la suppression de la carte, on les fait explicitement partir (Departir),
# sinon leur marqueur « a une planete » resterait bloque pour toujours (le
# mechant ne pourrait alors plus jamais attaquer). Seuls les personnages
# ENCORE marques ICI au moment de la suppression en partent (capture exacte
# de la liste envoyee a l'entree en jeu, pas un balayage de tout le plateau).
#
# TEXTE CONTRE CODE
#  « the villain AND EACH MINION engaged with that player » : le mechant
#    (peut etre absent si deja vaincu) + TOUS les sbires engages de ce
#    joueur precis (`GetEngagedMinions`), jamais ceux d'un autre joueur.
#  « take 3 damage » : chaque personnage envoye subit 3 degats, chacun pour
#    son propre compte (pas un degat unique partage).
#  « At the start of the NEXT player phase » : enregistrement a usage
#    unique, pas une capacite permanente.


def GetAbilities() -> Sequence['Ability']:

    def joueurs(effect: 'Effect') -> Sequence['AlterEgo|Hero']:
        return [p.GetIdentity() for p in Worlds.GetPlayers(effect)]

    def black_hole(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        if not effect.targets:
            return

        personnages_envoyes: List['CardFace'] = []

        def pour_ce_joueur(joueur: 'Player') -> None:
            cibles: List['CardFace'] = list(joueur.GetEngagedMinions())
            mechant = Worlds.FindVillain(effect)
            if mechant is not None:
                cibles.append(mechant)
            for cible in cibles:
                ArriverA(effect, cible, this)
                this.DealDamage([cible], 3, effect)
                personnages_envoyes.append(cible)

        Players.ForEachTargets(effect.targets, pour_ce_joueur)

        def retirer_de_la_partie(effect2: 'Effect', message2: 'Message.WhenPhaseBegin') -> None:
            Unused(message2)
            for personnage in personnages_envoyes:
                if EstÀUnePlanète(personnage) is this:
                    Departir(effect2, personnage)
            Faces.RemoveAllFromGame([this], effect2)

        this.effect.RegisterTemp(
            AbilityFactory.WhenPlayerPhaseBegin(
                AbilityType.NonKeyword,
                retirer_de_la_partie,
            ),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            black_hole,
        ).SetTarget(joueurs),
    ]
