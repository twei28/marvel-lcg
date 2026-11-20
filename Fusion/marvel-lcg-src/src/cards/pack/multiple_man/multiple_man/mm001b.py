from . import *

# * Jamie Madrox (face ALTER-EGO, UNIQUE) : MUTANT. REC 3, main 6, PV 9.
# Reabsorb Dupe — Action: (Limit once per round.) Discard a Dupe Ally from play, then choose 1:
#  • Heal 2 damage from Jamie Madrox.
#  • Remove 2 threat from a scheme.
#  • Multiple Man and all Dupe allies get +1 to all basic powers until the end of the round.
# + les bonus des complots annexes qui ne dependent pas de la forme (limite d'allies, Tenace des Dupe : `CapacitesCommunesIdentite`).
#
# CARTES DE REFERENCE : `mystique/my001b` (`WhenInYourPlayTurn(Action, op).SetName(..).LimitOncePerRound()`), `ca014` (`ForChoiceAbility` + `ChooseAbilities`), `ca001a` (`HealthUnits`), `lj019` / `ra009`
#  (`RemoveThreatFromSchemes`).
# TEXTE CONTRE CODE
#  « Discard a Dupe Ally FROM PLAY, THEN choose 1 » : RRG « Then » : le texte avant « then » doit etre pleinement resolu avant la suite ; sans Dupe en jeu l'Action n'est PAS offerte (condition) : pas de choix gratuit.
#  Le Dupe defausse est choisi par le joueur (n'importe quel Dupe en jeu). « Heal 2 damage FROM JAMIE MADROX » : l'identite. « Remove 2 threat from A scheme » : choisie par le joueur ; la source est Jamie (pas un
#  Dupe) : les complots « Only a Dupe ally... » refusent (decision utilisateur du 04/11). 3e option : DECISION UTILISATEUR (04/11) : le +1 aux pouvoirs de base (THW/ATQ/DEF du heros, THW/ATQ des Dupe) reste
#  jusqu'a la fin du round meme apres le retournement en heros : `GainUntilRoundEnd` sur l'identite et sur chaque Dupe EN JEU a la resolution. Chiffres : PV 9, main 6, REC 3.


def GetAbilities() -> Sequence['Ability']:

    def au_moins_un_dupe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and bool(DupesDuJoueur(joueur))

    def reabsorb(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        dupes = DupesDuJoueur(joueur)
        if not dupes:
            return
        choisi = joueur.AskChooseFace(dupes, effect, forced=True) if len(dupes) > 1 else dupes[0]
        if choisi is None or not Faces.DiscardAll([choisi], effect):
            return

        def soigner(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.HealthUnits([joueur.GetIdentity()], 2, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            manigances = Worlds.FindCardsOnField(effect, card_type=Scheme2)
            if not manigances:
                return
            cible = joueur.AskChooseFace(manigances, effect, forced=True) if len(manigances) > 1 else manigances[0]
            if cible is not None:
                this.RemoveThreatFromSchemes([cible], 2, effect)

        def bonus(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            # « until the end of the round » : gain TEMPORAIRE sur les cartes en jeu au moment de la resolution. L'identite est la MEME carte sous ses deux faces : `GainUntilRoundEnd` (ignore_flip) reste
            # donc actif apres le retournement en heros (decision utilisateur du 04/11).
            joueur.GetIdentity().GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1)
            for dupe in DupesEnJeu(effect):
                dupe.GainUntilRoundEnd(effect, attack=1, thwart=1)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Heal 2 damage from Jamie Madrox", soigner).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Remove 2 threat from a scheme", retirer).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Multiple Man and all Dupe allies get +1 to all basic powers until the end of the round", bonus).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reabsorb,
            conditions=[au_moins_un_dupe],
        ).SetName("Reabsorb Dupe").LimitOncePerRound(),
        *CapacitesCommunesIdentite(),
    ]
