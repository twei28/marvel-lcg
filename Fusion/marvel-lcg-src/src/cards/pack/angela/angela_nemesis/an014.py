from . import *

# * Disir — sbire nemesis. ASGARD. UNDEAD. PV 4 / SCH 1 / ATK 2.
# Forced Interrupt: When Disir would be defeated, shuffle them into the
#   encounter deck instead.
# [star] Boost: After this activation ends, shuffle this card back into the
#   encounter deck.
#
# ⚠ CETTE CARTE EST L'AUTRE CONTRE DU PACK : Disir ne MEURT jamais, elle
# retourne dans le deck. Elle ne nourrit donc JAMAIS le moteur d'Angela
# (an001a Frenzy, an004, an007, an009 paient tous sur une DEFAITE de sbire).
# Le joueur peut la frapper autant qu'il veut, il n'en tirera rien.
#
# Cartes de reference : bw021 Imperius Rex! (pack brawn) pour le [star] Boost
# qui detourne le rangement a venir de la carte, et 45160 Scarab pour le
# mot-piege « defeated vs damaged ».
#
# ⚠ « would be defeated ... INSTEAD » : c'est un remplacement, pas un ajout.
# La defaite ne doit PAS avoir lieu, sinon les cartes d'Angela se
# declencheraient quand meme — exactement ce que la carte veut empecher.

def GetAbilities() -> Sequence['Ability']:

    def disir(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)

        message.SetBeInstead(effect)
        Faces.ShuffleAllTo([this], Worlds.GetEncounterDeck(effect), effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        # Meme piege que bw021 : une carte de boost est rangee par le moteur
        # APRES la resolution de son effet, un deplacement immediat serait
        # ecrase. On detourne donc le rangement a venir.
        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            Faces.ShuffleAllTo([this], Worlds.GetEncounterDeck(effet_temp), effet_temp)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                rediriger,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            disir,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
