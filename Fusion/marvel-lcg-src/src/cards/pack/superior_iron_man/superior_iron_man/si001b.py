from . import *

# * Tony Stark
#
# Setup : modele Wonder Man (wonder_man/wonder_man/58001b.py)
# BeginGameWithSetAside, qui cherche la carte set-aside par son NOM dans
# set_aside_deck/additional_discard_pile et la met en jeu sous controle.
#
# O.P.A. : modele Tony Stark OFFICIEL (core/iron_man/01029b.py), cite en
# commentaire de ag001b.py (agent_13) comme LA reference pour une action
# imprimee sur la face alter-ego elle-meme : AbilityType.Action (jamais
# AlterEgoAction, reserve aux AUTRES cartes qui doivent declarer explicitement
# qu'elles ne s'appliquent qu'en alter-ego). Le retrait de menace variable
# suit Active Altruism (wonder_man/wonder_man/58003.py) : valeur = 1 + X ou
# X est lu sur `effect.cost_func.Get(CostFunc.Spend).return_res`, modele
# Lightning Strike (thor/thor/06006.py) pour le cout "Spend X [couleur]
# resources (minimum 1)" -- `Cost("B")` = un symbole [mental] = minimum 1.

def GetAbilities() -> Sequence['Ability']:

    def with_endo_sym_armor(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        for area in (initiator.set_aside_deck, initiator.additional_discard_pile):
            for face in list(area.Get()):
                if face.paper.name == 'Endo-Sym Armor':
                    face.CastTo(Upgrade).PutIntoPlay(initiator, effect, under_control=True)
                    return

    def opa(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        res = effect.cost_func.Get(CostFunc.Spend).return_res
        value = res.GetColor("B")
        this.RemoveThreatFromSchemes(effect.targets, 1 + value, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(['si002'], with_endo_sym_armor),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            opa,
        ).SetName("O.P.A.")
        .SetLabel('thwart')
        .SetCostFunc(CostFunc.Spend(Cost("B")))
        .SetTarget(Scheme2, has_threat=True)
        .LimitOncePerPhase(),
    ]
