from . import *

# Obstinance — amelioration signature, cout 1, ressource [mental]. CONDITION.
# Hero Interrupt: When you exhaust to use a basic power but before resolving its effects, exhaust Obstinance and spend
# 1 [mental] or [physical] resource → ready U.S. Agent.
#
# Cartes de reference :
#  - `ch017` Martial Mastery (meme auteur) : `WhenUnitUseBasicPower(HeroInterrupt, Hero, op, powers=["THW", "ATK", "DEF"],
#    control_by="You")` + `CostFunc.Exhaust("This")` : l'Interruption qui part quand le heros UTILISE un pouvoir de base
#    (apres l'inclinaison payee, avant la resolution).
#  - RECETTES §5 « Deux couts alternatifs (« A or B ») » : un cout est fige a la construction, le « or » devient DEUX
#    capacites (modeles `ar010`, `an003`). Ce ne sont pas des `Play` : la liste blanche de factory.py n'est pas concernee.
#
# ⚠ Mots-pieges :
#  - « When you EXHAUST to use a basic power » : ATQ, CTR ou DEF du heros (forme heros : Hero Interrupt) ;
#    « BEFORE resolving its effects » : le heros est redresse avant que le pouvoir ne resolve, donc PRET apres.
#  - « spend 1 [mental] OR [physical] resource » : deux capacites, `Cost("B")` et `Cost("R")` (la ressource [wild]
#    paie les deux) ; la couleur est celle des icones du texte, verifiee contre la carte du meme pack (Reckless RES=B).
#  - « exhaust OBSTINANCE and spend » : les DEUX couts, l'amelioration s'incline.


def GetAbilities() -> Sequence['Ability']:

    def obstinance(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Faces.ReadyAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Hero,
            obstinance,
            powers=["THW", "ATK", "DEF"],
            control_by="You",
        ).SetName("Spend a [mental] resource")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("B")),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            Hero,
            obstinance,
            powers=["THW", "ATK", "DEF"],
            control_by="You",
        ).SetName("Spend a [physical] resource")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("R")),
    ]
