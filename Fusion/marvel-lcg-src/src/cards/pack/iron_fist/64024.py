from . import *
def GetAbilities() -> Sequence['Ability']:
    def power_man_and_iron_fist(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        # Les cibles sont DECALEES d'un cran : le premier selecteur est
        # desormais « TeamUp », donc l'ennemi est en `targets2` et le
        # personnage a rendre tough en `targets3`. Modele Fastball Special
        # (35023), qui fait exactement ce decalage.
        this.AttackDamage(effect.targets2, 2, effect)
        Faces.GiveStatus(effect.targets3, "Tough", effect)
    def check_team_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        units = Worlds.GetOnFieldFriendlyCharacters(effect.this.card.game_area)
        for name in ('Iron Fist', 'Luke Cage'):
            if not any((u.IsName(name) or u.IsSubName(name)) for u in units):
                return False
        return True
    return [
        # CORRECTIF (29/08/2026) : le selecteur « TeamUp » manquait.
        # `CardsDB.FindAbilities` (database.py:222) exige que le PREMIER
        # selecteur d'un evenement portant la cle desc `TeamUp` vaille
        # exactement « TeamUp » : c'est lui qui impose la presence des DEUX
        # personnages nommes. Sans lui, `AssertionError: origin_card_id='62023'`
        # et le deck luke_cage ne montait pas.
        # Le `check_team_up` maison ci-dessus fait le meme travail a la main ;
        # on le garde, il ne nuit pas, mais le selecteur est desormais la garde
        # native du moteur.
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, power_man_and_iron_fist, conditions=[check_team_up])
        .SetPlay().SetLabel('attack')
        .SetTarget("TeamUp")
        .SetTarget2(Enemy, range=(1, 1))
        .SetTarget3(Unit2, range=(1, 1)),
    ]
