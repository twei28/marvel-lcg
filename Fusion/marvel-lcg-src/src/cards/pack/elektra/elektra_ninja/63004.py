from . import *

# Ninja Vanish — TRAITRISE, set « Elektra Ninja » (paquet NINJA d'Elektra, 2 exemplaires, Ninja (5/6)). NINJA. Surge.
# When Revealed: Give this card to Elektra as a facedown boost card.
# ★ Boost: If Elektra is using a basic power, give her a tough status card and shuffle this card into the NINJA deck. Otherwise, give this card to Elektra as a facedown boost card.
#
# CARTES DE REFERENCE
#  - « Deal this card ... as a facedown boost card » (When Revealed) : `leonardo/tl015` (`WhenCardWouldDiscard` + `SetToArea`, a USAGE UNIQUE) ;
#    ici la zone cible est la PILE DE BOOST de l'identite (`CanBoost.GiveBoostCard`).
#  - « ★ Boost » : `AbilityFactory.WhenCardBecomeBoost("This", op)` (`an013`, `16140`) ; pouvoir en cours lu sur `message.would_message`
#    (`PouvoirDeBase`, set Elektra). « Surge » : base automatique (`desc.Surge`).
#  - extension moteur du 13/11/2026 : un HEROS villainous resout sa pile de boost aussi sur DEJOUER et DEFENSE (`CanBoost.HeroBoostForBasicPower`).
#
# TEXTE CONTRE CODE
#  ⚠ « When Revealed : give this card to Elektra » : la carte NE va PAS a la defausse : elle est detournee vers la pile de boost de l'identite du
#    joueur qui la revele (une seule fois).
#  ⚠ « If Elektra is USING A BASIC POWER » : attaque, deploiement ou defense de BASE ; une attaque par evenement (Killer Blow) = « Otherwise ».
#  ⚠ « Otherwise » : la carte retourne dans la pile de boost d'Elektra (face cachee) ; le moteur ne la re-retourne pas dans la meme resolution.
#  ⚠ Killer Instinct (63001a) peut ANNULER ce « Boost » (Interruption d'Elektra) : le code ci-dessous ne s'execute alors pas.
#  Chiffres : une carte Tough, la carte rejoint le paquet Ninja.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        elektra = ElektraDuJoueur(joueur)
        if elektra is None:
            return

        def vers_les_boosts(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            message2.SetToArea(elektra.components.boostable.GetDeck())

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(AbilityType.Temp0, "This", vers_les_boosts),
            unregister_after_exec=True,
            until_round_end=True,
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        unite = message.would_message.trigger
        # « Elektra » = l'identite du joueur : celui qui controle l'unite, ou, si la carte sert de boost a un ENNEMI,
        # le joueur contre qui il agit (« Otherwise, give this card to Elektra »).
        joueur = unite.GetControlByPlayer() if Hero.IsType(unite) else message.GetAgainstPlayer()
        if joueur is None:
            return
        puissance = PouvoirDeBase(message)
        if puissance is None:
            DonnerEnBoostA(this, ElektraDuJoueur(joueur), effect)
            return
        Faces.GiveStatus([unite], "Tough", effect)
        MelangerDansPaquetNinja(this, joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
