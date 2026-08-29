from . import *

# Shield Arts
# Hero Interrupt: When Red Guardian uses a basic power against an enemy or a
#   scheme with Red Guardian's Shield attached, exhaust Shield Arts -> choose
#   to either return Red Guardian's Shield to your hand or ready Red Guardian.
#
# Declencheur : `WhenUnitUseBasicPower`, nomme sur Red Guardian comme Falcon le
# fait avec Battlefield Awareness (53010) — meme montage exact : interruption de
# heros, `CardFinder(name=...)`, cout `CostFunc.Exhaust("This")`.
#
# La cible du pouvoir se lit sur `message.would_message`, le message « would
# attack / would thwart » que le moteur transporte : ses `targets` sont les
# ennemis attaques ou les manigances contrariees. Il suffit de verifier que le
# porteur du bouclier s'y trouve.
#
# ECART ASSUME : seuls ATK et THW sont ecoutes.
#
# Le mot qui tranche est « AGAINST an enemy or a scheme » : le texte decrit une
# relation de CIBLAGE, et les deux seuls pouvoirs de base qui prennent une cible
# dans l'ensemble {ennemis, manigances} sont ATK et THW. C'est exactement ce que
# reflete le moteur : `WhenUnitWouldAttack` et `WhenUnitWouldThwart` portent des
# `targets`, `WhenUnitWouldDefend` n'a qu'un `attacker` (on ne pointe pas sa
# defense sur un ennemi, c'est lui qui pointe sur vous) et `WhenUnitWouldRecovery`
# n'a rien du tout. REC est de surcroit un pouvoir d'alter-ego, hors de portee
# d'un « Hero Interrupt ».
#
# Consequence assumee, verifiee en partie reelle : Red Guardian qui DEFEND contre
# l'ennemi porteur du bouclier ne declenche pas Shield Arts. Un joueur qui lit
# « basic power » sans s'arreter sur « against » s'attendrait a l'inverse ; le
# jour ou l'on tranche dans l'autre sens, il suffit d'ajouter "DEF" a `powers` et
# de lire `message.would_message.attacker` dans `contre_le_porteur`.


def GetAbilities() -> Sequence['Ability']:

    def contre_le_porteur(effect: 'Effect',
                          message: 'Message.WhenUnitUseBasicPower') -> bool:
        porteur = CibleDuBouclier(effect)
        if porteur is None:
            return False
        cibles = getattr(message.would_message, 'targets', [])
        return any(cible is porteur for cible in cibles)

    def shield_arts(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # Le declencheur EST Red Guardian : c'est lui qu'on redresse.
        heros = message.trigger

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Return Red Guardian's Shield to your hand",
                lambda targets: RendreLeBouclier(effect, joueur),
            ),
            AbilityFactory.ForChoiceAbility(
                "Ready Red Guardian",
                lambda targets: Faces.ReadyAll([heros], effect),
            ),
        )

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            CardFinder(name="Red Guardian"),
            shield_arts,
            conditions=[contre_le_porteur],
            powers=["ATK", "THW"],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
