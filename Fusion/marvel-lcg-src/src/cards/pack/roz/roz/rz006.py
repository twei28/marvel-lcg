from . import *

# Wakandan Stealth Tech — AMELIORATION, cout 2, [mental]. TECH. WAKANDA.
# Roz gets +1 DEF.
# Special: Draw 1 card (limit once per round).
# Special: Reduce the cost of the next card you play this turn by 1 (limit once per round).
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « gets +1 DEF » : `01028` (`GiveKeywordToAttached(CardFinder(name=...), defense=1)`).
#  - pioche : `01025` Split Personality (`joueur.DrawUp(1, effect)`).
#  - cout de la PROCHAINE carte : `nt008` Kickflip / `im001b` : `Worlds.UpdateNextCardPlayCost(joueur, -1, effect,
#    in_this="Turn")` (recette Shang-Chi : le montant est NEGATIF pour reduire).
#  - choix entre deux effets : `51025` (`ChooseAbilities` + `ForChoiceAbility(.., condition=...)`, helper `ResoudreSpecialSurAmelioration`).
#
# DECISION UTILISATEUR (26/10/2026, doute reel n°4) : quand une carte dit « resolve the "Special" ability on a WAKANDA
# upgrade », une carte qui imprime DEUX Specials n'en resout qu'UN SEUL, au choix du joueur (« the Special » est au
# singulier, chaque Special a sa propre limite). Rendu : UNE seule capacite `Special` pour le moteur (donc une seule
# resolution comptee pour `this_turn_resolved_specials`, Thor rz002 / rz003), qui fait choisir entre les deux effets
# imprimes ; seul un effet dont la limite du round est LIBRE est propose, et la limite est notee SUR LA CARTE
# (`rz006_pioche_round`, `rz006_reduction_round`) au moment de l'effet, pas au moment de la resolution.
#
# MOTS-PIEGES
#  - « (limit once per round) » : un marqueur de round par Special, jamais `LimitOncePerRound()` (il se consommerait
#    meme quand l'AUTRE Special est choisi). `effect.world.round_id` est le numero du round.
#  - « the NEXT card you play THIS TURN » : `in_this="Turn"`, d'un seul point ; l'effet part avec le tour.
#  - « Roz gets +1 DEF » : la face heros Roz (`CardFinder(name="Roz")`), pas l'alter ego.
def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect') -> None:
        joueur = JoueurDeCetteCarte(effect)
        effect.this.rz006_pioche_round = effect.world.round_id
        if joueur is not None:
            joueur.DrawUp(1, effect)

    def reduire_la_prochaine(effect: 'Effect') -> None:
        joueur = JoueurDeCetteCarte(effect)
        effect.this.rz006_reduction_round = effect.world.round_id
        if joueur is not None:
            Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Turn")

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        round_id = effect.world.round_id
        this = effect.this
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Draw 1 card",
                lambda targets: piocher(effect),
                condition=getattr(this, "rz006_pioche_round", None) != round_id,
            ),
            AbilityFactory.ForChoiceAbility(
                "Reduce the cost of the next card you play this turn by 1",
                lambda targets: reduire_la_prochaine(effect),
                condition=getattr(this, "rz006_reduction_round", None) != round_id,
            ),
        )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Roz"),
            defense=1,
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            special,
        ),
    ]
