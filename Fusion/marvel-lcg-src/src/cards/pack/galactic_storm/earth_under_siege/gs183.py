from . import *

# Induced Mutation — ATTACHEMENT (ensemble Doctor Minerva), x2 exemplaires.
# CONDITION.
# Attach to the villain and give it a tough status card.
# Uses (3 duration counters).
# [star] Forced Interrupt: When the villain activates, give it 1 additional boost card for that
#   activation and remove 1 duration counter from here.
#
# Cartes de reference :
#  - « Attach to the villain and give it a tough status card » : `AttachToFaceWhenPutIntoPlay(Villain,
#    when_attach_operation=...)` + `Faces.GiveStatus([mechant], "Tough", effect)` (modele hala_ultimatum
#    `DonnerTenaceAuVillainOuSinon`, ici sans branche alternative).
#  - « Uses (3 duration counters) » : `desc.Uses = "3,duration"` (natif), compteur 'duration' ajoute a
#    `CardFace.COUNTER`.
#  - « When the villain activates, give it 1 additional boost card... » : PAS de « against you » imprime
#    (contrairement a `AfterEnemyActivatesAgainstYou`, qui EXIGE un joueur cible) :
#    `Message.WhenEnemyActivateAgainstYou` construit directement (`Ability(...)`, `to_player` peut etre
#    None pour une manigance visant le complot principal) + `message.GiveAdditionalBoostCardForThisActivation`
#    (modele sk159/sk100, meme methode).
#
# ⚠ Mots-pieges : « the villain » = This, l'hote (`effect.this.bind_face`, pas effect.this lui-meme qui est
# l'attachement) ; le texte ne restreint PAS a une attaque « against you », toute activation compte
# (y compris une manigance sans joueur vise) ; « remove 1 duration counter » se fait a CHAQUE activation,
# pas seulement la premiere (pas de "Limit" imprime).


def GetAbilities() -> Sequence['Ability']:

    def a_lattache(this: 'CardFace', effect: 'Effect') -> None:
        villain = this.CastTo(Attachment).bind_face
        if villain is not None:
            Faces.GiveStatus([villain], "Tough", effect)

    def sur_lhote(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> bool:
        return message.trigger is getattr(effect.this, 'bind_face', None)

    def boost_supplementaire(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
        this = effect.this.CastTo(Attachment)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        Faces.RemoveCountersOn([this], 1, 'duration', effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain, when_attach_operation=a_lattache),
        Ability(
            AbilityType.ForcedInterrupt,
            Message.WhenEnemyActivateAgainstYou,
            [sur_lhote],
            boost_supplementaire,
        ),
    ]
