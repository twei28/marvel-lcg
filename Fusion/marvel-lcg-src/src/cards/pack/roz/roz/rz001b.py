from . import *

# * Rosalind Solomon (face ALTER EGO) — PV 9, REC 3★, main 6. S.H.I.E.L.D. SPY. WAKANDA.
# Setup: Find a [[WAKANDA]] upgrade and add it to your hand.
# [star] Agent E-23 — Response: After you make a basic recovery, search your deck for a [[S.H.I.E.L.D]] or
#   [[WAKANDA]] card and add it to your hand.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - Setup : `01040b` T'Challa (« Search your deck for a [[Black Panther]] upgrade and add it to your hand ») :
#    `WhenCardSetup("This", op)` + `Search.PlayerCard(...)` + `GainCard`. Le moteur REMELANGE le deck apres
#    la recherche.
#  - Response : `45015` Sidekick et `34001b` : `AfterUnitMakeRecovery(Response, "You", op, is_basic_recovery=True)`.
#  - « S.H.I.E.L.D. OR WAKANDA card » : `an001b` / `bl002` Gear Up : `finder=CardFinder(traits=[...])` (OU).
#
# MOTS-PIEGES
#  - « FIND » (Setup) : `Worthy` / `Starfarer` (pack beta_ray_bill, RECETTES) : « find » couvre le DECK ET LA
#    DEFAUSSE (« seek » = pioche jusqu'a, « search your deck » = deck seul). On cherche donc dans les deux.
#  - « search your DECK » (Response) : le deck SEUL, pas la defausse.
#  - « BASIC recovery » : `is_basic_recovery=True` (une guerison par une carte n'est pas une recuperation de base).
#  - REC « 3★ » : `desc.REC = "3*"` ; la valeur de base vaut 3.
def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            trait=TRAIT_WAKANDA,
            card_type=Upgrade,
        )
        if face:
            joueur.GainCard(face, effect)

    def agent_e23(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            finder=CardFinder(traits=["S.H.I.E.L.D", TRAIT_WAKANDA]),
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.AfterUnitMakeRecovery(
            AbilityType.Response,
            "You",
            agent_e23,
            is_basic_recovery=True,
        ).SetName("Agent E-23"),
    ]
