from . import *
def GetAbilities() -> Sequence['Ability']:
    def unbreakable_bond(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        # La machination est DECALEE en `targets2` : le premier selecteur est
        # desormais « TeamUp ». Modele Fastball Special (35023).
        this.RemoveThreatFromSchemes(effect.targets2, 3, effect)
        jj = Worlds.FindCardOnField(effect, name='Jessica Jones')
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        total = 3
        for c in (jj, lc):
            if not c or total <= 0:
                continue
            amount = min(total, c.GetLostHealth())
            if amount > 0:
                c.HealHealth(amount, effect)
                total -= amount
    def check_team_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        units = Worlds.GetOnFieldFriendlyCharacters(effect.this.card.game_area)
        for name in ('Jessica Jones', 'Luke Cage'):
            if not any((u.IsName(name) or u.IsSubName(name)) for u in units):
                return False
        return True
    return [
        # CORRECTIF (29/08/2026) : le selecteur « TeamUp » manquait.
        # `CardsDB.FindAbilities` (database.py:222) exige que le PREMIER
        # selecteur d'un evenement portant la cle desc `TeamUp` vaille
        # exactement « TeamUp » : c'est lui qui impose Jessica Jones ET Luke
        # Cage en jeu. Sans lui, `AssertionError: origin_card_id='61027'`, et
        # aussi `'62024'` qui est sa reimpression liee (`full_link`) dans le
        # pack Luke Cage. Les decks jessica_jones et luke_cage ne montaient pas.
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, unbreakable_bond, conditions=[check_team_up])
        .SetPlay().SetLabel('thwart')
        .SetTarget("TeamUp")
        .SetTarget2(Scheme2, range=(1, 1)),
    ]
