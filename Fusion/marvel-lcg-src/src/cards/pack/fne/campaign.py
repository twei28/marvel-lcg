"""Campagne « Fear No Evil » (livret mc60 p. 8-9, 13-23) : mise en place et
releve du carnet.

Le fil : cinq affaires jouables dans l'ordre choisi par les joueurs (Art
Museum Heist, The Getaway, Protection Racket, The Raft Breakout, Stop the
Presses!), chacune contre un vilain UNDERLING ; avant chaque partie, deux
affaires non resolues PROGRESSENT (marques), trois marques = affaire echouee ;
quand les cinq sont Completed ou Failed, Kingpin. Chaque affaire a un
environnement recto-verso Completed / Failed (60205-60209) qui entre en jeu a
toutes les parties suivantes.

Cles du carnet (les chaines litterales que `tools/verifier_campagnes.py`
compare a `data/campagnes/fne.json`) :
  - "Completed Scenarios" / "Failed Scenarios" : listes de manigances ;
  - "Progress: <manigance>" : 0..3 (ecrit par l'ecran des campagnes) ;
  - "Villain: <manigance>" : le vilain enregistre pour l'affaire ;
  - "Trust Established?" / "Mary Defeated?" : "1" ;
  - "Allies removed from the campaign" : titres (allies ET soutiens uniques) ;
  - "Remaining hit points" par joueur (campagne experte, cle du moteur).
La progression et l'affectation des vilains sont l'affaire de l'ecran
(public/js/campagne/app.js, vue « ordre libre ») : le moteur ne fait que lire.
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

MANIGANCES = ("art_museum_heist", "the_getaway", "protection_racket", "the_raft_breakout", "stop_the_presses")
ENVIRONNEMENTS = {
    "art_museum_heist":  ("60205a", "60205b"),
    "the_getaway":       ("60206a", "60206b"),
    "protection_racket": ("60207a", "60207b"),
    "the_raft_breakout": ("60208a", "60208b"),
    "stop_the_presses":  ("60209a", "60209b"),
}
SOUTIENS_DAILY_BUGLE = ("60153", "60154", "60155", "60156")
PRISONNIERS_DU_RAFT = ("60144", "60145", "60146", "60147", "60148", "60149")
MARY = "60210a,60210b"
CLE_COMPLETED = "Completed Scenarios"
CLE_FAILED = "Failed Scenarios"
CLE_TRUST = "Trust Established?"
CLE_MARY = "Mary Defeated?"
CLE_RETIREES = "Allies removed from the campaign"


def Completed(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_COMPLETED, effect)


def Failed(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_FAILED, effect)


def Progression(manigance: str, effect: 'Effect') -> int:
    return CampaignLog.GetIntInternal(f"Progress: {manigance}", effect)


def Retirees(effect: 'Effect') -> List[str]:
    return CampaignLog.GetListInternal(CLE_RETIREES, effect)


def EnvironnementsEnJeu(effect: 'Effect') -> List['CardFace']:
    ids = {a for a, b in ENVIRONNEMENTS.values()} | {b for a, b in ENVIRONNEMENTS.values()}
    faces = []
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is not None and face.IsInPlay() and face.paper.card_id in ids:
            faces.append(face)
    return faces


def NombreDeCompleted(effect: 'Effect') -> int:
    return len([f for f in EnvironnementsEnJeu(effect) if f.paper.card_id.endswith('a')])


def MettreLesEnvironnements(conditions=[]) -> 'Ability':
    """Etape 12 de la mise en place de campagne : l'environnement de chaque
    affaire Completed face Completed, de chaque affaire Failed face Failed."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        deja = {f.paper.card_id for f in EnvironnementsEnJeu(effect)}
        for manigance, (a, b) in ENVIRONNEMENTS.items():
            if manigance in Completed(effect):
                ids = f"{a},{b}"
            elif manigance in Failed(effect):
                ids = f"{b},{a}"
            else:
                continue
            if ids.split(',')[0] in deja:
                continue
            card = CardFactory.GenerateCard(ids, None, effect.world)
            card.face.PutIntoPlay(premier, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def RetirerLesCartesRetirees(conditions=[]) -> 'Ability':
    """Etape 8 : chaque joueur retire de son deck les cartes dont le titre est
    au carnet (allies et soutiens uniques retires du jeu). Le complement de
    deck en dessous du minimum n'est pas fait ici : c'est un choix de
    construction, hors mise en place automatique."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        titres = set(Retirees(effect))
        if not titres:
            return
        for player in Worlds.GetPlayers(effect):
            zones = list(player.player_deck.Get(True)) + list(player.hand_cards.Get(True)) + list(player.discard_pile.Get(True))
            a_retirer = [f for f in zones if f.paper.name.lstrip('* ') in titres or f.paper.name in titres]
            if a_retirer:
                Faces.RemoveAllFromGame(a_retirer, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MaryWalker(conditions=[]) -> 'Ability':
    """Etape 13 : « Trust Established? » coche et « Mary Defeated? » non ->
    l'alliee Typhoid Mary (210A) entre en jeu sous le controle d'un joueur."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        if not CampaignLog.GetStrInternal(CLE_TRUST, effect) or CampaignLog.GetStrInternal(CLE_MARY, effect):
            return
        premier = Worlds.GetFirstPlayer(effect)
        card = CardFactory.GenerateCard(MARY, None, effect.world)
        card.face.PutIntoPlay(premier, effect, under_control=True)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MarquesDeLAffaire(manigance: str, conditions=[]) -> 'Ability':
    """Les encarts CAMPAIGN INSTRUCTIONS / SETUP du livret (p. 13-21), selon
    le nombre de marques de progression de l'affaire jouee."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        n = Progression(manigance, effect)
        if n <= 0:
            return
        expert = Worlds.IsExpert(effect)
        premier = Worlds.GetFirstPlayer(effect)
        if manigance in ("art_museum_heist", "protection_racket"):
            # « Place 1 threat (2 in expert) on the/each main scheme for each check mark »
            par_marque = 2 if expert else 1
            for scheme in Worlds.GetAllMainSchemes(effect):
                scheme.PlaceThreatOnSchemes([scheme], par_marque * n, effect)
        elif manigance == "the_getaway":
            camion = Worlds.FindCardOnField(effect, name="Jackknifed Tanker Truck", card_type=EncounterSideScheme)
            if camion is None:
                camion = Find.FindAndReveal(effect, premier, name="Jackknifed Tanker Truck", card_type=EncounterSideScheme)
            if n >= 2 and camion is not None:
                camion.PlaceThreatOnSchemes([camion], 2 if expert else 1, effect)
        elif manigance == "the_raft_breakout":
            prisonniers = Worlds.FindCardsOnField(effect, trait="PRISONER", card_type=Minion)
            if prisonniers:
                Faces.GiveStatus(prisonniers, "Tough", effect)
                if n >= 2:
                    Faces.GiveFacedownBoostCards(prisonniers, 1, effect)
        elif manigance == "stop_the_presses":
            for soutien in Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support):
                Faces.RemoveCountersOn([soutien], n, 'stamina', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def MarquesKingpin(conditions=[]) -> 'Ability':
    """Kingpin, SETUP (p. 23) : 3 environnements Completed -> chaque sbire en
    jeu robuste ; 4 -> trouver et reveler James Wesley."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        n = NombreDeCompleted(effect)
        if n >= 3:
            sbires = Worlds.GetOnFieldMinions(effect)
            if sbires:
                Faces.GiveStatus(sbires, "Tough", effect)
        if n >= 4:
            Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect), name="James Wesley", card_type=Attachment)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=conditions)


def _partie_gagnee(message: 'Message.WhenGameOver') -> bool:
    """Le resultat vient du MESSAGE, pas du monde.

    ⚠ `GameOver.SetGameOver` envoie `WhenGameOver` PUIS pose `players_won` sur
    le monde : pendant le message, `world.game_over` dit encore « perdue ».
    La version precedente lisait le monde, donc « Completed Scenarios » n'etait
    JAMAIS ecrit, meme sur une victoire. Personne ne l'avait vu parce que rien
    ne jouait la fin d'une partie (trouve le 19/09/2026 par
    `tools/test_campagnes.py`).
    """
    return bool(getattr(message, "players_won", False))


def CollectFNE(manigance: 'str|None', effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Le carnet sortant, releve a la fin de la partie (VICTORY du livret) :
    l'affaire gagnee rejoint « Completed Scenarios » ; « Trust Established? »
    si Disturbed Psyche a au moins 2 jetons menace ; « Mary Defeated? » si
    l'alliee est dans la pile de victoire ; les allies et soutiens UNIQUES
    retires du jeu s'ajoutent a « Allies removed from the campaign »."""
    updates = {}
    gagnee = _partie_gagnee(message)
    if manigance and gagnee:
        faits = Completed(effect)
        if manigance not in faits:
            updates[CLE_COMPLETED] = ";".join(faits + [manigance])
    if gagnee:
        psyche = Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)
        if psyche is not None and psyche.GetTokens('threat') >= 2:
            updates[CLE_TRUST] = "1"
    for card in effect.world.object_manager.card_dict.values():
        face = card.face
        if face is not None and face.paper.card_id in ("60210a", "60210b") and card.area.flags.is_victory_display:
            updates[CLE_MARY] = "1"
    retirees = list(Retirees(effect))
    for face in effect.world.area_removed.Get(True):
        # ⚠ `paper.name` n'a PLUS l'etoile a l'execution (paper.py:45 la
        # retire et pose `is_unique`) : tester le drapeau, pas le prefixe
        # (cas « Carnet sortant » rouge le 18/09/2026, Black Cat non relevee).
        if (Ally.IsType(face) or Support.IsType(face)) and face.paper.is_unique:
            proprietaire = face.GetOwner()
            if Player.IsType(proprietaire):
                titre = face.paper.name.lstrip('* ')
                if titre not in retirees:
                    retirees.append(titre)
    if retirees and retirees != list(Retirees(effect)):
        updates[CLE_RETIREES] = ";".join(retirees)
    return updates


def CapacitesDeCampagne(manigance: str, garde=None) -> List['Ability']:
    """A poser sur la face 1A de chaque manigance interchangeable.

    `garde(effect, message) -> bool` : condition supplementaire sur les
    capacites de mise en place. Protection Racket a UN complot principal PAR
    JOUEUR (cinq copies de 60134a-60138a) : sans garde, chaque copie
    remettrait les environnements, Mary Walker et les marques de l'affaire
    (Mary entrerait N fois). La garde ne laisse parler que le premier complot
    en jeu ; le carnet de fin de partie, lui, est idempotent."""
    conditions = [garde] if garde else []
    return [
        MettreLesEnvironnements(conditions),
        RetirerLesCartesRetirees(conditions),
        MarquesDeLAffaire(manigance, conditions),
        MaryWalker(conditions),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(manigance, effect, message)),
    ]


def CapacitesDeCampagneKingpin() -> List['Ability']:
    """A poser sur The King's Gambit 1A (60161a)."""
    return [
        MettreLesEnvironnements(),
        RetirerLesCartesRetirees(),
        MarquesKingpin(),
        MaryWalker(),
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(lambda effect, message: CollectFNE(None, effect, message)),
    ]
