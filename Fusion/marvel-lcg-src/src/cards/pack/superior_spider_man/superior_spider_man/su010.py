from . import *

# Spider-Bot — AMELIORATION, cout 1 [mental]. TECH. Uses (3 surveillance).
# Hero Action (thwart): Exhaust Spider-Bot and remove 1 surveillance counter
#   from it -> track a minion or remove 1 threat from a scheme.
#
# CARTES DE REFERENCE
#  - `bl007` Bandolier of Stakes, `53006` : `CostFunc.Exhaust("This")` chaine
#    avec `CostFunc.Counter("This", 1, '<compteur>')` — RECETTES §5 : les deux
#    `SetCostFunc` s'ajoutent.
#  - `an004` : `RemoveThreatFromSchemes` pour la seconde branche.
#  - Le mot-cle maison `track` pour la premiere.
#
# TEXTE CONTRE CODE
#  ⚠ « Uses (3 surveillance counters) » est une BASE AUTOMATIQUE (`desc.Uses`,
#    fiche `uses.md`) : le moteur pose les pions a l'entree en jeu ET fait
#    SORTIR la carte au dernier pion retire. Ne PAS recoder la sortie.
#    ⚠ Le compteur `surveillance` a du etre AJOUTE a l'enum `COUNTER` le
#    08/09/2026 : il n'existait pas.
#  ⚠ « track a minion OR remove 1 threat » : deux branches, et la SECONDE
#    N'EST PAS un track (rien n'est pose sur un sbire). Les confondre ferait
#    disparaitre la moitie de la carte.
#  ⚠ La branche `track` n'est offerte que s'il y a de quoi tracer : sans sbire
#    ou sans menace, elle ne ferait rien et mangerait le pion quand meme.
#  ⚠ Aucune limite « once per » imprimee : etape 7 bis sans objet, ce sont les
#    3 pions qui bornent.


def GetAbilities() -> Sequence['Ability']:

    def spider_bot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def tracer(sbires: Sequence['CardFace']) -> None:
            sbire = next((c for c in sbires if c is not None), None)
            if sbire is None:
                return
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Move 1 threat from that scheme to the minion",
                    lambda complots: Tracer(effect, sbire, complots),
                ).SetTarget(Scheme2, range=(1, 1)),
            )

        def retirer(complots: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(
                [c for c in complots if c is not None], 1, effect)

        branches = []
        if PeutTracer(effect):
            branches.append(
                AbilityFactory.ForChoiceAbility("Track a minion", tracer)
                .SetTarget(Minion, range=(1, 1)))
        branches.append(
            AbilityFactory.ForChoiceAbility("Remove 1 threat from a scheme", retirer)
            .SetTarget(Scheme2, range=(1, 1)))
        joueur.ChooseAbilities(effect, *branches)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            spider_bot,
        ).SetName("Spider-Bot").SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, COMPTEUR_SURVEILLANCE)),
    ]
