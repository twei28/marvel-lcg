from . import *

# Mastering Superpowers 2B — complot principal, face B. Menace 5[per_hero] (etoile),
# depart 0, escalade +1[per_hero].
# [star] Forced Interrupt: When this scheme would be completed, place 1 mastery
#   counter on Paibok and remove all threat from here instead. Then, discard cards
#   from the encounter deck until a POWER SKRULL card is discarded. Reveal that card.
# When the player phase ends, if all 4 POWER SKRULL cards are attached to Paibok, the
#   players lose the game. (en gras)
#
# Cartes de reference :
#  - **`39002b`** Melee in the Mojo-seum et **`21099b`** The Armies of Thanos : meme
#    fenetre `WhenMainSchemeStageWouldBeCompleted(WhenCompleted)` + `SetBeInstead` +
#    `RemoveThreatFromSchemes([this], "All")` (retrait de TOUTE la menace).
#  - **`21184b`** Defensive Protocols : `WhenPlayerPhaseEnd(...)` (message general de fin
#    de phase JOUEUR, une fois pour tous les joueurs).
#  - `27102b` : `Worlds.SetGameOver(False, effect)` pour la defaite.
#
# ⚠ Mots-pieges : « remove all threat from here INSTEAD » : le complot n'est jamais accompli
# (il boucle) ; ruling FFG n°32 (cf. 39002b) : si la menace ne peut pas etre retiree, l'Interruption
# ne se resout pas ; « Then, discard ... » vient APRES le jeton et le retrait ; « when the PLAYER
# phase ends » (pas la phase du mechant) ; « ALL 4 » attachements POWER SKRULL « attached TO
# PAIBOK » (pas seulement en jeu) ; « if 2B is in play » : la capacite vit sur cette face.


def GetAbilities() -> Sequence['Ability']:

    def completer(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        avant = this.threat
        this.RemoveThreatFromSchemes([this], "All", effect)
        if avant > 0 and this.threat >= avant:
            return
        message.SetBeInstead(effect)
        PoserMaitrise(effect)
        RevelerPouvoirDuDeck(effect, Worlds.GetFirstPlayer(effect))

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        paibok = PaibokEnJeu(effect)
        if paibok is not None and len(PouvoirsAttaches(paibok)) >= 4:
            Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.WhenCompleted, "This", completer),
        AbilityFactory.WhenPlayerPhaseEnd(AbilityType.NonKeywordBold, fin_de_phase),
    ]
