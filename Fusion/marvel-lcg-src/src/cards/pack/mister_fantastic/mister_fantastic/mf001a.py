from . import *

# * Mister Fantastic — custom « DesignHacker »
# Flexibility — Response: After you spend a SUPERPOWER card as a resource or
# discard it from your hand without being played, return it to your hand.
# (Limit once per phase.)
#
# Dépenser une carte comme ressource et la défausser de la main aboutissent au
# même message moteur (mise à la défausse) : le déclencheur couvre les deux cas
# d'un coup, et les deux sont mesurés verts.
#
# CORRECTIF (31/08/2026) : il ne distinguait PAS la défausse d'une carte
# SUPERPOWER qui était EN JEU, et la rendait alors à la main. Mesuré : Cosmic
# Flight (01017), amélioration SUPERPOWER détruite en jeu, revenait en main.
# Le texte dit « discard it FROM YOUR HAND », donc jamais depuis le jeu. Le
# deck de DÉPART n'expose pas le défaut (il ne porte que des événements
# SUPERPOWER, qui ne séjournent pas en jeu), mais le catalogue compte 102
# améliorations SUPERPOWER et le deckbuilder permet d'en mettre : c'était une
# récupération gratuite de toute amélioration SUPERPOWER détruite.

def GetAbilities() -> Sequence['Ability']:

    def flexibility(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        initiator = effect.GetInitiator()
        face = message.trigger
        if face is None:
            return
        initiator.GainCard(face, effect)

    def pas_depuis_le_jeu(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        # « discard it FROM YOUR HAND » : la carte ne doit pas venir du terrain.
        # `from_where` du moteur ne propose que des filtres POSITIFS
        # ("PlayerArea", "PlayerDeckTop"...), pas leur negation : d'ou la
        # condition explicite sur le drapeau de zone (`deck/deck_type.py`).
        return not message.from_area.flags.is_in_play

    return [
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(trait="SUPERPOWER"),
            flexibility,
            control_by_player="You",
            conditions=[pas_depuis_le_jeu],
        ).SetName("Flexibility")
        .LimitOncePerPhase(),
    ]
