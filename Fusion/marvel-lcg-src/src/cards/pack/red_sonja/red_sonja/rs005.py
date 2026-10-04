from . import *

# Devil's Defiance — evenement signature, x2 (6-7/15). DEFENSE. Cout 1,
# ressource [Y].
# Hero Interrupt (defense): When an enemy attacks, prevent all damage from
# that attack. After this attack, give Red Sonja a tough status card.
#
# CARTE DE REFERENCE : `01003` Backflip (officiel), montage identique pour
# « prevent all damage » (`WhenUnitWouldTakeDamage(Interrupt, "You",
# is_from_attack=True).SetPlay().SetLabel('defense')`, `message.
# PreventDamage("All", effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « give Red Sonja a tough status card » : `Faces.GiveStatus`, cible
#    l'IDENTITE du joueur (Red Sonja = le heros, jamais un allie).
#  ⚠ ECART ASSUME, minime : « After this attack » -> pose le statut tout de
#    suite dans l'Interrupt plutot que dans un declencheur separe APRES
#    l'attaque. Sans consequence de jeu : la prevention couvre deja la
#    TOTALITE des degats de CETTE attaque (« prevent all »), donc rien ne
#    peut lire « Red Sonja a-t-elle Tough PENDANT cette attaque » de facon
#    pertinente -- le statut est de toute facon en place avant la suivante.

def GetAbilities() -> Sequence['Ability']:

    def devils_defiance(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

        joueur = effect.GetInitiator()
        if isinstance(joueur, Player):
            Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            devils_defiance,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
