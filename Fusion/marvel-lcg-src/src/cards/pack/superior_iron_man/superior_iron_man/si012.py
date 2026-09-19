from . import *

# Spectacular Save
#
# Decision utilisateur (29/08/2026) : les 2 exemplaires (013/014 sur les
# scans) sont identiques en Interruption de heros -- la traduction francaise
# de l'exemplaire 014 disait a tort "Reponse", l'anglais original de l'auteur
# (« Hero Interrupt (defense/thwart) ») confirme Interrupt sur les DEUX. Une
# Reponse ne pourrait de toute facon pas prevenir des degats deja subis.
# Modele Human Shield (determination/dt006.py) pour la fenetre
# `WhenUnitWouldTakeDamage` + `PreventDamage`, filtre "personnage ami"
# (controle par l'initiateur, pas seulement l'identite).

def GetAbilities() -> Sequence['Ability']:

    def check_friendly(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        initiator = effect.GetInitiator()
        unit = message.trigger
        # CORRECTIF (18/09/2026) : un ENNEMI qui subit des degats (Rhino
        # attaque par le heros) passe aussi par cette fenetre, et
        # `GetControlByPlayer()` leve `assert isinstance(owner, Player)` sur
        # lui : la partie plantait au premier coup porte avec cette carte en
        # main (passe complete des decks du 18/09/2026, 135/136). On lit le
        # controleur sans assert et on ne garde que les personnages AMIS.
        controleur = unit.GetControlByOrOwner()
        return Player.IsType(controleur) and controleur == initiator

    def spectacular_save(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        message.PreventDamage(3, effect)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            spectacular_save,
            conditions=[check_friendly],
        ).SetPlay().SetLabel('defense', 'thwart')
        .SetTarget(Scheme2, has_threat=True),
    ]
