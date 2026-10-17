from . import *

# * Shinobi Batman « Bruce Wayne » — ALLIE 3 [mental], 2**/2*, 3 PV, aspect Basic (TMNT Aspects). NINJA. VIGILANTE.
# Play only if you control a [[NINJA]] or [[VIGILANTE]] card.
# Response: After Shinobi Batman leaves play, search your deck for a [[NINJA]] or [[VIGILANTE]] card and add it
#   to your hand. (Shuffle.)
#
# NOUVELLE. Cartes de reference : 27048 Ghost-Spider (« Play only if you control a WEB-WARRIOR card » +
# fouille du deck quand il quitte le jeu ; mais SON texte est une INTERRUPTION « When ... leaves play ») ;
# ici « Response: AFTER ... leaves play » -> la famille « after leaves play » (`AfterCardLeavePlay`).
# Fouille : 18002 Nebula (`Search.PlayerCard(include_player_deck=True, traits=[A, B])`, OU).
# TEXTE CONTRE CODE : « a NINJA or VIGILANTE CARD » (tout type) ; « your DECK » (pas la defausse) ;
#   « AFTER leaves play » (Reponse, apres la sortie).


def GetAbilities() -> Sequence['Ability']:

    def shinobi_batman(effect: 'Effect', message: 'Message2') -> None:
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            traits=["NINJA", "VIGILANTE"],
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        JouableSiVousControlez(AbilityFactory.CanPlayThisAllyCard().SetPlay(), ["NINJA", "VIGILANTE"]),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            shinobi_batman
        ),
    ]
