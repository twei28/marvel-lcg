from . import *

# Silver Up — Evenement, cout 2, ressource [energy]. COSMIC. SUPERPOWER.
# When you play this card, you may discard The Silver Surfboard, then choose two instead.
# Alter-Ego Action: Flip to Silver Surfer, then choose one: draw 2 cards, deal 4 damage to an enemy, or ready
#   Silver Surfer.
#
# Cartes de reference :
#  - `ls005` To Arms! (lady_sif) : Action d'alter-ego « Change to hero form » puis effet, un seul module.
#  - `14004` Double Time (qsv) : `ChooseAbilities` pour le choix ; `choose_x_different_options=2` pour « choose
#    two » (deux options DIFFERENTES).
#  - `lj*` (Lockjaw) : `identite.ChangeToOtherIdentityForm(effect)` pour « flip ».
#
# ⚠ Mots-pieges :
#  - la defausse de la planche est FACULTATIVE (« you may ») et vient AVANT le choix ; elle fait passer le choix
#    de UNE a DEUX options (differentes). Sans planche en jeu, on ne la propose pas.
#  - « Flip to Silver Surfer, THEN choose » : le retournement precede le choix, donc « ready Silver Surfer »
#    redresse la face heros qui vient d'arriver.
#  - la planche est defaussee en forme ALTER-EGO : l'Interruption de sv003 (1 degat a Silver Surfer) n'est pas
#    payable ici (lecture litterale, le Surfer n'est pas en jeu), donc pas de pioche.
#  - Une seule capacite de jeu (Alter-Ego Action), pas de liste blanche.


def GetAbilities() -> Sequence['Ability']:

    def silver_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        deux = []

        def defausser_la_planche(cibles: Sequence['CardFace']) -> None:
            planche = LaPlanche(effect, joueur)
            if planche is not None:
                Faces.DiscardAll([planche], effect)
                deux.append(True)

        if LaPlanche(effect, joueur) is not None:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard The Silver Surfboard (choose two instead)",
                    defausser_la_planche,
                ).SetHasNoTargetEffect(),
            )

        ChangerDeForme(joueur, effect)

        def piocher(cibles: Sequence['CardFace']) -> None:
            joueur.DrawUp(2, effect)

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(cibles, 4, effect)

        def redresser(cibles: Sequence['CardFace']) -> None:
            identite = joueur.GetIdentity()
            if identite is not None and Hero.IsType(identite):
                Faces.ReadyAll([identite], effect)

        options = [
            AbilityFactory.ForChoiceAbility("Draw 2 cards", piocher).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Deal 4 damage to an enemy", frapper).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility("Ready Silver Surfer", redresser).SetHasNoTargetEffect(),
        ]
        if deux:
            joueur.ChooseAbilities(effect, *options, choose_x_different_options=2)
        else:
            joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            silver_up,
        ).SetPlay(),
    ]
