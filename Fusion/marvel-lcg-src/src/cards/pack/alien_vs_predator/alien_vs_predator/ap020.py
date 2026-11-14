from . import *

# Xenomorph Warrior — SBIRE. XENOMORPH. SCH 1, ATK 2, PV 6. Boost 1.
# Quickstrike.
# When Defeated: Discard the top card of the encounter deck and deal 1 damage to a [[YAUTJA]] enemy for each icon ([star] and [boost]) in
#   that card's boost area.
#
# Cartes de reference : Quickstrike natif (`desc`) ; « each icon (★ and Y) in that card's boost area » : pd008 (`IconesDeBoost`) ;
#   `Worlds.DiscardEncounterTopCard` ; « deal damage to an enemy » : `DealDamage` au choix du joueur (`AskChooseFace`).
#
# ⚠ Mots-pieges : « A [[YAUTJA]] enemy » : UN seul (mechant ou sbire YAUTJA), au choix du joueur qui l'a vaincu ; aucun en jeu ou 0 icone
#   -> la carte est quand meme defaussee.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = JoueurQuiVainc(message, effect, this)
        carte = Worlds.DiscardEncounterTopCard(effect)
        n = IconesDeBoost(carte)
        cibles = EnnemisParTrait(effect, "YAUTJA")
        if n <= 0 or not cibles:
            return
        cible = joueur.AskChooseFace(cibles, effect, prompt="Deal damage to a YAUTJA enemy") or cibles[0]
        this.DealDamage([cible], n, effect)

    return [
        # NoOutOfPlayLimit : Expanding Hive (Interruption forcee) a peut-etre deja donne la carte en boost ; son « When Defeated » se
        # resout quand meme (arbitrage du 25/10/2026).
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu).NoOutOfPlayLimit(),
    ]
