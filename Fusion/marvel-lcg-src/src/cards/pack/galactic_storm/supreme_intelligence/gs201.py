from . import *

# Genetic Augmentation — ATTACHEMENT (Supreme Intelligence), x2. CONDITION. +1 ATK, 1 icone de boost.
# Attach to the KREE minion with the most remaining hit points. Otherwise, this card gains surge.
# Attached minion gets +2 hit points and gains the ELITE trait.
#
# Cartes de reference :
#  - **`jubilee/47026`** Battle Suit : `AttachToFaceWhenPutIntoPlay(Minion, fewest_remaining_hp=True,
#    if_cannot_gain_surge=True)` + `GiveKeywordToAttached(Minion, health=3, trait="AERIAL")` : meme phrase
#    au mot pres (ici `most_remaining_hp` et un finder KREE).
#  - **`hercules/59002`** Defeat the Hydra : « gets +6 hit points and gains the ELITE trait ».
#  - +1 ATK : cle `desc` `ATK+` (sk232 Enemy Adaptation), aucun code.
#
# ⚠ Mots-pieges : « the KREE minion » (sbire au trait KREE, pas le mechant) ; « with the MOST REMAINING hit
# points » (PV restants, pas imprimes ; egalite : le joueur choisit) ; « Otherwise, this card gains SURGE »
# (aucun sbire KREE en jeu) ; « gets +2 hit points AND gains the ELITE trait » (les deux) ; +1 ATK imprime en
# icone. Le trait ELITE gagne est NOTE sur le message de defaite du porteur (`gs_elite_a_la_defaite`), lu par
# la Reponse forcee de Supreme Intelligence (I)/(II) : l'attachement quitte le jeu avec le sbire, donc le
# trait gagne aurait disparu au moment de la Reponse.


def GetAbilities() -> Sequence['Ability']:

    def porteur_va_etre_vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        return effect.this.IsInPlay() and message.trigger == effect.this.bind_face

    def noter_elite(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        Unused(effect)
        setattr(message, "gs_elite_a_la_defaite", True)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion, trait="KREE"),
            most_remaining_hp=True,
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            health=2,
            trait="ELITE",
        ),
        Ability(AbilityType.NonKeyword, Message.WhenUnitWouldBeDefeated, [porteur_va_etre_vaincu], noter_elite),
    ]
