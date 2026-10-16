from . import *

# * Alopex's Kama — AMELIORATION signature, x1 (14/16). KAMA. NINJA. WEAPON.
# Cout 1, [mental]. Restricted.
# Each [[KAMA]] upgrade you control gains: "Hero Response: After Prey leaves
#   play, exhaust this card and spend a [mental] resource -> ready Alopex."
#
# Cartes de reference :
#  - « each X upgrade you control GAINS an ability » : DECISION UTILISATEUR
#    (15/10/2026, decisions-phase-b.md, Katana / Nunchuck) : VRAI octroi,
#    `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(finder, control_by="You",
#    given_abilities=[...])` (`leonardo/tl011`, `michelangelo/tm011`) ;
#  - declencheur : `AfterCardLeavePlay(HeroResponse, CardFinder(name="Prey"), op)`
#    (card_move.py:258) ;
#  - cout « exhaust this card AND spend a [mental] resource » : deux parties,
#    `SetCost(Cost("B"))` + `SetCostFunc(CostFunc.Exhaust("This"))`.
#
# Mots-pieges :
#  - « EACH KAMA upgrade you control GAINS » : CHAQUE Kama controle, y compris
#    cette carte et ta010 ; sans ta009 en jeu, ta010 n'a pas cette Reponse ;
#  - « exhaust THIS card » : la Kama qui porte la capacite donnee, pas ta009 ;
#  - « ready ALOPEX » : l'identite du joueur (face heros) ;
#  - Restricted : base automatique (desc), RIEN a coder.


def GetAbilities() -> Sequence['Ability']:

    def redresser_alopex(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    reponse_donnee = AbilityFactory.AfterCardLeavePlay(
        AbilityType.HeroResponse,
        CardFinder(name=NOM_PREY),
        redresser_alopex,
    ).SetCostFunc(CostFunc.Exhaust("This")) \
     .SetCost(Cost("B"))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait=TRAIT_KAMA, card_type=Upgrade),
            control_by="You",
            given_abilities=[reponse_donnee],
        ),
    ]
