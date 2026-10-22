from ..commun import *
from ..campaign import *

# ⚠ Le dossier porte le nom du set nettoye (`FileManager.CleanName("Campaign - The City Never Sleeps")`) : sinon le chargeur ne trouve aucun
# script (cartes sans capacite, sans erreur : trouve le 22/10/2026).
# Cartes de campagne de « La ville ne dort jamais » (MC×DC 2026) : pu140 Big Apple Gang War! (combat 1) et pu141 Seized Tech Crates
# (recompense du combat 1). La mise en place et le releve du carnet sont dans `punisher_mcdc_2026/campaign.py`.


def JetonsDeDepart(effect: 'Effect') -> int:
    """pu141, Setup : « Place 1 counter here, plus 1 more for each player who did not play the last game together. »
    Un joueur « nouveau » = un heros absent du carnet de la partie precedente (`Player N Identity`, ecrit par `WriteCampaignLogAtGameOver`)."""
    precedents = {CampaignLog.GetStrInternal(f'Player {i} Identity', effect) for i in range(1, 5)} - {''}
    if not precedents:
        return 1
    nouveaux = 0
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is None:
            continue
        try:
            nom = identite.GetHeroFace().paper.name.lstrip('* ')
        except AssertionError:      # une identite sans face heros lisible (voir mts/campaign.py) : comptee comme nouvelle
            nom = ''
        if nom not in precedents:
            nouveaux += 1
    return 1 + nouveaux


################################################################################
# KINGSFALL MULTI-TABLES (assemblees, « pods »). Voir `game/operate/assemblee.py` et .planning/mcdc-punisher/decisions-multi-tables.md.
# Hors assemblee (`Assemblee.Courante` rend None), RIEN de ceci ne s'applique : les cartes gardent leur comportement d'un seul groupe.
################################################################################
from cards.pack.fne.kingpin import TrouverPublicSupport

EN_COURS_POD = 0


def Pod(effect: 'Effect') -> 'tuple[str, str] | None':
    """(code, table) de l'assemblee de cette partie, ou None."""
    return Assemblee.Courante(effect)


def LongueVie(effect: 'Effect') -> 'CardFace|None':
    """Longue vie / A bas : la carte en jeu, quelle que soit la face visible."""
    return Worlds.FindCardOnField(effect, card_ids=['pu149a', 'pu149b'])


def SynchroniserLaTable(effect: 'Effect') -> None:
    """Applique a CETTE table l'etat commun de l'assemblee. IDEMPOTENT et peu couteux : on ne touche a rien tant que la version du stockage n'a pas change.
      1. les jetons que d'autres groupes ont envoyes (Action d'assemblee) arrivent sur Power to the People (jetons `counter`) ;
      2. Longue vie (miroir) montre le TOTAL commun, et se retourne en « A bas » des que l'assemblee a atteint le seuil (A bas remet alors les jetons de
         Soutien des Citoyens de CETTE table a 2 par joueur + 3) ;
      3. Le Roi (miroir) montre les degats et la menace communs."""
    pod = Pod(effect)
    if pod is None:
        return
    code, table = pod
    etat = Assemblee.Etat(code)
    if etat is None:
        return
    monde = effect.world
    en_attente = next((g['recus'] for g in etat['groupes'] if g['tab'] == table), 0)
    if getattr(monde, 'pod_version', None) == etat['version'] and not en_attente:
        return
    monde.pod_version = etat['version']
    if en_attente:
        recus = Assemblee.PrendreLesJetonsRecus(code, table)
        pouvoir = Worlds.FindCardOnField(effect, card_ids=[POUVOIR_AU_PEUPLE])
        if recus and pouvoir is not None:
            Faces.PlaceCountersOn([pouvoir], recus, 'counter', effect)
    roi = Worlds.FindCardOnField(effect, card_ids=['pu151'])
    if roi is not None:
        for nom, valeur in (('king_damage', etat['degats']), ('king_threat', etat['menace'])):
            actuel = roi.GetCounters(nom)
            if actuel < valeur:
                Faces.PlaceCountersOn([roi], valeur - actuel, nom, effect)
    longue = LongueVie(effect)
    if longue is not None:
        actuel = longue.GetCounters('support')
        total = etat['total_jetons']
        if actuel < total:
            Faces.PlaceCountersOn([longue], total - actuel, 'support', effect)
        elif actuel > total:
            Faces.RemoveCountersOn([longue], actuel - total, 'support', effect)
        if etat['retournee'] and str(longue.paper.card_id) == 'pu149a':
            longue.card.Flip(effect)


def ActionDAssemblee() -> 'Ability':
    """« Pod Action : Choose a group in the pod. Move 1 counter from your Public Support to their Power to the People. » (Longue vie ET A bas)
    Le jeton quitte le Soutien des Citoyens de CETTE table ; il arrive sur Power to the People du groupe choisi (sur la meme table : tout de suite ;
    sur une autre : a sa prochaine synchronisation, voir `SynchroniserLaTable`)."""

    def groupes_en_cours(etat: 'Dict[str, Any]') -> 'List[Dict[str, Any]]':
        return [g for g in etat['groupes'] if g['etat'] == EN_COURS_POD]

    def possible(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        pod = Pod(effect)
        if pod is None:
            return False
        SynchroniserLaTable(effect)
        soutien = TrouverPublicSupport(effect)
        etat = Assemblee.Etat(pod[0])
        return soutien is not None and soutien.GetCounters('support') >= 1 and etat is not None and bool(groupes_en_cours(etat))

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        pod = Pod(effect)
        if joueur is None or pod is None:
            return
        code, table = pod
        etat = Assemblee.Etat(code)
        if etat is None:
            return

        def envoyer(groupe: 'Dict[str, Any]') -> None:
            soutien = TrouverPublicSupport(effect)
            if soutien is None or soutien.GetCounters('support') < 1:
                return
            if groupe['tab'] == table:
                pouvoir = Worlds.FindCardOnField(effect, card_ids=[POUVOIR_AU_PEUPLE])
                if pouvoir is None:
                    return
                Faces.RemoveCountersOn([soutien], 1, 'support', effect)
                Faces.PlaceCountersOn([pouvoir], 1, 'counter', effect)
            elif Assemblee.EnvoyerJeton(code, groupe['tab']):
                Faces.RemoveCountersOn([soutien], 1, 'support', effect)

        options = []
        for groupe in groupes_en_cours(etat):
            nom = (groupe['noms'] or groupe['tab']).strip()
            libelle = f"{nom} ({groupe['tab']})" + (" - this table" if groupe['tab'] == table else "")
            options.append(AbilityFactory.ForChoiceAbility(libelle, lambda cibles, g=groupe: envoyer(g)))
        joueur.ChooseAbilities(effect, *options)

    return (AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action, conditions=[possible])
            .SetName("Pod Action")
            .AnyPlayerCanDoThis())
