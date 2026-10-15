from . import *

# * Jazinda — ALLIEE de campagne (Justice / Campaign, n° 264). Cout 3. THW 3** / ATK 1*, 4 PV. SKRULL.
# Jazinda does not count against your ally limit.
# While Jazinda is exhausted, your hero gets +1 THW.
#
# Cartes de reference :
#  - **`55063`** Absorbing Man (ally) : « Does not count against your ally limit » =
#    `AbilityFactory.ThisNotCountAllyLimit()`.
#  - **`an002`** Sera (et RECETTES §3, contraste avec `06007` Asgard) : « your HERO gets +N » =
#    `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", ...)` (le MOT : « your HERO », pas « you » :
#    forme heros seulement ; `Identity` serait pour « you »).
#  - **`29004`** Brawn (ally) : « While Brawn is exhausted » = condition `effect.this.IsExhaust()`.
#
# ⚠ Mots-pieges : « YOUR hero » = le heros du CONTROLEUR de Jazinda (pas celui d'un autre joueur) et
# seulement en forme heros (l'alter ego n'a pas de CTR) ; « WHILE exhausted » : le bonus doit etre
# recalcule quand Jazinda s'incline ET quand elle se redresse (`OnEvent.TemplateTrigger` sur
# AfterCardExhausted / AfterCardReady) ; « does not count against your ALLY limit » : elle ne bloque pas un
# 4e allie.


def GetAbilities() -> Sequence['Ability']:

    def inclinee(effect: 'Effect') -> bool:
        return effect.this.IsExhaust()

    def cette_carte(effect: 'Effect', message: 'Message2') -> bool:
        return message.trigger == effect.this

    changement_d_etat = OnEvent.TemplateTrigger(
        Message.AfterCardExhausted | Message.AfterCardReady,
        cette_carte,
    )

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            thwart=1,
            condition=inclinee,
            change_on_event=changement_d_etat,
        ),
    ]
