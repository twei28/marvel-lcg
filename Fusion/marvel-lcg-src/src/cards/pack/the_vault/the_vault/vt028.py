from . import *

# Contingency Measures — MANIGANCE ANNEXE. Menace de depart 2[per_hero]. 3 icones de boost.
# Forced Interrupt: When a villain would be defeated, shuffle it into the villain deck instead.
# While Inspection of the Vault is in play, this card gains a hazard icon.
#
# Cartes de reference :
#  - « When a villain would be defeated, ... instead » : `WhenUnitWouldBeDefeated(ForcedInterrupt, Villain, ...)` +
#    `message.SetBeInstead(effect)` (modele gs162a pour la forme ; `Villains.ShuffleIntoVillainDeck`, brique du 25/10/2026) puis
#    `ApresDepartDUnMechant` (livret p.1).
#  - « While Inspection of the Vault is in play, this card gains a hazard icon » : `ThisGainKeywordWhileFaceIsInPlay(
#    while_face_is_in_play=CardFinder(name=Inspection), hazard=1)` (modele officiel 21182 ; icone verifiee sur le glyphe H).
#
# ⚠ Mots-pieges : « would be DEFEATED ... INSTEAD » : le vilain n'est PAS vaincu (aucun « When Defeated », aucun retrait) et ses
# attachements / cartes d'etat sont defausses ; « any villain », pas seulement le vilain de plus bas ordre ; le melange se fait
# meme pour le DERNIER vilain en jeu (on revele alors le suivant, ou le meme).


def GetAbilities() -> Sequence['Ability']:

    def melanger_a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        mechant = message.trigger.CastTo(Villain)
        message.SetBeInstead(effect)
        Villains.ShuffleIntoVillainDeck(mechant, effect)
        ApresDepartDUnMechant(effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Villain, melanger_a_la_place),
        AbilityFactory.ThisGainKeywordWhileFaceIsInPlay(CardFinder(name=NOM_INSPECTION), hazard=1),
    ]
