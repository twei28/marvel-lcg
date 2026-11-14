from . import *
# * Captain of the Starjammer (Leadership, amelioration 3 [energy]). TITLE.
# Your identity gains the STARJAMMER trait.
# Hero Response: After you use a basic power, each STARJAMMER ally you control gets +1 to that basic power until the end of the phase.
#
# Cartes de reference : 06007 Asgard / 03xxx (`*GiveKeywordToAttached("You", trait=..)` = « YOU gain trait » : l'IDENTITE, les deux faces ;
# RECETTES §3) ; 14001a Quicksilver (`AfterUnitUseBasicPower(HeroResponse, "You", op)`) ; sy033 (`GainUntilPhaseEnd(effect, **bonus)`).
# « YOU gain the trait » : identite = heros ET alter ego. « each STARJAMMER ALLY you control » : les allies (pas l'identite), controles par le joueur.
# L'amelioration entre en jeu pres de l'identite (aucune cible d'attache imprimee) ; unique (✦).
def GetAbilities() -> Sequence['Ability']:
    def captain(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = JoueurDe(effect)
        bonus = BonusAuPouvoir(message.power)
        if joueur is None or not bonus:
            return
        for allie in joueur.GetControlAllies():
            if allie.IsInPlay() and allie.HasTrait("STARJAMMER"):
                allie.GainUntilPhaseEnd(effect, **bonus)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached("You", trait="STARJAMMER"),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            captain,
            powers=["ATK", "THW", "DEF"],
        ),
    ]
