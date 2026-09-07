from . import *

# On the Hunt — EVENEMENT, cout 0, [mental]. TACTIC. THWART. x2.
# Hero Action (thwart): Search the encounter deck for a minion and put it into
#   play engaged with you -> remove 3 threat from a scheme. If that minion has
#   the VAMPIRE trait, draw 1 card.
#
# CARTES DE REFERENCE
#  - `ar001a` Bring the War (Ares) : LE modele, `CostFunc.SearchForCard(Minion,
#    "PutIntoPlayEngagedYou", include_encounter_deck=True)` en COUT,
#    `searched_faces` relu dans l'effet, condition « le deck rencontre a un
#    sbire » (RECETTES §5, coût offert sans cible).
#  - `ls001a` : la manigance en cible de l'abilite (`SetTarget(Scheme2,
#    has_threat=True)`), une seule question.
#
# TEXTE CONTRE CODE
#  ⚠ « Search the encounter deck » -> le DECK seulement, pas la defausse
#    (contrairement a Lead the Charge, ar014).
#  ⚠ « -> » : le sbire convoque est le COUT. Sans sbire dans le deck, la carte
#    n'est pas offerte.
#  ⚠ « If THAT minion has the VAMPIRE trait » -> lu sur le sbire convoque,
#    apres son entree en jeu (Blood Hunt en jeu lui DONNE le trait : il compte).
#  ⚠ Le sbire entre en jeu AVANT le retrait de menace : sa capacite d'entree
#    (Teamwork, Quickstrike...) part d'abord.


def GetAbilities() -> Sequence['Ability']:

    def deck_rencontre_a_un_sbire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        deck = Worlds.GetEncounterDeck(effect)
        if deck is None:
            return False
        return any(f is not None and Minion.IsType(f) for f in list(deck.GetAll()))

    def on_the_hunt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        cout = effect.cost_func.Get(CostFunc.SearchForCard)
        sbires = [s for s in list(getattr(cout, "searched_faces", []) or [])
                  if s is not None and Minion.IsType(s)]
        for sbire in sbires:
            if sbire.card.IsOnField():
                sbire.CastTo(Minion).EngagePlayer(joueur, effect)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if any(s.HasTrait(TRAIT_VAMPIRE) for s in sbires):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            on_the_hunt,
            conditions=[deck_rencontre_a_un_sbire],
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.SearchForCard(
            Minion, "PutIntoPlayEngagedYou", include_encounter_deck=True))
        .SetTarget(Scheme2, has_threat=True),
    ]
