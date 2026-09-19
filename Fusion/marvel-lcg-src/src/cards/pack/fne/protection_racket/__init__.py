from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Protection Racket : CHAQUE joueur a son complot principal dans son aire de
# jeu (livret mc60 p. 13, « Separate Main Schemes »). Le moteur sait faire
# vivre plusieurs complots principaux a la fois (Tower Defense 21098/21099 :
# `world.area_schemes_main` en contient plusieurs, la phase du vilain les fait
# tous avancer, `Worlds.FindMainScheme` pose la question `GettingMainScheme`
# quand il y en a plus d'un). Ce module fournit :
#  - la propriete `proprietaire_racket` (player_id) posee sur la CARTE ;
#  - `GettingMainScheme` -> le complot du joueur courant (`world.current_player`
#    : le joueur qui joue, celui contre qui l'ennemi s'active, celui a qui la
#    carte rencontre est distribuee), sinon celui de son proprietaire ;
#  - « in this play area » = controle par le proprietaire, ou sbire engage avec
#    lui (livret : identites, allies, ameliorations, sbires...).
# Regle FFG (article Fear No Evil) : quand un ennemi manigance, la menace va
# SEULEMENT sur le complot du joueur contre qui il s'active. Ecart assume : un
# texte d'environnement ou de manigance annexe qui dit « the main scheme »
# tombe sur le complot du joueur courant, pas sur tous (livret p. 13).

NOMS_RACKET = ("Battle in the Bodega", "Bull in a China Shop", "Hung Out to Dry",
               "Pawn Shop Showdown", "A Slice of the Pizza Dough")
CLE = "proprietaire_racket"


def Proprietaire(face: 'CardFace') -> 'Player|None':
    pid = getattr(face.card, CLE, None)
    if pid is None:
        return None
    for p in face.card.world.players:
        if p.player_id == pid:
            return p
    return None


def ComplotsRacket(effect: 'Effect') -> List['MainScheme']:
    return [s for s in Worlds.GetAllMainSchemes(effect) if s.paper.set_name == "Protection Racket"]


def ComplotDuJoueur(effect: 'Effect', joueur: 'Player') -> 'MainScheme|None':
    for s in ComplotsRacket(effect):
        if Proprietaire(s) is joueur:
            return s
    return None


def DansCetteAire(face: 'CardFace', scheme: 'CardFace') -> bool:
    """« in this play area » : controle par le proprietaire du complot, ou
    sbire engage avec lui."""
    proprio = Proprietaire(scheme)
    if proprio is None or face is None:
        return False
    if Minion.IsType(face):
        return getattr(face, "engaged_player", None) is proprio
    if Enemy.IsType(face):
        # Le vilain n'est dans l'aire de personne. `WhenUnitBeDefeated(Unit2)`
        # arrive aussi pour lui (Bullseye I vaincu) et `GetControlByPlayer`
        # posait un assert : partie bloquee en autoplay (18/09/2026).
        return False
    # Un allie deja vaincu (AfterUnitTookDamage arrive apres la defausse)
    # n'a plus de controleur : son proprietaire fait foi.
    controleur = face.GetControlByOrOwner()
    if not Player.IsType(controleur):
        return False
    return controleur is proprio


def MettreEnJeuLeComplot(face_a: 'CardFace', joueur: 'Player', effect: 'Effect') -> 'MainScheme|None':
    """Un complot Protection Racket (face A, mis de cote) entre en jeu dans
    l'aire de `joueur` et se retourne sur sa face 1B (Reveal, comme Tower
    Defense 21098a fait entrer son second complot)."""
    setattr(face_a.card, CLE, joueur.player_id)
    face_a.Reveal(joueur, effect)
    return face_a.card.face.CastTo(MainScheme) if MainScheme.IsType(face_a.card.face) else None


def ComplotsDeCote(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetSetAsideAreaCards(effect)
            if MainScheme.IsType(f) and f.paper.set_name == "Protection Racket"]


def EchangerLeComplot(effect: 'Effect', joueur: 'Player') -> None:
    """Change of Venue : « Swap your main scheme with a random set-aside main
    scheme. Place the threat from the previous scheme on the new scheme. »
    Les attachements de l'ancien complot sont defausses (FAQ du livret)."""
    ancien = ComplotDuJoueur(effect, joueur)
    candidats = ComplotsDeCote(effect)
    if ancien is None or not candidats:
        return
    nouveau_a = Rand.RandomChoice(candidats, effect)
    menace = ancien.threat
    attaches = list(ancien.GetInventoryDeck().Get())
    if attaches:
        Faces.DiscardAll(attaches, effect)
    setattr(ancien.card, CLE, None)
    Faces.SetAside([ancien], effect)
    nouveau = MettreEnJeuLeComplot(nouveau_a, joueur, effect)
    if nouveau is not None and menace > 0:
        nouveau.PlaceThreatOnSchemes([nouveau], menace, effect)


def CapacitesCommunes1B() -> Sequence['Ability']:
    """Sur chaque face 1B : resolution de « the main scheme », defaite si
    n'importe quel complot est accompli ou un joueur elimine, et pion
    d'acceleration partage (« place that acceleration token near the villain :
    each token adds 1 threat to each main scheme »)."""

    def le_complot(effect: 'Effect', message: 'Message.GettingMainScheme') -> 'MainScheme|None':
        this = effect.this.CastTo(MainScheme)
        monde = effect.world
        courant = getattr(monde, "current_player", None)
        demandeur = getattr(message, "face", None) or getattr(message, "trigger", None)
        joueur = None
        if demandeur is not None:
            if Minion.IsType(demandeur):
                joueur = getattr(demandeur, "engaged_player", None)
            elif not EncounterCard.IsType(demandeur):
                joueur = demandeur.GetControlByPlayer()
        if joueur is None:
            joueur = courant
        # Un joueur qui possede plusieurs complots (cas de test, Puzzle.Reveal
        # d'un complot de rechange) : seul le PREMIER repond, sinon le dernier
        # SetReturn l'emporte au hasard de l'ordre des effets.
        if joueur is not None and ComplotDuJoueur(effect, joueur) is this:
            return this
        return None

    def elimine(effect: 'Effect', message: 'Message.WhenPlayerEliminated') -> None:
        Worlds.SetGameOver(False, effect)

    etat = {"en_cours": False}

    def partager(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        if etat["en_cours"]:
            return
        this = effect.this.CastTo(MainScheme)
        etat["en_cours"] = True
        try:
            for s in ComplotsRacket(effect):
                if s is not this:
                    s.PlaceAccelerationToken(1, effect)
        finally:
            etat["en_cours"] = False

    def un_pion_acceleration(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
        return not etat["en_cours"] and getattr(message, "token_name", None) == 'acceleration_token'

    def ranger(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        # La carte du deck de complots que personne n'a choisie : le moteur
        # l'a retournee d'office (world.py:542), on la met de cote ici, sur la
        # face 1B (les capacites de la face 1A ne vivent plus apres le flip).
        this = effect.this
        if getattr(this.card, CLE, None) is None and this.IsInPlay():
            Faces.SetAside([this], effect)

    return [
        AbilityFactory.AfterGameSetup(ranger),
        AbilityFactory.GetMainScheme(le_complot),
        Ability(AbilityType.NonKeyword, Message.WhenPlayerEliminated, [], elimine),
        AbilityFactory.AfterCardPlacedToken(AbilityType.ForcedResponse, "This", None, partager, conditions=[un_pion_acceleration]),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]


def CapacitesDe1A() -> Sequence['Ability']:
    """Setup: Each player chooses a single Protection Racket main scheme (at
    random in expert mode), places it in their play area, and flips it to its
    1B side. Set each unused main scheme aside, out of play.
    Cette carte (celle du deck de complots) est candidate comme les quatre
    mises de cote. Si personne ne la choisit, elle est mise de cote juste
    apres la mise en place (AfterGameSetup) : le moteur l'a deja retournee
    d'office (world.py:542), on ne peut pas l'en empecher sans le toucher."""

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        candidats: List['CardFace'] = [this] + ComplotsDeCote(effect)

        def choisir(player: 'Player') -> None:
            if not candidats:
                return
            if Worlds.IsExpert(effect):
                choix = Rand.RandomChoice(candidats, effect)
            else:
                choix = candidats[0] if len(candidats) == 1 else player.AskChooseFace(list(candidats), effect, prompt="Choose your Protection Racket main scheme")
            if choix is None:
                choix = candidats[0]
            candidats.remove(choix)
            if choix is this:
                setattr(this.card, CLE, player.player_id)
            else:
                MettreEnJeuLeComplot(choix, player, effect)

        Players.ForEachPlayer(effect, choisir)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        if getattr(this.card, CLE, None) is None:
            joueur = message.GetToPlayer()
            if joueur is not None:
                setattr(this.card, CLE, joueur.player_id)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
