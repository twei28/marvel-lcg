from . import *

# * Karai — SBIRE UNIQUE (set Chunin). FOOT CLAN. NINJA. MNG 1 / ATQ 1 / PV 2.
# When Revealed: Cloak Karai.
# When Defeated: Cloak the villain.
# [star] Boost: Deal this card to the first player as a facedown encounter card.
#
# Cartes de reference : `tl015` * Karai (nemesis de Leonardo) : MEME texte, MEME
# montage (`WhenThisRevealed`, `WhenUnitBeDefeated(WhenDefeated, "This")`,
# detournement du rangement du boost). ⚠ Ce n'est PAS la meme carte : `ts101`
# vit dans le set Chunin ; les deux ne coexistent pas (carte unique, meme titre).
#
# Mots-pieges : « Cloak KARAI » (elle-meme) vs « Cloak THE VILLAIN » (When
# Defeated) ; « to the FIRST player » (pas celui qui revele).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, effect.this)

    def vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Cloak(effect, Worlds.FindVillain(effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        FaceCacheeAuPremierJoueur(effect, effect.this)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
