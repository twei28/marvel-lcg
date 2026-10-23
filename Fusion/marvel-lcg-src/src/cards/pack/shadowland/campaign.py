"""Campagne « Shadowland » (MC65) : mise en place et relevé du carnet.

Livret FR : docs/packs/shadowland/livret-fr.md (« Mode campagne », instructions de campagne des trois scénarios p. 9-10, 14-15, 17, registre p. 20). Trois scénarios, dans l'ordre :
Des Ombres dans la Nuit (1, `shadows_in_the_night`), Le Labyrinthe des Ombres (2, `shadow_labyrinth`), Cœur d'Ombre (3, `heart_of_shadow`).

Le carnet (clés, toutes en anglais comme le reste du jeu ; l'écran les affiche en français) :
- `Dark Protege Removed` : liste « sl013a;sl014a » des vilains Sombres Protégés retirés de la campagne (registre, case « Sombres Protégés retirés »). Écrite aux victoires des
  scénarios 1 et 2 ; le tirage au hasard des scénarios 1 et 2 l'exclut (`VilainsTirables`, `__init__.py`). Daredevil et Elektra sont retirés dès la mise en place si un joueur porte ce nom.
- `Player N Overpowering Scenario 1|2` : « 1 » si la Corruption Insidieuse du joueur avait le trait INSOUTENABLE (OVERPOWERING, face sl072b) à la victoire (registre, grille J1-J4).
- `Player N Recorded Card 1|2` : l'identifiant du soutien / de l'amélioration de coût 2 ou moins que le joueur inscrit au registre après les scénarios 1 et 2 (saisi par le joueur : « peut choisir »).
- `Player N Remaining hit points` : campagne experte (PV persistants), posé par le panneau (`victoire_commune_expert`).
- `Campaign Completed` : posé à la victoire du scénario 3.

⚠ Ce que le livret ne dit pas, et qui est décidé ici : si les six Sombres Protégés sont retirés (cas impossible en trois scénarios hors Daredevil et Elektra + deux victoires, mais écrit par
sécurité), le tirage retombe sur la liste complète plutôt que de laisser le scénario sans vilain.
"""
from cards.pack.shadowland import *
from cards.pack.shadowland.black_flower import CreepingCorruptionDe, CorruptionOverpowering, PoserCorruption
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

# L'ensemble des cartes du set Black Flower QUI ENTRENT DANS LE DECK DE RENCONTRE (data/encounter_sets/black_flower.json) : un test de la campagne vérifie l'égalité.
CARTES_BLACK_FLOWER = ['sl073', 'sl074', 'sl075', 'sl075', 'sl076', 'sl077', 'sl077', 'sl078', 'sl078']
CORRUPTION = 'sl072a,sl072b'
SBIRES_SOMBRES_PROTEGES = ['sl020', 'sl021', 'sl022', 'sl023']   # Grande Prêtresse (Archpriestess), Gorgone, Lady Bullseye, Tigre Blanc
MENACE_SUPPLEMENTAIRE = {1: 1, 2: 3}                             # par joueur : « Placez 1 / 3 menace(s) supplémentaire(s) sur la manigance principale »


def CleOverpowering(scenario: int) -> str:
    return f'Overpowering Scenario {scenario}'


def CleCarteInscrite(numero: int) -> str:
    return f'Recorded Card {numero}'


def _joueurs(effect: 'Effect') -> List['Player']:
    return list(Worlds.GetPlayers(effect))


def _manigance_principale(effect: 'Effect') -> 'MainScheme|None':
    schemes = Worlds.GetAllMainSchemes(effect)
    return schemes[0] if schemes else None


# ------------------------------------------------------------------------------------------------------------------------------------------ mise en place
def PoserLaCorruptionInsidieuse(effect: 'Effect') -> None:
    """Scénarios 1 et 2 : « chaque joueur met en jeu sous son contrôle une Corruption Insidieuse (72A), face A visible, mot-clé Mise en Place. Mettez de côté les autres.
    Mélangez dans le deck Rencontre chaque autre carte de ce set modulaire. » Les exemplaires inutilisés ne sont tout simplement pas créés (« de côté »)."""
    for joueur in _joueurs(effect):
        if CreepingCorruptionDe(joueur) is not None:
            continue
        card = CardFactory.GenerateCard(CORRUPTION, None, effect.world)
        card.SetOwner(joueur)
        card.face.CastTo(Upgrade).AttachTo2(joueur.GetIdentity(), effect)
    for card_id in CARTES_BLACK_FLOWER:
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)


def PlacerMenacesSupplementaires(effect: 'Effect', par_joueur: int) -> None:
    scheme = _manigance_principale(effect)
    if scheme is None:
        return
    scheme.PlaceThreatInternal(par_joueur * len(_joueurs(effect)), effect)


def JetonsDesCorruptionsInsoutenables(effect: 'Effect', niveau: int) -> None:
    """Scénario 2 : un jeton Corruption pour le joueur dont la Corruption était INSOUTENABLE au scénario 1. Scénario 3 : un jeton par scénario précédent où elle l'était (1 et 2)."""
    for joueur in _joueurs(effect):
        n = sum(1 for s in range(1, niveau) if CampaignLog.GetStrByPlayer(CleOverpowering(s), joueur.player_id, effect) != '')
        if n:
            PoserCorruption(effect, joueur, n)


def MettreEnJeuLesCartesInscrites(effect: 'Effect', niveau: int) -> None:
    """« Chaque joueur a le droit de choisir dans son deck son exemplaire de la carte inscrite au registre et de la mettre en jeu sous son contrôle. Chaque joueur qui le fait place 1 jeton
    Corruption. » Scénario 2 : la carte n°1 ; scénario 3 : chaque carte inscrite (n°1 et n°2). Un joueur qui n'a pas la carte dans son deck n'a rien à choisir."""
    for joueur in _joueurs(effect):
        for numero in range(1, niveau):
            card_id = CampaignLog.GetStrByPlayer(CleCarteInscrite(numero), joueur.player_id, effect).strip()
            if not card_id:
                continue
            exemplaires = [f for f in joueur.player_deck.Get() if str(f.paper.card_id) == card_id]
            if not exemplaires:
                continue
            face = exemplaires[0]

            def mettre_en_jeu(_cibles: Sequence['CardFace'], face: 'CardFace'=face, joueur: 'Player'=joueur) -> None:
                face.PutIntoPlay(joueur, effect, under_control=True)
                PoserCorruption(effect, joueur, 1)

            joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility(
                f"Mettre {face.paper.name} (inscrite au registre) en jeu et placer 1 jeton Corruption", mettre_en_jeu))


def DistribuerLesSbiresDeSombresProteges(effect: 'Effect') -> None:
    """Scénario 3 : « trouvez les quatre sbires restants du set Sombres Protégés (Grande Prêtresse, Gorgone, Lady Bullseye et Tigre Blanc). Attribuez aléatoirement un sbire à chaque joueur
    en tant que carte Rencontre face cachée. Ensuite, mélangez les sbires restants dans le deck Rencontre. » Ils sont créés (le scénario 3 ne met pas le set de côté)."""
    sbires = [CardFactory.GenerateCard(card_id, None, effect.world).face for card_id in SBIRES_SOMBRES_PROTEGES]
    for joueur in _joueurs(effect):
        if not sbires:
            break
        face = Rand.RandomChoice(sbires, effect)
        sbires.remove(face)
        Faces.MoveAllTo([face], joueur.dealt_encounter_cards, effect)
    if sbires:
        Faces.ShuffleAllTo(sbires, 'EncounterDeck', effect)


def MiseEnPlaceDeCampagne(niveau: int) -> 'Ability':
    """TOUTE la mise en place d'un scénario dans UNE capacité : l'ordre compte (la Corruption doit exister avant d'y poser des jetons)."""
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        if niveau in (1, 2):
            PoserLaCorruptionInsidieuse(effect)
        if niveau in (2, 3):
            JetonsDesCorruptionsInsoutenables(effect, niveau)
            MettreEnJeuLesCartesInscrites(effect, niveau)
        if niveau in MENACE_SUPPLEMENTAIRE:
            PlacerMenacesSupplementaires(effect, MENACE_SUPPLEMENTAIRE[niveau])
        if niveau == 3:
            DistribuerLesSbiresDeSombresProteges(effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)


# ------------------------------------------------------------------------------------------------------------------------------------------ carnet sortant
def VilainUtilise(effect: 'Effect') -> 'str|None':
    """« sl014a » : le vilain Sombres Protégé de ce scénario (tiré au hasard : en jeu au scénario 1, mis de côté et retenu au scénario 2), ou None."""
    retenu = getattr(effect.world, 'sl_vilain_choisi', None)
    if retenu:
        return f'{retenu}a'
    for face in Worlds.GetAllVillains(effect):
        base = BaseDuVilain(face.paper.card_id)
        if base in VILAINS_SOMBRES_PROTEGES:
            return f'{base}a'
    return None


def CollectShadowland(niveau: int, effect: 'Effect', gagne: bool) -> dict:
    updates: dict = {}
    if niveau in (1, 2):
        retires = [BaseDuVilain(x) for x in CampaignLog.GetListInternal(CLE_VILAINS_RETIRES, effect)]
        retires += VilainsDeLIdentite(effect)
        utilise = VilainUtilise(effect)
        if gagne and utilise:
            retires.append(BaseDuVilain(utilise))
        if retires:
            updates[CLE_VILAINS_RETIRES] = ';'.join(sorted({f'{b}a' for b in retires}))
        if gagne:
            for joueur in _joueurs(effect):
                if CorruptionOverpowering(joueur):
                    updates[f'Player {joueur.player_id + 1} {CleOverpowering(niveau)}'] = '1'
    if niveau == 3 and gagne:
        updates['Campaign Completed'] = '1'
    return updates


def CampaignSetup(niveau: int) -> List['Ability']:
    abilities: List['Ability'] = [MiseEnPlaceDeCampagne(niveau)]
    if niveau in (2, 3):
        # Campagne experte : PV restants du registre, puis chaque joueur peut se soigner jusqu'à ses PV de départ en s'attribuant une carte Rencontre face cachée.
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(AbilityFactoryCampaign.ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(1))
    abilities.append(WriteCampaignLogAtGameOver(
        lambda effect, message: CollectShadowland(niveau, effect, bool(getattr(message, 'players_won', False)))))
    return abilities
