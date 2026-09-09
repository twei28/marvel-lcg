from . import *

# Symbiotic Not Today! — EVENEMENT, cout 1, RES [mental]. DEFENSE. SYMBIOTE.
# Hero Interrupt (defense): When your hero defends against an attack, it gets
#   +2 DEF for that attack. If you take no damage from this attack, remove 2
#   threat from a scheme.
#
# CARTE DE REFERENCE
#  - `38016` Not Today! (Protection, pack rogue) : meme cout, meme ressource,
#    meme texte (« that attack » chez elle, « this attack » ici : meme attaque).
#    Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ « If you take NO damage » se lit APRES l'attaque : c'est
#    `message.IfYouTakeNoDamage`, une fenetre du moteur, et non un test pose
#    au moment de l'Interruption ou les degats ne sont pas encore connus.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_not_today(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.GainDEFForThisAttack(+2, effect)

        def retirer_de_la_menace():
            initiator = effect.GetInitiator()
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda targets:
                        this.RemoveThreatFromSchemes(targets, 2, effect)
                ).SetTarget(Scheme2)
            )

        message.IfYouTakeNoDamage(retirer_de_la_menace)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            symbiotic_not_today
        ).SetPlay().SetLabel('defense'),
    ]
