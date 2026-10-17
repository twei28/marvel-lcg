from . import *

# * Dreadmon — ALLIE 3 [energy], aspect Justice (TMNT Aspects, Inkwire). JACKAL. MUTANIMAL.
# PV 3, THW 2 (2 degats consecutifs), ATK 2 (2 degats consecutifs).
# [star] Response: After Dreadmon takes consequential damage ([consequential]), ready him.
# Forced Interrupt: When the round ends, discard Dreadmon.
#
# Le [star] (« ★ Response », et l'etoile a cote des valeurs 2 imprimees) est l'icone de rappel des Rules
# Reference (« Star Icon ») : une capacite du texte modifie l'usage de ces valeurs. Aucune ligne de code.
#
# CARTES DE REFERENCE
#  - `19012` Martyr / `tl009` : « After <allie> takes consequential damage » =
#    `AfterAllyTakeConsequentialDamage(type, which_ally, op)`, le message porte `trigger` = l'allie ;
#    condition « encore en jeu » en `conditions` (un allie vaincu par ses degats consecutifs ne se redresse
#    pas, la Reponse ne doit pas etre proposee).
#  - `bw015` / `16080b` : « Forced Interrupt: When the round ends » = `WhenRoundEnd(ForcedInterrupt, None, op)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After DREADMON takes consequential damage » : ses propres degats consecutifs (attaque OU contre),
#    pas ceux d'un autre allie. « ready HIM » : Dreadmon.
#  ⚠ Aucune limite imprimee : il peut se redresser apres chaque usage tant qu'il survit (PV 3, 2 degats
#    consecutifs par usage : le 2e usage le tue, la Reponse ne part alors pas).
#  ⚠ « Forced Interrupt » : OBLIGATOIRE, a la fin du round, Dreadmon est defausse (pas « vaincu »).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.ReadyAll([this], effect)

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            redresser,
            conditions=[lambda effect, message: effect.this.IsInPlay() and effect.this.IsExhaust()],
        ),
        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedInterrupt,
            None,
            fin_de_round,
        ),
    ]
