from . import *

# Spider Armor — FACE [[OPERATIONAL]] de l'amelioration PERMANENTE a deux
# faces. ARMOR. Classe Hero, pas de cout : elle arrive par le Setup de as001b.
# Permanent.
# Forced Response: After you flip to this side, place 3 metal counters here.
# Forced Response: After the last metal counter is removed from here, flip
#   this card.
#
# Cartes de reference :
#  - **`34002a`** Phoenix Force (face RESTRAINED) : « Forced Response: After
#    the last power counter is removed from here, flip this card. » C'est la
#    MEME phrase, au nom du compteur pres :
#    `AfterCardRemovedCounter(ForcedResponse, "This", 'power', op,
#    is_last_counter=True)` puis `this.card.Flip(effect)`.
#  - **`45075b`** Pursued by the Past : `AfterFlipToThisFace(ForcedResponse,
#    op)`, le declencheur « After you flip to this side ».
#  - `34001b` * Jean Grey pour `Faces.PlaceCountersOn(..., 'metal', effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After **the last** metal counter is removed » : PAS « after a metal
#    counter is removed ». Le drapeau `is_last_counter=True` est ce qui fait
#    la difference, et sans lui l'armure se retournerait des le premier
#    compteur depense.
#  - « After you flip **to this side** » : le retour sur OPERATIONAL, pas le
#    depart. La face DESTROYED (as002b) n'a AUCUN declencheur de retournement,
#    c'est bien celle-ci qui se recharge.
#  - « place 3 metal counters **here** » : sur l'amelioration, pas sur
#    l'identite. C'est `"This"`.
#  - « Permanent. » : base automatique lue dans `desc.Permanent`, AUCUN
#    script (fiche mots-cles/permanent.md). Ne rien coder pour ca.
#  - ⚠ Le Setup de as001b pose les 3 premiers compteurs LUI-MEME : la carte
#    n'est pas « retournee » a la mise en place, donc le Forced Response
#    ci-dessous ne se declenche pas ce tour-la. Les deux chemins existent, et
#    ne font pas double emploi.


def GetAbilities() -> Sequence['Ability']:

    def recharge(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.PlaceCountersOn([this], MAX_METAL, 'metal', effect)

    def destruction(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.card.Flip(effect)

    return [
        AbilityFactory.AfterFlipToThisFace(
            AbilityType.ForcedResponse,
            recharge,
        ),
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.ForcedResponse,
            "This",
            'metal',
            destruction,
            is_last_counter=True,
        ),
    ]
