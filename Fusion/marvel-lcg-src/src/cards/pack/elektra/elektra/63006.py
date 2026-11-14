from . import *

# Acrobatic Prowess — EVENEMENT, cout 1, [energy]. ACROBATIC. SKILL. x2 (Elektra 2-3/15).
# Hero Action: Ready Elektra and give her 1 facedown boost card.
#
# CARTES DE REFERENCE
#  - « Ready <hero> » : `Faces.ReadyAll([identite], effect)` (35006 I Got Better).
#  - « give her 1 facedown boost card » : `Faces.GiveFacedownBoostCards` (voir 63011 White Tiger).
#  - Hero Action sans cible : `WhenInYourPlayTurn(HeroAction, op).SetPlay()` (modele : 01012, sans `SetTarget`).
#
# TEXTE CONTRE CODE
#  ⚠ « Ready Elektra » PUIS « give her 1 facedown boost card » : dans cet ordre ; Elektra = l'IDENTITE du joueur en forme heros.
#  ⚠ « 1 facedown boost card » : prise sur le dessus du paquet de rencontre. Paquet de rencontre vide : rien a donner.
#  ⚠ Aucun label `attack`/`thwart` : c'est une COMPETENCE (SKILL), pas une attaque.
#  Chiffres : cout 1, 1 carte boost.


def GetAbilities() -> Sequence['Ability']:

    def acrobatic_prowess(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        Faces.ReadyAll([identite], effect)
        Faces.GiveFacedownBoostCards([identite], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            acrobatic_prowess,
        ).SetPlay(),
    ]
