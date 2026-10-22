from . import *

# Invasive Thoughts — TRAITRISE. Boost ★.
# When Revealed : Place 1 corruption counter on your Creeping Corruption. If it has the OVERPOWERING trait, place 1 threat on the main scheme; otherwise, take 1 damage.
# [star] Boost : Choose: Either place 1 corruption counter on your Creeping Corruption, or take 4 indirect damage.
#
# Cartes de reference : trors/absorbing_man/04085 Stall Tactics (`PlaceThreatOnSchemes("MainScheme", ...)`, `TakeIndirectDamage` en boost), shadows_in_the_night/sl010 (`DealDamage([identite], n)`),
#  aoa/clan_akkaba/45162 (boost a deux branches), psylocke_nemesis/41029 (boost « take N indirect damage »).
# ⚠ Mots-pieges : « If IT has the trait » = test APRES la pose du compteur (la pose peut retourner la carte a 5 et faire apparaitre OVERPOWERING) ; « take 1 damage » = 1 degat DIRECT a l'identite ;
#  « 4 INDIRECT damage » = 4 degats indirects, repartis par le joueur ; sans Creeping Corruption : pas de compteur, « it » n'existe pas, donc « otherwise » (1 degat, DECISIONS-d.md n°9).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        PoserCorruption(effect, joueur, 1)
        if CorruptionOverpowering(joueur):
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)
        else:
            this.DealDamage([joueur.GetIdentity()], 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            BrancheCorruption(effect, joueur, 1),
            AbilityFactory.ForChoiceAbility("Take 4 indirect damage", lambda cibles: joueur.GetIdentity().TakeIndirectDamage(this, 4, effect)),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
