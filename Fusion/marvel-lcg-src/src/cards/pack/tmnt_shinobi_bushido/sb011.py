from . import *

# Vow — EVENEMENT THWART, classe Bushido (Inkwire, TMNT Shinobi). Cout 2, [energy]. Pas de citation.
# Hero Action (thwart): Remove threat from a scheme equal to your hero's THW. If this removes the last threat on that scheme,
#   search your deck for an OATH upgrade, and add it to your hand. (Shuffle.)
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md) pour le trait OATH.
#
# Cartes de reference :
#  - « Remove N threat from a scheme. If this removes the last threat from that scheme, <suite> » : `cw/tigra/56009` Feline Senses
#    (`this.RemoveThreatFromSchemes(cibles, n, effect, if_this_remove_last_threat=action)`, `.SetTarget(Scheme2)`,
#    `.SetLabel('thwart')`), ici N = le CTR courant du heros ;
#  - « search your deck for an X, and add it to your hand. (Shuffle.) » : `ares/ares/ar001b` (`Search.PlayerCard(include_player_deck=True,
#    trait=...)` + `joueur.GainCard([face], effect)`) ;
#  - « equal to your THW » : `valk/25018` Quick Strike pour l'ATQ (`GetHero().attack`), ici `GetHero().thwart`.
#
# TEXTE CONTRE CODE
#  ⚠ « equal to YOUR HERO'S THW » : le CTR COURANT du heros (bonus compris, Rectitude +1 CTR), lu a la resolution.
#  ⚠ « If THIS removes the LAST threat ON THAT scheme » : seulement si ce retrait ramene la menace de la cible choisie a 0 ; un
#    retrait partiel ne declenche rien.
#  ⚠ « search YOUR DECK » : le deck seulement (pas la defausse) ; « an OATH UPGRADE » : une amelioration portant le trait OATH ;
#    « add it to your HAND » ; « (Shuffle.) » : comportement par defaut de la recherche ; sans OATH dans le deck, rien ne vient.
#  ⚠ « scheme » : n'importe quel complot (principal ou annexe) : `Scheme2`.


def GetAbilities() -> Sequence['Ability']:

    def vow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()

        def derniere_menace() -> None:
            face = Search.PlayerCard(
                effect, joueur,
                include_player_deck=True,
                trait="OATH",
                card_type=Upgrade,
            )
            if face is not None:
                joueur.GainCard([face], effect)

        this.RemoveThreatFromSchemes(effect.targets, joueur.GetHero().thwart, effect, if_this_remove_last_threat=derniere_menace)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vow,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
