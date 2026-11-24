from . import *
def GetAbilities() -> Sequence['Ability']:
    def dance_with_the_devil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        Faces.DiscardAll([this], effect)
        if target:
            this.DealDamage([target], 3, effect)
    def check_team_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        units = Worlds.GetOnFieldFriendlyCharacters(effect.this.card.game_area)
        for name in ('Daredevil', 'Elektra'):
            if not any((u.IsName(name) or u.IsSubName(name)) for u in units):
                return False
        return True
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy), conditions=[check_team_up]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, dance_with_the_devil).SetLabel('attack')]
# 22/10/2026 : source de la carte officielle 63027 (Elektra Natchios, n° 27) ; `60031` (pack Daredevil) en est maintenant un lien `full_link`.
