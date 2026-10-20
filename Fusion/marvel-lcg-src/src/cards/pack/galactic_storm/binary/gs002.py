from . import *

# Cosmic Influx — EVENEMENT, cout 1, [physical]. SUPERPOWER. x2 (Binary 1/15, 2/15).
# Max 1 per round.
# Hero Action: Draw 3 cards. Take 1 damage for each non-[energy] resource drawn
#   this way.
#
# Cartes de reference :
#  - **`cap/03015`** Avengers Assemble! : « Max 1 per round » sur un evenement =
#    `.MaxOnePerRound()` sur la capacite de jeu.
#  - pioche + effet sur les cartes piochees : `player.DrawUp(n, effect)` rend la
#    liste des cartes piochees (`player_action.py:1191`).
#  - « take N damage » : `identite.TakeDamage(this, n, effect)` (`jubilee/47031`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « for EACH non-[energy] RESOURCE drawn » : on compte des ICONES (Strength =
#    2 degats), sur les seules cartes piochees PAR CETTE CARTE.
#  - L'icone est lue une fois la carte EN MAIN : Energy Conversion (gs010) la
#    traite alors comme [energy] et elle ne blesse pas (FAQ du livret 1.2 p.22,
#    citee mot pour mot dans le gabarit).
#  - une carte sans ressource ne blesse pas ; une icone [wild] est « non-energy »
#    (question Q3, meme lecture que l'ATQ X).
#  - « TAKE damage » : l'identite du joueur, pas « deal ».
#  - « Max 1 per ROUND » : temoin d'epuisement (deux copies en main, la 2e
#    refusee dans le meme round).


def GetAbilities() -> Sequence['Ability']:

    def influx(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        piochees = joueur.DrawUp(3, effect) or []
        degats = sum(NonEnergieDeLaCarte(f) for f in piochees)
        if degats > 0:
            joueur.GetIdentity().TakeDamage(this, degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            influx,
        ).SetPlay()
        .MaxOnePerRound(),
    ]
