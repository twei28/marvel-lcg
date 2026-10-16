from . import *

# * Ocho — SBIRE UNIQUE (set Chunin). BRUTE. MOLE. YOUKAI. MNG 2 / ATQ 2* / PV 4,
# 1 icone de boost + etoile. Guard.
# [star] Ocho's attacks gain piercing.
# [star] Boost: Search the encounter deck and discard pile for Karai and reveal
#   her. (Shuffle.)
#
# Cartes de reference : `web_of_deceit wd110` Tiger (`UnitAttackGainKeyword("This",
# piercing=True)`) ; `01095` (Search.EncounterCard + Reveal) ; Guard lu dans `desc`.
#
# Mots-pieges : « Karai » cherchee par card_id (`IDS_KARAI`) ; « reveal HER » : si
# Karai n'est pas trouvee, rien ; le boost ne cherche pas dans l'ensemble des
# cartes du jeu mais dans le deck ET la defausse de rencontre.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            finder=CardFinder(card_ids=IDS_KARAI),
        )
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
