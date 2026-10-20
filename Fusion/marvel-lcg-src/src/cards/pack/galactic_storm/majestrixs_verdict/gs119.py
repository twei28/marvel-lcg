from . import *

# Imprisoned on Chandilar — MANIGANCE ANNEXE (Majestrix's Verdict), menace de depart 6. Assault. Permanent.
# Forced Response: After a STARJAMMER ally leaves play, tuck it under here.
# Forced Interrupt: When the last threat is removed from here, the players as a group choose a STARJAMMER ally
#   tucked under here, put that ally into play under any player's control and place 6 threat here.
#
# Cartes de reference :
#  - Assault, Permanent : BASES AUTOMATIQUES (`desc.Assault`, `desc.Permanent`, fiches mots-cles/assault.md et
#    permanent.md), aucun module.
#  - « After an ally leaves play, tuck it under here » : modele OFFICIEL 50081 Abduct Superhumans (« When an ally
#    leaves play, tuck it under here »), ici en REPONSE (`AfterCardLeavePlay`) et face VISIBLE (livret p.4).
#  - « When the last threat is removed from here ... put into play under any player's control » : modele
#    OFFICIEL 50088b Locate Missing Person (`WhenLastThreatRemoveFromThisScheme` + `PutIntoPlay(under_control)`).
#
# ⚠ Mots-pieges : « a STARJAMMER ALLY leaves play » (pas un autre allie) ; un allie RETIRE DE LA PARTIE (2A)
# n'est plus atteignable et ne revient pas ; « place 6 threat here » est fait meme s'il ne reste personne a
# liberer (la prison, Permanente, ne peut pas rester a 0) ; « the players AS A GROUP choose » : premier joueur.


def GetAbilities() -> Sequence['Ability']:

    def recapturer(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        face = message.trigger.card.face
        Glisser(effect.this, [face], effect)

    def recapturable(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        if not EstStarjammer(message.trigger):
            return False
        destination = message.into_area
        if destination is effect.world.area_removed or destination.flags.is_place_card_area:
            return False
        return True

    def liberer(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        Unused(message)
        this = effect.this.CastTo(SchemeSide2)
        glisses = Glisses(this)
        if glisses:
            for allie in ChoisirEnGroupe(effect, glisses, 1):
                MettreEnJeuSousControle(effect, allie)
        this.PlaceThreatOnSchemes([this], 6, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.ForcedResponse,
            CardFinder(trait=STARJAMMER, card_type=Ally),
            recapturer,
            conditions=[recapturable],
        ),
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, liberer),
    ]
