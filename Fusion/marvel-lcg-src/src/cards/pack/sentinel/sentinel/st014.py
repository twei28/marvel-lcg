from . import *

# Prime Directive — OBLIGATION de Sentinel, 3 icones de boost.
# <i>Give to the Sentinel player.</i>
# Forced Action: Choose one:
#  • Deal 3 damage to another friendly character ([[MUTANT]] if able) →
#    discard this card.
#  • Place 3 threat on the main scheme → discard this card.
#
# Cartes de reference :
#  - `nt012` Practice : l'obligation d'un heros maison, `WhenThisObligationGiveToYou`
#    + `ChooseAbilities` avec une `condition=` par branche.
#  - `01170` Business Problems : la meme forme officielle (« Choose: • ... »).
#  - `ih003` / `al012` : `AskChooseFace` pour designer une carte dans une liste
#    deja restreinte par le texte.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **another** friendly character » : un autre que VOUS. Ce sont donc vos
#    allies, jamais votre identite.
#  - « (**MUTANT if able**) » n'est pas un filtre de cible, c'est une
#    CONTRAINTE : s'il existe un allie MUTANT, la cible DOIT en etre un ; s'il
#    n'y en a pas, n'importe quel allie fait l'affaire. Un simple
#    `SetTarget(trait="MUTANT")` interdirait la branche en l'absence de mutant,
#    ce qui n'est pas ce que dit la carte. D'ou la liste calculee.
#  - Sentinel est un ANDROID, pas un MUTANT : le clin d'oeil vise Juston, qui
#    pilote un robot chasseur de mutants. Aucune carte du pack n'a le trait.
#  - Sans allie en jeu, la premiere branche n'existe pas : `condition=` la
#    retire, et la menace devient le seul choix. C'est bien le comportement
#    voulu, pas un blocage.
#  - Les deux branches DEFAUSSENT la carte : Prime Directive ne reste jamais
#    en jeu.


def GetAbilities() -> Sequence['Ability']:

    def prime_directive(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)

        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return

        allies: List['CardFace'] = list(joueur.GetControlAllies())
        mutants = [a for a in allies if a.HasTrait("MUTANT")]
        candidats = mutants if mutants else allies

        def blesser_un_allie(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            cible = joueur.AskChooseFace(candidats, effect)
            if cible is None:
                return
            this.DealDamage([cible], 3, effect)
            Faces.DiscardAll([this], effect)

        def charger_le_complot(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.PlaceThreatOnSchemes("MainScheme", 3, effect)
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to another friendly character (MUTANT if able) -> discard this card",
                blesser_un_allie,
                condition=bool(candidats),
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 3 threat on the main scheme -> discard this card",
                charger_le_complot,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            prime_directive,
        ),
    ]
