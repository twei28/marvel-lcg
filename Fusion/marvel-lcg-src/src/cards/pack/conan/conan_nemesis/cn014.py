from cards.pack.conan.conan import *

# Frozen Ambush — manigance annexe du set nemesis (1/5). Menace de depart 4.
# Amplify x1, Boost x3 (glyphes F et B de ChampionsIcons.ttf, verifies).
# Forced Response: After an identity changes form place 2 threat here.
#
# CARTES DE REFERENCE
#  - `AfterUnitChangeForm(ForcedResponse, Identity, op)` (factory/form.py).
#  - poser de la menace sur soi : `this.PlaceThreat(2, effect)`.
#
# TEXTE CONTRE CODE
#  « an identity » : N'IMPORTE QUELLE identite (tous les joueurs).
#  Le couronnement de Conan n'est pas un changement de forme (arbitrage du
#  25/09/2026) : il ne pose rien ici.


def GetAbilities() -> Sequence['Ability']:

    def frozen_ambush(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        Unused(message)
        this = effect.this.CastTo(SchemeSide2)
        this.PlaceThreatOnSchemes([this], 2, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            Identity,
            frozen_ambush,
        ),
    ]
