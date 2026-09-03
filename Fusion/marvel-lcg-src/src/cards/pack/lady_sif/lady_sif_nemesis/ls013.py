from . import *

# Captivating Wiles — COMPLOT ANNEXE nemesis (N 1/5). Menace de depart 3 par
# joueur. 1 icone de boost + une icone [star].
# The Enchantress is manipulating us to do her dirty work for her!
# Forced Interrupt: When the player phase begins, exhaust the first player's
#   identity and place 2 threat on the main scheme.
# [star] Boost: Place 2 threat on the main scheme.
#
# Cartes de reference :
#  - `WhenPlayerPhaseBegin(ForcedInterrupt, op)` (turn_phase.py:163) pour la
#    fenetre ; `56001a` * Tigra emploie la variante APRES
#    (`AfterPlayerPhaseBegin`), c'est le meme couple When/After que ls001a et
#    ls009 du set principal ;
#  - `Worlds.GetFirstPlayer(effect)` (worlds.py:599) pour « the FIRST
#    player » ;
#  - `50134` / `ho015` pour `PlaceThreatOnSchemes("MainScheme", 2, effect)` ;
#  - `an013` / `16140` / `ho017` pour `WhenCardBecomeBoost("This", op)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the FIRST player's identity », pas « each player » ni « the engaged
#    player ». En solo c'est le meme joueur, mais le code ne doit pas
#    l'ecrire en dur : `Worlds.GetFirstPlayer`, pas `effect.GetInitiator()`.
#  - « **When** the player phase begins » : une INTERRUPTION, donc l'identite
#    est inclinee AVANT que le joueur ne commence a jouer. C'est tout le sel
#    de la carte : il perd son action de base du tour.
#  - `Forced` : aucun choix, la capacite part toute seule tant que le complot
#    est en jeu. Elle se repete DONC A CHAQUE ROUND, ce qui en fait la
#    priorite de contre absolue.
#  - « 3 [per_hero] » de menace de depart : base automatique
#    (`desc.StartingThreat = "3*"`), aucun script.
#  - Le `[star] Boost` est un effet de boost, PAS une capacite permanente
#    (fiche mots-cles/boost.md) : il ne tire que si la carte sort comme carte
#    de boost pendant une activation, et il pose 2 menaces de plus.
#  - La phrase en italique est du texte d'ambiance, sans effet.


def GetAbilities() -> Sequence['Ability']:

    def captivating_wiles(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        premier = Worlds.GetFirstPlayer(effect)
        if premier is not None:
            identite = premier.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)

        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(message)

        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenPlayerPhaseBegin(
            AbilityType.ForcedInterrupt,
            captivating_wiles,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
