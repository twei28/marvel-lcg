from . import *

# Total Authority — AMELIORATION, cout 2, RES [physical]. CONDITION.
# You gain steady.
# Hero Action: After Iron Patriot uses a basic power -> resolve the "Special"
#   ability on 1 REGISTERED ally you control.
#
# CARTE DE REFERENCE
#  - `ip001b` Norman Osborn : la resolution d'un « Special », par
#    `face.ResolveSpecialAbility(joueur, effect)`. Ici le declencheur est un
#    POUVOIR DE BASE et non une Action d'alter ego.
#  - `40049` Probability Field : le declencheur « when you use a basic power ».
#
# TEXTE CONTRE CODE
#  ⚠ « You gain STEADY » : mot-cle donne a l'IDENTITE, pas a la carte. Base
#    native par `GiveKeywordToInPlayWhenApplyThis(..., steady=1)`.
#  ⚠ « Hero Action: AFTER ... » : le texte melange les deux formes. C'est une
#    REPONSE dans les faits — elle suit un pouvoir de base — mais elle est
#    imprimee « Hero Action ». On monte donc le declencheur sur la fenetre
#    « apres un pouvoir de base » avec le type Reponse de heros, seule lecture
#    qui rende la carte jouable ; l'ecart de vocabulaire est celui de l'auteur.
#  ⚠ « 1 REGISTERED ally YOU CONTROL » : pas ceux des autres joueurs.


def GetAbilities() -> Sequence['Ability']:

    def autorite_totale(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for allie in effect.targets:
            allie.ResolveSpecialAbility(joueur, effect)

    def un_allie_registered(effect: 'Effect') -> Sequence['CardFace']:
        return AlliesRegistredPouvantResoudreUnSpecial(effect.GetInitiator())

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            control_by="You",
            steady=1,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "YourHero",
            autorite_totale,
        ).SetTarget(un_allie_registered),
    ]
