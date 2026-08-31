from . import *

# * Coldwar — sbire nemesis. ALIEN. BOUNTY HUNTER. PV 2 / SCH 1 / ATK 1*.
# Quickstrike. (After this minion engages your hero, it attacks you.)
# [star] While Killer Thrill is in play, Coldwar gets +1 ATK.
# [star] Boost: After this activation, deal this card to yourself as a
#   facedown encounter card.
#
# Cartes de reference :
#  - Quickstrike : lu directement dans `desc` (`Quickstrike: "1"`), AUCUN
#    module — modele 01167 * Vulture. Ne pas coder de capacite fantome.
#  - « While X is in play, +1 ATK » : dt133 * Orka (pack determination),
#    `ThisGainKeyword(check_fn, attack=1, change_on_event=OnEvent.CardInPlay)`.
#    `ThisGainKeywordWhileFaceIsInPlay` ne conviendrait PAS : elle n'expose ni
#    `attack` ni `scheme` (enhance_self.py:138), seulement patrol/health/
#    quickstrike/amplify/crisis/hazard.
#  - [star] Boost : bw021 Imperius Rex! (pack brawn), qui porte le MEME texte
#    mot pour mot et documente le piege ci-dessous.
#
# ⚠ PIEGE DOCUMENTE PAR bw021 : deplacer la carte ici ne sert a rien, le
# moteur range une carte de boost APRES la resolution de son effet et ecrase
# le deplacement. Il faut DETOURNER le rangement a venir en enregistrant un
# `WhenCardWouldDiscard` temporaire qui redirige vers `dealt_encounter_cards`.

def GetAbilities() -> Sequence['Ability']:

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
        AbilityFactory.ThisGainKeyword(
            killer_thrill_en_jeu,
            attack=1,
            change_on_event=OnEvent.CardInPlay(Minion),
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RedirigerVersLeJoueur,
        ),
    ]
