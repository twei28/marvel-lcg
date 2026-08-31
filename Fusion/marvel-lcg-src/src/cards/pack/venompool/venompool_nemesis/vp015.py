from . import *

# * Guzz — sbire nemesis. ALIEN. BOUNTY HUNTER. PV 2 / SCH 1* / ATK 1.
# Plotting. (After this minion engages you, it schemes.)
# [star] While Killer Thrill is in play, Guzz gets +1 SCH.
# [star] Boost: After this activation, deal this card to yourself as a
#   facedown encounter card.
#
# Cartes de reference :
#  - Plotting : voir docs/reference/mots-cles/plotting.md et ss019 * Bella
#    Donna (pack scarlet_spider), premiere carte a nommer le mot-cle.
#    `AfterMinionEngagePlayer` + `this.CastTo(Minion).BasicSchemes(effect)`.
#    Le texte de rappel de Guzz dit « engages YOU » la ou ss019 dit « engages
#    your identity » : meme mecanisme, la fiche le note.
#  - Le reste est le jumeau de vp014 Coldwar (SCH au lieu d'ATK).

def GetAbilities() -> Sequence['Ability']:

    def plotting(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        this.BasicSchemes(effect)

    def killer_thrill_en_jeu(effect: 'Effect', ui: List['CardFace']) -> int:
        face = Worlds.FindCardOnField(
            effect,
            card_type=Minion,
            name=KILLER_THRILL_NAME,
        )
        if face:
            ui.append(face)
            return 1
        return 0

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            plotting,
        ),
        AbilityFactory.ThisGainKeyword(
            killer_thrill_en_jeu,
            scheme=1,
            change_on_event=OnEvent.CardInPlay(Minion),
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RedirigerVersLeJoueur,
        ),
    ]
