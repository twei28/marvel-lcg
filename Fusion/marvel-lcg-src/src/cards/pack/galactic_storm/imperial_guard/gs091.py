from . import *

# Disciplined Training — ENVIRONNEMENT (Imperial Guard). CONDITION. SETTING. Setup.
# Setup.
# Each IMPERIAL GUARD minion gains toughness.
# Special: Deal 1 damage to your identity.
# When Revealed: Discard each other SETTING environment in play.
#
# Cartes de reference :
#  - « Setup » : BASE AUTOMATIQUE `desc.Setup = "1"` (fiche setup.md, modele fne 60113a) : l'environnement entre en jeu a la mise en
#    place ; son « When Revealed » ne joue qu'en cas de revelation tardive.
#
#  - « Each IMPERIAL GUARD minion gains toughness » : `GiveKeywordToInPlayWhenApplyThis(CardFinder(trait=.., card_type=Minion), toughness=1)`,
#    modeles ar011 Athena's Guidance et 40189 Mutant Insurrection (fiche toughness.md : un sbire qui ENTRE en jeu recoit sa carte Tough).
#  - « When Revealed: Discard each other SETTING environment in play » : `Worlds.DiscardEachOther(effect, this, trait=SETTING,
#    card_type=Environment)` (modele du moteur, worlds.py).
#  - « Special » : capacite nommee `WhenResolveSpecialAbility("This", ..)` (fiche special.md, modele ab007 / baxter_stockman tx004b),
#    resolue par les sbires via `ResoudreLeSpecial`.
#
# ⚠ Mots-pieges : « EACH IMPERIAL GUARD minion » (pas les autres sbires) ; « gains toughness » : seuls les sbires qui ENTRENT apres l'environnement la recoivent (l'environnement est en jeu des la mise en place) ; « YOUR identity » = celle du joueur qui resout le Special.


def GetAbilities() -> Sequence['Ability']:

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            effect.this.DealDamage([joueur.GetIdentity()], 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(trait=IG, card_type=Minion), toughness=1),
        AbilityFactory.WhenResolveSpecialAbility("This", special),
        EnvironnementImperialGuard(),
    ]
