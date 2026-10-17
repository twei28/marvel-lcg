from . import *

# Hitodama — EVENEMENT DUAL Ninjutsu/Taijutsu, cout 2, [mental]. ATTACK.
# Classe : « Ninjutsu;Taijutsu ».
# Hero Response (attack): Deal 3 damage to an enemy. If you paid for this card with a THWART event, cloak your hero.
#
# ⚠ QUESTION Q-D2 RESOLUE le 17/10/2026 (.planning/tmnt/shinobi-reponses.md) : Hero Action (attack) confirmee. Rappel : : une « Hero Response » SANS declencheur (« After... »)
# n'a aucune fenetre ou partir. Meme situation que `beast/bt005` Fighting With Friends (« Hero Response: Ready your hero »),
# tranchee par l'utilisateur en Hero Action. LECTURE RETENUE (reponse de l'utilisateur) : comme une Hero Action (attack). Le texte affiche garde le « Hero Response »
# imprime (comme sj020).
#
# Mots-cles (fiches lues AVANT le code) : Cloak (cloak.md, cloaked.md) ; Shinobi (shinobi.md).
#
# Cartes de reference :
#  - Hero Action (attack) a 1 cible, degats puis effet conditionne par le paiement : `jennika/tj004` Decisive Strike (helper
#    partage `PayeAvecUnEvenement(effect, "THWART")` extrait de ce modele) ;
#  - Hero Response sans declencheur lue comme Hero Action : `beast/bt005` ;
#  - « cloak your hero » : `ShinobiCloak(effect, joueur.GetHero())`.
#
# TEXTE CONTRE CODE
#  ⚠ « paid for this card with A THWART EVENT » : un AUTRE evenement portant le trait THWART, defausse pour sa ressource ; un
#    evenement ATTACK ou un allie ne compte pas.
#  ⚠ « Deal 3 damage to AN enemy » PUIS « cloak YOUR HERO » : le HEROS (jamais l'alter-ego ni un allie), seulement si la
#    condition de paiement est vraie.


def GetAbilities() -> Sequence['Ability']:

    def hitodama(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect)
        if PayeAvecUnEvenement(effect, "THWART"):
            joueur = effect.GetInitiator()
            if joueur is not None and joueur.IsHero():
                ShinobiCloak(effect, joueur.GetHero())

    return [
        # Q-D2 (provisoire) : « Hero Response » sans declencheur codee en Hero Action (precedent bt005).
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hitodama,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
