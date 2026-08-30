from . import *

# * Spider Stealth Suit — ARMOR. TECH.
# You get +1 hit point.
# Hero Interrupt: When you play an [[ATTACK]] or [[THWART]] event, increase
#   the damage dealt or the threat removed by that event by 1.
#
# Carte sans texte "Attach to..." imprime (portee directement par le
# joueur, comme la TITLE ok016 Royal Protector) : `AbilityFactory.
# GiveKeywordToInPlayWhenApplyThis("You", health=1)` pour le "+1 hit point"
# fixe (meme kwarg `health` que ag009/il015 pour un attache, applique ici
# au porteur lui-meme).
#
# Cote degats : `AbilityFactory.WhenDamageWouldBeDealtTo(HeroInterrupt, None,
# ..., by_play_card=("YouControl", CardFinder(trait="ATTACK", card_type=
# Event)))` + `message.IncreaseDamage(1, effect)` (game/ability/factory/
# damage.py, meme mecanisme qu'utilise en interne `if_this_attack_deal_
# excess_damage` de DealDamage). `by_play_card` verifie que la source du
# degat EST la carte jouee (`message.by_effect.this`), pas necessairement
# l'identite -- c'est le cas ici puisqu'un Event appelle `this.DealDamage`
# sur lui-meme.
#
# Cote menace retiree : aucune methode "IncreaseValue" n'existe sur
# `Message.WhenSchemeWouldRemoveThreat` (contrairement a `WhenSchemeBeing
# Scheme.UpdateValue`, qui existe pour la base de complot), MAIS
# `Scheme2.RemoveThreatInternal` (game/card/face/base/scheme.py:140-143)
# RELIT `remove_message.value` juste apres `.Send()` pour calculer le
# montant reellement retire -- la mutation directe du champ (`message.value
# += 1`) a donc un effet reel, meme si le typage `Final` ne le documente
# pas (Python ne l'impose pas a l'execution). Filtre par
# `who_make_thwart=("YouControl", CardFinder(trait="THWART", card_type=
# Event))` (meme idiome `("YouControl", CardFinder(...))` que ok016).


def GetAbilities() -> Sequence['Ability']:

    def increase_damage(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.IncreaseDamage(1, effect)

    def increase_threat_removed(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.value += 1

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            health=1,
        ),
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.HeroInterrupt,
            None,
            increase_damage,
            by_play_card=("YouControl", CardFinder(trait="ATTACK", card_type=Event)),
        ),
        AbilityFactory.WhenSchemeWouldRemoveThreat(
            AbilityType.HeroInterrupt,
            None,
            increase_threat_removed,
            who_make_thwart=("YouControl", CardFinder(trait="THWART", card_type=Event)),
        ),
    ]
