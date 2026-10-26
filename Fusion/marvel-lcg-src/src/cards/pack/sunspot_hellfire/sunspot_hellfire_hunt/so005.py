from . import *

# Radiant Disruption — EVENEMENT, cout 1, RES [mental], x2. THWART.
# Hero Action (thwart): Remove X solar counters from Sunspot. Remove X threat from a scheme. If Sunspot has the AERIAL
#   trait, remove X threat from another scheme.
#
# CARTES DE REFERENCE
#  - `sw006` Psi-Web Trap : la jumelle (X compteurs retires -> X menaces retirees), X = ce qui est VRAIMENT retire.
#  - `48009` Scout Ahead : « from a scheme ... from ANOTHER scheme » = `MayChooseOneAbility(ForChoiceAbility(..).SetTarget(Scheme2, exclude=effect.targets))`.
#
# TEXTE CONTRE CODE
#  ⚠ X est choisi par le joueur (0 a stock) ; la seconde manigance n'est visee qu'avec le trait AERIAL, et elle est OBLIGATOIRE des qu'une
#    autre manigance existe (aucun « may » imprime ; verdict du 26/10/2026, RR « May ») : le joueur ne choisit que laquelle.
#  ⚠ Sans X (X = 0) : rien ne bouge.


def GetAbilities() -> Sequence['Ability']:

    def radiant_disruption(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cibles = [c for c in effect.targets if c is not None]
        if joueur is None or not cibles:
            return
        retire = RetirerSolaires(joueur, DemanderCombien(joueur, effect), effect)
        if retire <= 0:
            return
        this.RemoveThreatFromSchemes(cibles, retire, effect)
        if EstAerien(joueur) and [c for c in Worlds.GetOnFieldSchemes(effect) if c not in cibles]:
            # OBLIGATOIRE (corrige le 26/10/2026, RR « May ») : aucune option « Cancel » ; le joueur choisit seulement QUELLE autre manigance.
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda autres: this.RemoveThreatFromSchemes(autres, retire, effect),
                ).SetTarget(Scheme2, exclude=cibles),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            radiant_disruption,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
