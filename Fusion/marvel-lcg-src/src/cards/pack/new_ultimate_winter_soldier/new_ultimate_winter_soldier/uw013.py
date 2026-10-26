from . import *

# Live with the Burden — obligation de Logan. Boost 1.
# Give to the Logan player.
# When Revealed: Discard 1 card from your hand at random. Take X damage, where X is equal to the numeral in the printed
# resource cost of that card. You may exhaust your identity to prevent 2 of that damage. Discard this card.
#
# Cartes de reference : `42024` Apocalyptic Influence (`WhenThisObligationRevealed`, `message.GetGaveToPlayer()`),
# `hc013` Mental Episode (`identite.TakeDamage(this, n, effect)` + `Faces.DiscardAll([this], effect)` : une obligation
# revelee ENTRE EN JEU et y reste, il faut la defausser explicitement, RECETTES-MOTEUR §3).
#
# Mots-pieges : « at random » ; « Take X damage » : des DEGATS a l'identite (pas indirects, pas une attaque) ;
# « You MAY exhaust your identity to prevent 2 of that damage » : facultatif, l'identite doit pouvoir s'incliner
# (deja inclinee : pas d'offre), et on ne previent jamais plus que X ; la carte se defausse dans tous les cas.


def GetAbilities() -> Sequence['Ability']:

    def live_with_the_burden(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        identite = joueur.GetIdentity()
        faces = joueur.DiscardRandomHandCards(1, effect)
        degats = CoutImprime(faces[0]) if faces else 0

        if degats > 0 and identite.CanExhaust():
            etat = {"degats": degats}

            def inciter(cibles: 'Sequence[CardFace]') -> None:
                if Faces.ExhaustAll([identite], effect):
                    etat["degats"] = max(0, etat["degats"] - 2)

            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Exhaust your identity → prevent 2 of that damage",
                    inciter,
                ),
            )
            degats = etat["degats"]

        if degats > 0:
            identite.TakeDamage(this, degats, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisObligationRevealed(
            live_with_the_burden,
        ),
    ]
