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

        def aucune_attaque() -> None:
            if vilain is not None:
                vilain.GiveFacedownBoostCardsInternal(1, effect, None)
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

        # « If no attack was made THIS WAY » : un vilain etourdi defausse son
        # Stunned AU LIEU d'attaquer, et cela compte comme « pas d'attaque ».
        # Le moteur le dit par `if_no_attack_was_made` (modele 27029, 22031).
        # Jusqu'au 20/10/2026 le module tenait l'attaque pour faite des qu'il
        # l'avait lancee (backlog 12, cas « vilain etourdi »).
        if vilain is not None and identite is not None \
                and identite.IsName(NOM_HEROS):
            vilain.DoAttackYou(joueur, effect,
                               if_no_attack_was_made=aucune_attaque)
        else:
            aucune_attaque()

    return [
        AbilityFactory.WhenThisRevealed(None, lumiere_narquoise),
    ]
