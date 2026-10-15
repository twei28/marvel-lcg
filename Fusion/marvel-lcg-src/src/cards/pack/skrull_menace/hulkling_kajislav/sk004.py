from . import *

# Kree Durability — evenement signature x2 (3/16, 4/16). KREE. SUPERPOWER.
# Cout 2 [physical].
# Hero Response: After you change form, ready Hulkling and give him a tough
#   status card.
#
# Cartes de reference :
#  - **`13033`** Perseverance : « Hero Response: After you change form, give
#    your hero a tough status card. » Meme declencheur, meme statut :
#    `AfterUnitChangeForm(HeroResponse, "You", op).SetPlay()`.
#  - `23004` Upgraded Chassis : meme declencheur, statut Tough.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you change **form** » : TOUT changement de forme, heros <-> civil
#    ET forme d'origine (livret p. 4 ; sk002a/b passent par
#    ChangeAdditionalFrom). Aucun filtre `to_form` / `is_change_additional_form`.
#  - « **Hero** Response » : jouable seulement en forme heros, donc apres un
#    passage civil -> heros, ou apres un changement d'origine en forme heros.
#  - « ready Hulkling **and** give him a tough » : les DEUX, sans condition.
#    Pas de `canbe_tough` sur une cible (Perseverance en a un parce que le
#    statut est tout son effet) : un Hulkling deja Tough se redresse quand meme.
#  - Pas d'etiquette attack/thwart/defense imprimee.


def GetAbilities() -> Sequence['Ability']:

    def durabilite(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        identite = effect.GetInitiator().GetIdentity()
        Faces.ReadyAll([identite], effect)
        Faces.GiveStatus([identite], "Tough", effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            durabilite,
        ).SetPlay().SetLabel(),
    ]
