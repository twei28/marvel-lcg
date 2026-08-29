from . import *

# * Okoye (face heros)
# The Art of War — Response: After you make a basic attack or basic thwart,
#   Dora Milaje allies you control take 1 less consequential damage when
#   performing the same basic power until the end of the phase. (Limit once
#   per round.)
#
# Declencheur : AbilityFactory.AfterUnitUseBasicPower(..., "You", powers=
# ["ATK","THW"]), qui donne message.power ("ATK"/"THW", sender_unit.py:11).
# La reduction elle-meme n'est PAS `GainUntilPhaseEnd` (ce wrapper n'expose
# pas attack_consequential_damage/thwart_consequential_damage) mais
# `TemporaryGain` directement -- le meme appel que `GainUntilPhaseEnd` fait en
# interne (face_action.py:451), avec le bon champ selon `message.power`.
# Modele du couple attack_consequential_damage/thwart_consequential_damage :
# hercules/59018.py (`GainForThisActive(..., attack_consequential_damage=-1)`),
# ici etendu a TOUS les allies Dora Milaje plutot qu'a la seule carte, et
# jusqu'a la fin de la phase plutot que pour une seule attaque active.


def GetAbilities() -> Sequence['Ability']:

    def the_art_of_war(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        allies = Worlds.FindCardsOnField(effect, trait="DORA MILAJE", card_type=Ally)
        if not allies:
            return

        kwargs = {}
        if message.power == "ATK":
            kwargs["attack_consequential_damage"] = -1
        elif message.power == "THW":
            kwargs["thwart_consequential_damage"] = -1
        else:
            return

        for face in allies:
            face.TemporaryGain(effect, None, Message.WhenPhaseEnd, **kwargs)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            the_art_of_war,
            powers=["ATK", "THW"],
        ).SetName("The Art of War")
        .LimitOncePerRound(),
    ]
