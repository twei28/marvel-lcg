from . import *

# * Frenzied Violence : AMELIORATION (CONDITION.), cout 2, [energy]. Classe Hero.
# Carnage gets +1 ATK and his basic attacks gain overkill.
# Hero Response: After you attack and defeat an enemy, exhaust this card -> ready Carnage.
#
# CARTES DE REFERENCE
#  - « NOM gets +1 ATK and his basic attacks gain overkill » : `im012` (Hulkbuster Armor) : `GiveKeywordToAttached(Hero, attack=1)` + `UnitAttackGainKeyword("You", overkill=True, is_basic_attack=True)` (fiche mots-cles/overkill.md).
#  - « After you attack and defeat an enemy » : `an004` (Murderous Glare) / ar005 : `AfterUnitDefeatedUnit(HeroResponse, "You", Enemy, op, is_from_attack=True)` ; « ready Carnage » : `Faces.ReadyAll` (`an001a`).
#
# TEXTE CONTRE CODE
#  « CARNAGE gets +1 ATK » : nom propre, face heros (`Hero`). « his BASIC attacks gain overkill » : `is_basic_attack=True` (Chomp, Vicious Lashing et Rend n'en profitent pas par cette ligne).
#  « Hero Response: After YOU attack AND defeat AN enemy » : `HeroResponse` + `"You"` + `Enemy` (vilain compris) + `is_from_attack=True`. « exhaust this card → » : COUT (`CostFunc.Exhaust("This")`). « ready CARNAGE » : l'identite, pas la carte.
#  Chiffres : cout 2, +1 ATK.


def GetAbilities() -> Sequence['Ability']:

    def frenzied_violence(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            overkill=True,
            is_basic_attack=True,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Enemy,
            frenzied_violence,
            is_from_attack=True,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
