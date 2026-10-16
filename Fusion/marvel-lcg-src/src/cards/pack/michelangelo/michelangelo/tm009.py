from . import *

# * I'm Here to Help — manigance-joueur signature, x1 (12/15). StartingThreat 3.
# This card does not count against the player side scheme limit.
# Forced Response: After the player phase ends, remove 1 threat from this card.
# Hero Interrupt: When this scheme is defeated, draw 3 cards (only the
#   Michelangelo player can trigger this ability).
#
# Regle de l'insert : « When the "I'm Here to Help" side scheme is defeated,
# you must be in hero form to draw the 3 cards. »
#
# Cartes de reference :
#  - hors limite : `jj/jessica_jones/61007` Piecing It All Together —
#    `WhenCardSetup("This", ...)` + `not_count_player_side_scheme_limit = True`
#    (world/limit_monitor/player_side_scheme_limit.py) ;
#  - fin de la phase des joueurs : `aos/maria_hill/50029` Press Conference —
#    `AfterPhaseEnd(ForcedResponse, "Player", op)` ;
#  - retrait de menace sur soi : `jubilee/jubilee/47003` Shopping Spree
#    (`this.RemoveThreatFromSchemes([this], 1, effect)`) ;
#  - « when defeated, draw » : 61007 (`WhenSchemeBeDefeated`), ici en
#    INTERRUPTION de heros (`AbilityType.HeroInterrupt`, la condition
#    `initiator.IsHero()` rend automatiquement la regle de l'insert).
#
# ⚠ Mots-pieges :
#  - « After the player phase ENDS » : `AfterPhaseEnd`, pas le debut.
#  - Le dernier point de menace retire par la Reponse forcee VAINC la
#    manigance : l'Interruption se declenche alors (3 cartes) si le joueur
#    est en forme de heros. C'est la lecture litterale.
#  - « only the Michelangelo player can trigger » : on exige que l'initiateur
#    soit le PROPRIETAIRE de la carte ; il pioche, pas le joueur qui a vaincu
#    (decision de l'utilisateur, 15/10/2026 : l'insert tranche, forme heros
#    obligatoire + « only the Michelangelo player » = proprietaire).
#  - `CanPlayThisSchemeCard()` : la carte peut aussi etre jouee depuis la
#    main (Call for Help l'y ajoute) ; cout imprime 0.

def GetAbilities() -> Sequence['Ability']:

    def hors_limite(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        effect.this.not_count_player_side_scheme_limit = True

    def retirer_une_menace(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(message)
        this.RemoveThreatFromSchemes([this], 1, effect)

    def le_proprietaire(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        # `defeating_player` = le joueur qui vainc la manigance (le controleur de la carte qui la
        # vainc, sinon l'initiateur de l'effet) ; `effect.GetInitiator()` serait toujours le
        # proprietaire de tm009 (l'effet est le SIEN) et laisserait piocher quand un autre la vainc.
        return message.defeating_player is not None and \
            message.defeating_player == effect.this.GetOwnerPlayer()

    def piocher_trois(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        proprietaire = effect.this.GetOwnerPlayer()
        if proprietaire is None:
            return
        proprietaire.DrawUp(3, effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenCardEnterPlay(AbilityType.Temp0, "This", hors_limite),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            retirer_une_menace,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.HeroInterrupt,
            "This",
            piocher_trois,
            conditions=[le_proprietaire],
        ),
    ]
