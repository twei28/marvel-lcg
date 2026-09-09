from . import *

# Symbiotic Multitasking — EVENEMENT, cout 1, RES [physical]. SYMBIOTE. THWART.
# Hero Action (thwart): Remove 2 threat form a scheme. If you paid for this
#   card using a [mental] resource, remove 2 threat from a different scheme.
#
# ⚠ « form » AU LIEU DE « from » : COQUILLE IMPRIMEE de l'auteur, reproduite
# telle quelle dans `cards.json` — on porte ce qui est IMPRIME. L'officielle
# `15013` ecrit « from », et c'est bien ce que la carte fait.
#
# CARTE DE REFERENCE
#  - `15013` Multitasking (Justice, pack scw) : meme cout, meme ressource,
#    meme texte a la coquille pres. Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ « a DIFFERENT scheme » -> `exclude=effect.targets` : sans cela le second
#    retrait pourrait retomber sur la premiere manigance.
#  ⚠ Le second retrait est un CHOIX qui peut ne pas exister (une seule
#    manigance en jeu) : il passe par `ChooseAbilities`, jamais en direct.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_multitasking(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        if effect.GetPaidResources().GetColor("B"):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "",
                    lambda targets:
                        this.RemoveThreatFromSchemes(targets, 2, effect)
                ).SetLabel('thwart')
                .SetTarget(Scheme2, exclude=effect.targets),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            symbiotic_multitasking
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
