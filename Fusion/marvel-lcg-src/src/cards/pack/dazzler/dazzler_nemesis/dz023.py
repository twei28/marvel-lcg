from . import *

# Taunting Light
# TREACHERY.
# When Revealed: If you are Dazzler, the villain attacks you. If no attack was
#   made this way, give the villain a facedown boost card and shuffle this card
#   into the encounter deck.
#
# « If you are Dazzler » : la carte vient du set nemesis de Dazzler, mais elle
# peut etre revelee par un AUTRE joueur en multijoueur — d'ou la verification
# explicite du nom de l'identite. C'est la clause qui decide de tout : sans
# elle, pas d'attaque, et donc la carte repart dans le deck rencontre.


def GetAbilities() -> Sequence['Ability']:

    def lumiere_narquoise(effect: 'Effect',
                          message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        identite = joueur.GetIdentity()
        attaque_faite = False

        if vilain is not None and identite is not None \
                and identite.IsName(NOM_HEROS):
            vilain.DoAttackYou(joueur, effect)
            attaque_faite = True

        if not attaque_faite:
            if vilain is not None:
                vilain.GiveFacedownBoostCardsInternal(1, effect, None)
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, lumiere_narquoise),
    ]
