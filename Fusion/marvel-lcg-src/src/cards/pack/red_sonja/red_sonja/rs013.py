from . import *

# * Hyrkanium Blade — amelioration signature, x1 (15/15). WEAPON. Cout 2,
# ressource [R].
# Red Sonja's basic attacks gain piercing.
# Response: After you defeat a side scheme or minion, ready Hyrkanium
# Blade. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `av001a` Agent Anti-Venom : `AbilityFactory.UnitAttackGainKeyword("You",
#    piercing=True, is_basic_attack=True)` pour « basic attacks gain
#    piercing » -- restreint aux pouvoirs de base, contrairement a une
#    attaque d'evenement.
#  - `wave/65006.py` Ocean's Fury : « defeats an enemy OR removes the last
#    threat » -> deux fabriques enregistrees ensemble, meme corps.
#  - `AfterSchemeRemoveThreat(by_who="You", last_threat=True)`
#    (scheme.py:156) pour « defeat a side scheme » (vaincre = retirer la
#    DERNIERE menace) ; aucun type Python dedie « SideScheme » distinct de
#    `Scheme2` -- exclu la manigance PRINCIPALE par condition
#    (`not MainScheme.IsType(...)`), la manigance principale ne se « vainc »
#    jamais au sens de cette carte.
#
# TEXTE CONTRE CODE
#  ⚠ « a side scheme OR minion » : deux declencheurs distincts, meme effet.
#  ⚠ « Limit once per round » : sur la capacite de READY elle-meme, pas sur
#    le passif de percee (qui n'a pas de limite imprimee).

def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.ReadyAll([this], effect)

    def pas_la_manigance_principale(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        return not MainScheme.IsType(message.trigger)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            piercing=True,
            is_basic_attack=True,
        ),
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.Response,
            Scheme2,
            redresser,
            by_who="You",
            last_threat=True,
            conditions=[pas_la_manigance_principale],
        ).LimitOncePerRound(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            redresser,
        ).LimitOncePerRound(),
    ]
