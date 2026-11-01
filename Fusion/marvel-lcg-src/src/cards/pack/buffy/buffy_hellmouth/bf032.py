from . import *

# * Angelus — SBIRE (ELITE. VAMPIRE. HELLMOUTH). SCH 2, ATQ 2*, PV 7, boost 2. Guard. Victory 0.
# [star] Angelus's attacks gain piercing.
# When Defeated: Find Angel and put him into play under any player's control.
#
# CARTES DE REFERENCE : `04012` (piercing sur « ses attaques »), `32159` (When Defeated), `bf031` (« under any player's control »).
# TEXTE CONTRE CODE : « Angel » -> l'allie `bf017` (Linked (Angelus), mis de cote). Filtre `Ally` : « Angelus » et « Angel » sont deux noms distincts.


def GetAbilities() -> Sequence['Ability']:

    def angelus(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.GetKillerPlayer() or Worlds.GetFirstPlayer(effect)
        angel = Search.SearchForCard(effect, joueur, include_set_aside=True, name=NOM_ANGEL, card_type=Ally)
        if angel:
            angel.PutIntoPlay(ChoisirUnJoueur(effect, joueur), effect, under_control=True)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            angelus,
        ),
    ]
