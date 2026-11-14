# Cas test_capacites : les options REFUSEES d'un choix (`ChooseAbilities`) partent dans le canal des refus. Prefixe `[choixrefus]`.
# Bug 129 (12/11/2026), Nick Fury 01084 : « Remove 2 threat from a scheme » disparaissait quand aucun complot n'avait de menace.
CAS = [
    {"nom": "[choixrefus] 01084 Nick Fury, aucun complot avec de la menace : l'option « retirer 2 menaces » part dans les refus du choix",
     "pourquoi": "`ChooseEffects` garde les options ecartees (`WorldRender.choix_refuses`) et `Controller.RendreLesRefus(choix=<question>)` les joint ; hors de cette question, rien",
     "scenario": "rhino", "heros": "spider_man",
     "mise_en_place": ["Puzzle.ChangeToFace('01001b', '01001a')", "Puzzle.SetThreat('01097b', 0)"],
     "declencher": [], "verifier": "choix_refuses_nick_fury", "attendu": {}},
]

VERIFICATIONS = r'''
def choix_refuses_nick_fury(monde, aides):
    from engine.controller.controller import Controller
    from game.event.manager import EventManager
    from game.effect.effect import Effect
    from game.effect.rule import GameRule
    from game.message import Message
    from game.ability.factory import AbilityFactory
    from game.card.face.base import Scheme2, Enemy
    joueur = monde.players[0]
    identite = joueur.GetIdentity()
    # Les trois options de 01084, telles que le script les declare.
    abilites = [
        AbilityFactory.ForChoiceAbility("Remove 2 threat from a scheme", lambda cibles: None).SetTarget(Scheme2),
        AbilityFactory.ForChoiceAbility("Draw 3 cards", lambda cibles: None).SetTarget("YourIdentity"),
        AbilityFactory.ForChoiceAbility("Deal 4 damage to an enemy", lambda cibles: None).SetTarget(Enemy),
    ]
    effets = [Effect(identite, a, world=monde) for a in abilites]
    message = Message.WhenPlayerChooseAbility(joueur, GameRule(identite), (1, 1), False)
    message.Send()
    # Le VRAI chemin (`ChooseEffects`), la reponse du joueur seule etant court-circuitee : premiere option offerte.
    offertes = []
    action = joueur
    d_origine = action.ChoiceAndSpellEffect
    def repondre(filtres, *a, **k):
        offertes.extend(filtres)
        return filtres[0], False
    action.ChoiceAndSpellEffect = repondre
    try:
        action.ChooseEffects(effets, message, forced=True)
    finally:
        action.ChoiceAndSpellEffect = d_origine
    noms = sorted(e.GetDisplayName() for e in offertes)
    if len(offertes) != 2:
        return False, f"options offertes : {noms} (attendu 2 : piocher, degats)"
    # Le VRAI controleur : `_RefusDesCartesAJouer` y rejoue un filtre par carte en main, ce qui ecrase
    # `derniers_refus`. C'est ce qui vidait le canal en partie reelle (vu au navigateur le 12/11/2026).
    controleur = monde.controller_manager.controllers[joueur.player_id]
    hors_choix = [r for r in controleur.RendreLesRefus(None) if r.is_text_choice]
    if hors_choix:
        return False, f"hors choix, des options de choix partent : {[r.name for r in hors_choix]}"
    autre = Message.WhenPlayerChooseAbility(joueur, GameRule(identite), (1, 1), False)
    perimes = [r for r in controleur.RendreLesRefus(None, choix=autre) if r.is_text_choice]
    if perimes:
        return False, f"une AUTRE question de choix recoit les refus de celle-ci : {[r.name for r in perimes]}"
    refus = [r for r in controleur.RendreLesRefus(None, choix=message) if r.is_text_choice]
    if len(refus) != 1 or "threat" not in refus[0].name.lower():
        return False, f"refus du choix : {[(r.name, r.failure_reason, r.is_text_choice) for r in refus]}"
    return True, f"offertes {noms} ; refusee « {refus[0].name} » ({refus[0].failure_reason})"
'''
