from . import *

# * Rōnin (Mikey) — ALLIE double aspect Aggression/Justice (Inkwire, TMNT Aspects).
# Cout 4, PV 2, THW 2 / ATK 2 (1 degat consecutif chacun), ressource [wild].
#
# Response: After Rōnin enters play, cloak him.
# Interrupt: When Rōnin is defeated by consequential damage ([consequential]),
#   spend a [wild] resource -> draw 3 cards.
#
# Cartes de reference :
#  - Cloak : `tl016` Foot Soldiers / fiche mots-cles/cloak.md : « Cloak X » =
#    `Faces.GiveStatus([X], "Cloaked", effect)` ;
#  - « After X enters play » sur l'allie lui-meme : `AfterCardEnterPlay(Response, "This", ...)`
#    (meme fabrique que 01066 Hawkeye, cible differente) ;
#  - « When X is defeated by consequential damage » : `WhenUnitBeDefeated(Interrupt, "This",
#    by_consequential=True)` (30021 SP//dr, filtre `by_consequential`) ;
#  - « spend a [wild] resource -> draw » : `.SetCost(Cost("G"))`, 04097 Moon Knight (« spend a
#    [wild] resource -> draw 2 cards »). `HasColor("G")` ne convertit pas : SEULE une ressource
#    wild paie ce cout.
#
# Mots-pieges : « cloak HIM » = Rōnin lui-meme ; « defeated » (pas « damaged ») ; « by consequential
# damage » (pas une attaque ennemie) ; le cout est une ressource WILD, pas « une ressource ».


def GetAbilities() -> Sequence['Ability']:

    def se_camoufler(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Cloaked", effect)

    def piocher_trois(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        effect.GetInitiator().DrawUp(3, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            se_camoufler,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Interrupt,
            "This",
            piocher_trois,
            by_consequential=True,
        ).SetCost(Cost("G")),
    ]
