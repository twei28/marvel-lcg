from . import *

# Tribute
# SONG.
# Limit 1 per deck.
# Hero Action: After you play Tribute from your hand, choose 1 non-identity
#   event in your collection. Tribute becomes a copy of that card, (except for
#   its cost) but keeps the SONG trait, until it is placed in the discard pile.
#
# Decision de l'utilisateur (Q4 du backlog 12, 20/10/2026) : VRAIE COPIE,
# limitee aux evenements jouables tout de suite en Action / Hero Action.
#   - le joueur choisit EN VOYANT LES CARTES (modele Cameo 58031 : candidats
#     fabriques dans `world.area_removed`, `AskChooseFace`) un evenement
#     non-identite ; un evenement a Interrupt / Response n'est pas propose ;
#   - Tribute DEVIENT cette carte (`DevenirCopie`, dazzler/__init__.py) et en
#     resout l'effet sans payer son cout en ressources (les couts AVANT la
#     fleche se paient, comme pour Karaoke Night, Q5) ; elle garde [[SONG]] ;
#   - aucune carte n'apparait en main ;
#   - Live Concert la range dans la Setlist EN TANT QUE COPIE (avec son
#     Showtime! si elle en a un) ; elle redevient Tribute en entrant dans la
#     defausse (`Card.CheckIfCanDiscard`).
# Avant le 20/10/2026 : `Search.Collection` fabriquait la carte, la mettait en
# MAIN et tentait de la jouer ; une Response choisie y RESTAIT.


def GetAbilities() -> Sequence['Ability']:

    def candidats(effect: 'Effect', joueur: 'Player') -> List['CardFace']:
        from cards.database import CardsDB
        from game.card.factory import CardFactory
        world = effect.world
        vus = set()
        faces: List['CardFace'] = []
        for card_id, paper in sorted(CardsDB.papers.items()):
            if paper.type != "Event" or card_id == effect.this.paper.card_id:
                continue
            classes = (paper.desc.get("Class") or "").split(";")
            if "Hero" in classes or paper.name in vus:
                continue
            texte = paper.text or ""
            if "Action</b>" not in texte:
                continue
            carte = CardFactory.GenerateCard(card_id, world.area_removed, world)
            if carte is None or carte.face is None:
                continue
            jeu = CapaciteDeJeu(carte.face)
            if jeu is None:
                continue
            jeu.context.initiator = joueur
            if not all(cf.HasTargets(jeu) for cf in jeu.cost_func.GetAll()):
                continue
            vus.add(paper.name)
            faces.append(carte.face)
        return faces

    def tribute(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.card.tribute_copie = None
        faces = candidats(effect, joueur)
        if not faces:
            return
        choisie = joueur.AskChooseFace(faces, effect)
        if choisie is None:
            return
        copie = DevenirCopie(this, choisie.paper, effect)
        jeu = CapaciteDeJeu(copie)
        if jeu is None:
            return
        ref = Message.WhenPlayerInTurn(joueur, effect)
        ResoudreAvecChoix(jeu, copie, joueur, effect, ref, payer_cout=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tribute,
        ).SetPlay().SetLabel(),
    ]
