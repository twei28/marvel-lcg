"""Campagne « Galactic Storm » (Kajislav, livret 1.2) : mise en place et relevé du carnet.

Livret : docs/packs/galactic-storm/REGLES.md §4 (mode campagne), §7/9/10/11/13 (instructions de
campagne par scénario). Cinq scénarios, dans l'ordre : Kree Sentry (1), Majestrix's Verdict (2),
Hala Ultimatum (3), Earth Under Siege (4), Supreme Intelligence (5).

Particularité unique à ce coffret : chaque joueur joue TROIS identités différentes au fil de la
campagne (pas une seule comme les autres boîtes). Le choix de QUELLE identité amener à quel
scénario, et la restriction de deckbuilding (« aucune carte unique qui corresponde à une carte
déjà notée au carnet ») sont des contraintes qui se jouent ENTRE deux parties, au moment de
construire le deck suivant — rien dans ce moteur ne les contrôle pour AUCUNE campagne (vérifié :
aucun fichier campaign.py existant n'implémente de restriction de deckbuilding). Ce fichier ne les
invente donc pas non plus : elles restent à l'appréciation des joueurs, comme au jeu de plateau, et
sont seulement DOCUMENTÉES dans le journal (identité jouée, cartes uniques en jeu) pour que le
panneau de récompenses les affiche.

Retrait Imperial Guard (décision utilisateur du 21/10/2026, fidélité totale demandée) :
`CardFactory.RandomPick` (`game/card/factory.py`) construit le deck de rencontre AVANT que
`WhenCampaignSetup` ne parte (c'est la face 1A de la manigance principale, mise en place APRÈS la
formation du deck) — on ne peut donc pas lui passer une liste d'exclusion a priori sans toucher un
mécanisme PARTAGÉ du moteur (actuellement le seul consommateur de `random_pick` est ce lot, mais le
modifier reste un risque pour tout pack futur qui s'en servirait). Solution retenue, confinée à ce
pack : `CorrigerImperialGuardExclue` (appelée APRÈS la mise en place), qui repère les cartes déjà
notées « Imperial Guard Removed » si elles ont été piochées à nouveau (environnement en jeu, ou
sbire dans le deck de rencontre) et les remplace par une autre carte du même groupe, encore
disponible. Fonctionnellement équivalent à une vraie exclusion du tirage.

Odd cards (§ "Odd cards", p.6) : le livret dit lui-même "entirely optional... players may still
discuss them" — aucune vérification mécanique n'existe même au jeu de plateau (les joueurs
comparent eux-mêmes leur devinette aux solutions p.19). Le carnet se contente donc d'une case
« combien de devinettes se sont avérées justes » (0 à 4, saisie par le joueur), fidèle à ce que le
livret demande réellement.
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, FaceExists, ExpertMayPlaceAccelerationToHeal

# -------------------------------------------------------------- allié de campagne <- carte gagnée --
ALLIES_BASIC = {
    'gs224': 'Rick Jones',
    'gs225': 'Gladiator',
    'gs226': 'Lauri-Ell',
}
ALLIES_IDENTITY_SPECIFIC = [
    'gs227', 'gs228', 'gs229', 'gs230', 'gs231', 'gs232', 'gs233', 'gs234', 'gs235', 'gs236',
]
STARJAMMER_BASIC_ALLIES = {
    'gs122': "Ch'od", 'gs123': 'Corsair', 'gs124': 'Hepzibah', 'gs125': 'Korvus', 'gs126': 'Raza',
}
# gs091-gs111 : les 21 cartes NON-traîtrise du modulaire Imperial Guard (gs112/gs113 exclues).
IMPERIAL_GUARD_ENVIRONMENTS = ['gs091', 'gs092', 'gs093']
IMPERIAL_GUARD_MINIONS = [f'gs{n:03d}' for n in range(94, 112)]
IMPERIAL_GUARD_NON_TREACHERY = IMPERIAL_GUARD_ENVIRONMENTS + IMPERIAL_GUARD_MINIONS
GLADIATOR_MINION = 'gs098'  # le sbire Imperial Guard, distinct de l'allié de campagne gs225.
NEGA_BOMB = 'gs222a'
GREEN_INTERFERENCE = 'gs223'


def CleCampagnePool(nom: str) -> str:
    return f'Campaign Pool: {nom}'


def RecruteAllie(effect: 'Effect', updates: dict, nom: str, card_id: str) -> None:
    """« record X in Recruited Allies and add the matching campaign-specific ally to the campaign
    pool ». Les deux clés sont cumulatives : on ajoute seulement si pas déjà présent.

    ⚠ `updates` peut déjà porter une liste PLUS A JOUR que le carnet (si `RecruteAllie` a déjà été
    appelée une fois dans CE MÊME `collect_fn`) : lire le carnet à chaque appel écraserait l'ajout
    précédent au lieu de le completer (piège trouvé par l'épreuve `tools/epreuves_campagnes.py`,
    « Gladiator » écrasait « Rick Jones »)."""
    Unused(card_id)
    deja = updates.get('Recruited Allies')
    deja = deja.split(';') if deja is not None else CampaignLog.GetListInternal('Recruited Allies', effect)
    if nom not in deja:
        updates['Recruited Allies'] = ';'.join(deja + [nom])
    updates[CleCampagnePool(nom)] = '1'


def EnregistrerImperialGuardRetiree(effect: 'Effect', updates: dict) -> None:
    """« remove each non-treachery Imperial Guard card USED from the campaign » : une carte
    DÉFAITE (Victory X, en pile de victoire) a bien été « used », pas seulement une encore en jeu
    à l'instant de la victoire (`gs098` Gladiator, vaincu, quitte le jeu AVANT la fin de partie)."""
    deja = set(CampaignLog.GetListInternal('Imperial Guard Removed', effect))
    utilisees = [cid for cid in IMPERIAL_GUARD_NON_TREACHERY
                 if FaceExists(effect, cid, in_play=True) or FaceExists(effect, cid, in_victory=True)]
    nouvelles = deja | set(utilisees)
    if nouvelles:
        updates['Imperial Guard Removed'] = ';'.join(sorted(nouvelles))


def CorrigerImperialGuardExclue(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
    """Remplace, APRÈS la mise en place, toute carte Imperial Guard déjà retirée de la campagne
    (carnet « Imperial Guard Removed ») qui aurait quand même été piochée par le tirage aléatoire
    du modulaire (`data/encounter_sets/gs_imperial_guard.json`). Voir le mot en tête de fichier."""
    Unused(message)
    retirees = set(CampaignLog.GetListInternal('Imperial Guard Removed', effect))
    if not retirees:
        return

    # L'environnement SETTING en jeu.
    for face in Worlds.GetOnFieldEnvironment(effect):
        cid = face.paper.card_id
        if cid in retirees and cid in IMPERIAL_GUARD_ENVIRONMENTS:
            candidats = [c for c in IMPERIAL_GUARD_ENVIRONMENTS if c not in retirees]
            if not candidats:
                continue
            Faces.RemoveAllFromGame([face], effect)
            remplacement = CardFactory.GenerateCard(candidats[0], None, effect.world)
            remplacement.face.CastTo(Environment).PutIntoPlay('FirstPlayer', effect)

    # Les sbires déjà mélangés dans le deck de rencontre.
    deck = Worlds.GetEncounterDeckCards(effect)
    presents = {f.paper.card_id for f in deck}
    for face in deck:
        cid = face.paper.card_id
        if cid in retirees and cid in IMPERIAL_GUARD_MINIONS:
            candidats = [c for c in IMPERIAL_GUARD_MINIONS if c not in retirees and c not in presents]
            if not candidats:
                continue
            choisi = candidats[0]
            presents.add(choisi)
            Faces.RemoveAllFromGame([face], effect)
            remplacement = CardFactory.GenerateCard(choisi, None, effect.world)
            Faces.ShuffleAllTo([remplacement.face], 'EncounterDeck', effect)


def EnregistrerTimePressure(effect: 'Effect', updates: dict) -> None:
    """« record the value on the game round dial in Time Pressure » (scénario 2) / « if the round
    dial is higher than the Time Pressure value recorded, replace it with the dial value »
    (scénarios 3 et 4) : texte imprimé pris au pied de la lettre, la valeur ne baisse jamais."""
    valeur = effect.world.round_id
    recorded = CampaignLog.GetIntInternal('Time Pressure', effect)
    if valeur > recorded:
        updates['Time Pressure'] = str(valeur)


def CollectGalacticStorm(level: int, effect: 'Effect') -> dict:
    updates: dict = {}
    if level == 1:
        RecruteAllie(effect, updates, 'Rick Jones', 'gs224')
        if FaceExists(effect, GLADIATOR_MINION, in_victory=True):
            RecruteAllie(effect, updates, 'Gladiator', 'gs225')
        EnregistrerImperialGuardRetiree(effect, updates)
    elif level == 2:
        for cid, nom in STARJAMMER_BASIC_ALLIES.items():
            if FaceExists(effect, cid, in_play=True):
                RecruteAllie(effect, updates, nom, cid)
        if FaceExists(effect, GLADIATOR_MINION, in_victory=True):
            RecruteAllie(effect, updates, 'Gladiator', 'gs225')
        EnregistrerImperialGuardRetiree(effect, updates)
        EnregistrerTimePressure(effect, updates)
    elif level == 3:
        RecruteAllie(effect, updates, 'Lauri-Ell', 'gs226')
        EnregistrerTimePressure(effect, updates)
        # Pas de retrait Imperial Guard au scénario 3 (le set n'y figure pas).
    elif level == 4:
        if FaceExists(effect, GLADIATOR_MINION, in_victory=True):
            RecruteAllie(effect, updates, 'Gladiator', 'gs225')
        EnregistrerTimePressure(effect, updates)
        # Pas de retrait Imperial Guard au scénario 4 (absent des instructions de victoire, bien
        # que le set soit dans l'encounter deck — vérifié dans REGLES.md §11).
    elif level == 5:
        updates['Campaign Completed'] = '1'
    return updates


# ------------------------------------------------------------------- mise en place de campagne --

def SetupScenario5() -> List['Ability']:
    """Campagne, Supreme Intelligence (REGLES.md §13) :
    - Nega-Bomb en jeu avec X menace PAR JOUEUR, X = Time Pressure enregistrée (remplace la menace
      de départ imprimée, 8[per_hero]) ;
    - les DEUX exemplaires de Green Interference mélangés au deck de rencontre ;
    - pour chaque devinette "Odd card" juste (case saisie par le joueur, 0 à 4), le groupe choisit
      un allié de campagne IDENTITY-SPECIFIC à ajouter à la réserve ;
    - chaque joueur peut mélanger un allié de la réserve (qui ne « correspond » à aucune carte
      unique de son deck — non vérifié automatiquement, voir le mot en tête de fichier) dans son
      deck."""

    def placer_nega_bomb(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        card = CardFactory.GenerateCard(NEGA_BOMB, None, effect.world)
        face = card.face.CastTo(EncounterSideScheme)
        face.PutIntoPlay('FirstPlayer', effect)
        pression = CampaignLog.GetIntInternal('Time Pressure', effect)
        nb_joueurs = len(Worlds.GetPlayers(effect))
        cible = pression * nb_joueurs
        if cible != face.threat:
            face.PlaceThreatOnSchemes([face], cible - face.threat, effect)

    def melanger_green_interference(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        for _ in range(2):
            card = CardFactory.GenerateCard(GREEN_INTERFERENCE, None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)

    def allies_bonus_odd_cards(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        bonnes_reponses = CampaignLog.GetIntInternal('Odd Guesses Correct', effect)
        premier = Worlds.GetFirstPlayer(effect)
        if premier is None:
            return
        for _ in range(max(0, bonnes_reponses)):
            deja = set(CampaignLog.GetListInternal('Recruited Allies', effect))
            candidats = [cid for cid in ALLIES_IDENTITY_SPECIFIC
                         if CampaignLog.GetStrInternal(CleCampagnePool(cid), effect) == '']
            if not candidats:
                return
            choix: Dict[str, str] = {}

            def faire(cid: str):
                def pick(_targets: Sequence['CardFace']):
                    choix['id'] = cid
                return pick
            premier.ChooseAbilities(
                effect,
                *[AbilityFactory.ForChoiceAbility(cid, faire(cid)) for cid in candidats],
            )
            cid = choix.get('id')
            if cid:
                CampaignLog.SetStr(CleCampagnePool(cid), '1', effect.world)

    def chaque_joueur_peut_piocher_un_allie(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        """« Each player may shuffle one ally from the campaign pool ... into their deck » : un
        AJOUT pur, sans retirer quoi que ce soit (distinct de la fonction suivante, qui REMPLACE)."""
        Unused(message)
        for player in Worlds.GetPlayers(effect):
            disponibles = [cid for cid in ALLIES_IDENTITY_SPECIFIC
                           if CampaignLog.GetStrInternal(CleCampagnePool(cid), effect) == '1']
            if not disponibles:
                continue

            def melanger(cid: str):
                def action(_targets: Sequence['CardFace']):
                    card = CardFactory.GenerateCard(cid, player.player_deck, effect.world)
                    Faces.ShuffleAllTo([card.face], player.player_deck, effect)
                return action
            player.ChooseAbilities(
                effect,
                *[AbilityFactory.ForChoiceAbility(
                    f"Mélanger {cid} (réserve de campagne) dans son deck", melanger(cid))
                  for cid in disponibles],
                AbilityFactory.ForChoiceAbility("Ne rien mélanger", lambda _t: None),
            )

    def chaque_joueur_peut_remplacer_un_allie(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        """« Each player may choose one identity-specific ally in their deck and replace it with a
        campaign identity-specific ally from the Galactic Storm set ... » : RETIRE un allié
        IDENTITY-SPECIFIC du deck (desc.Class, `ClassCard.IsClass`, base native du moteur) et pose
        un allié de la réserve à la place — distinct de la fonction précédente, qui ne fait
        qu'ajouter. « ne correspond à aucune carte unique » (prohibited cards, p.6) : non vérifié
        mécaniquement ici, voir le mot en tête de fichier sur la restriction de deckbuilding."""
        Unused(message)
        for player in Worlds.GetPlayers(effect):
            disponibles = [cid for cid in ALLIES_IDENTITY_SPECIFIC
                           if CampaignLog.GetStrInternal(CleCampagnePool(cid), effect) == '1']
            allies_identite = [f for f in player.player_deck.FindCards(card_type=Ally)
                                if f.IsClass("IdentitySpecific")]
            if not disponibles or not allies_identite:
                continue

            def remplacer(ancien: 'CardFace', cid: str):
                def action(_targets: Sequence['CardFace']):
                    Faces.RemoveAllFromGame([ancien], effect)
                    card = CardFactory.GenerateCard(cid, player.player_deck, effect.world)
                    Faces.ShuffleAllTo([card.face], player.player_deck, effect)
                return action
            choix = [
                AbilityFactory.ForChoiceAbility(
                    f"Remplacer {ancien.paper.card_id} ({ancien.paper.name}) par {cid} (réserve de campagne)",
                    remplacer(ancien, cid))
                for ancien in allies_identite for cid in disponibles
            ]
            player.ChooseAbilities(
                effect, *choix,
                AbilityFactory.ForChoiceAbility("Ne rien remplacer", lambda _t: None),
            )

    return [
        AbilityFactoryCampaign.WhenCampaignSetup(placer_nega_bomb),
        AbilityFactoryCampaign.WhenCampaignSetup(melanger_green_interference),
        AbilityFactoryCampaign.WhenCampaignSetup(allies_bonus_odd_cards),
        AbilityFactoryCampaign.WhenCampaignSetup(chaque_joueur_peut_piocher_un_allie),
        AbilityFactoryCampaign.WhenCampaignSetup(chaque_joueur_peut_remplacer_un_allie),
    ]


def CampaignSetup(level: int) -> List['Ability']:
    abilities: List['Ability'] = []
    if level in (1, 2, 4):
        # Imperial Guard est utilisée (et sa randomisation corrigée pour tenir compte des cartes
        # déjà retirées) aux scénarios 1, 2 et 4 (absente du scénario 3, voir REGLES.md §10/11).
        abilities.append(AbilityFactoryCampaign.WhenCampaignSetup(CorrigerImperialGuardExclue))
    if level == 5:
        abilities += SetupScenario5()
    abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
    abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(
        lambda effect, message: CollectGalacticStorm(level, effect)))
    return abilities
