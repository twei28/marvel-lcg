from . import *

# "Can't Escape Us!" — EVENEMENT, cout 2, RES [physical]. ATTACK.
# Action (attack): Deal 2 damage to an enemy. Exhaust a SYMBIOTE card you
#   control -> deal an additional 3 damage to that enemy.
#
# CARTE DE REFERENCE
#  - `32008` Steel Fist : « Deal 5 damage to an enemy. You may discard a tough
#    status card from your hero -> stun and confuse that enemy. » MEME FORME :
#    un effet garanti, puis une SECONDE fenetre dont le cout est une carte
#    qu'on possede, resolue par `MayChooseOneAbility` + `SetTarget2`.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » et non « Hero Action » : jouable dans LES DEUX formes, meme si
#    l'etiquette est `attack`.
#  ⚠ La seconde phrase n'est PAS obligatoire malgre l'absence de « you may » :
#    son cout (incliner une carte SYMBIOTE) peut etre impayable — aucune carte
#    SYMBIOTE, ou toutes deja inclinees. `MayChooseOneAbility` couvre les deux
#    cas sans bloquer la carte.
#  ⚠ « a SYMBIOTE card YOU CONTROL » : les cartes controlees, pas la main.
#  ⚠ « THAT enemy » : la meme cible que les 2 premiers degats, jamais une
#    autre -> `effect.targets`, pas un nouveau `SetTarget(Enemy)`.
def GetAbilities() -> Sequence['Ability']:

    def cant_escape_us(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)

        symbiotes = [f for f in joueur.GetControlCards()
                     if f is not this and PorteLeTraitSymbiote(f) and f.IsReady()]
        if not symbiotes:
            return

        def frapper_encore(cibles: Sequence['CardFace'], by_effect: 'Effect') -> None:
            Faces.ExhaustAll(by_effect.targets2, effect)
            this.DealDamage(cibles, 3, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility3(
                "Exhaust a SYMBIOTE card you control to deal 3 additional damage",
                frapper_encore
            ).SetTarget(effect.targets)
            .SetTarget2(symbiotes, is_optional=False),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            cant_escape_us
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
