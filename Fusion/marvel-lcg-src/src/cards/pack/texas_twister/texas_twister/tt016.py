from . import *

# Lone Star Rangers — EVENEMENT BASIC, cout 1, [wild].
# Hero Action: After a [[RANGER]] character is defeated, ready each [[RANGER]]
#   character you control.
#
# CARTE DE REFERENCE
#  - `bk014` Proper Funeral : `AfterUnitBeDefeated` sur un evenement joue en
#    reaction, `.SetPlay()`.
#
# ⚠ ECART ASSUME SUR LE TYPE DE CAPACITE. La carte imprime « Hero ACTION »
# suivi d'un declencheur « After ... ». Les deux sont incompatibles : une
# Action se joue quand on veut pendant son tour, une capacite « After » est
# une REPONSE. Le moteur tranche par la fabrique employee — ici
# `AfterUnitBeDefeated` — et le sous-type retenu est donc `HeroResponse`.
# Ecrire `HeroAction` rendrait la carte jouable a n'importe quel moment, sans
# jamais verifier qu'un RANGER est tombe. Question posee a l'auteur.
#
# TEXTE CONTRE CODE
#  « each RANGER CHARACTER you control » -> ⚠ CHARACTER, pas ALLY : l'identite
#    heros de Texas Twister porte elle-meme le trait RANGER et se redresse
#    donc avec les autres. C'est tout l'interet de la carte dans ce pack, et
#    le helper `RangersDuJoueur` le dit noir sur blanc.
#  « After a RANGER character IS DEFEATED » -> n'importe lequel, y compris
#    celui d'un autre joueur, y compris un SBIRE qui porterait le trait. Aucun
#    filtre de controle sur le declencheur ; le controle ne porte que sur les
#    cartes REDRESSEES.


def GetAbilities() -> Sequence['Ability']:

    def rangers(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        rangers_en_jeu = RangersDuJoueur(effect)
        if rangers_en_jeu:
            Faces.ReadyAll(rangers_en_jeu, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.HeroResponse,
            CardFinder(card_type=Unit2, trait=TRAIT_RANGER),
            rangers,
        ).SetPlay(),
    ]
