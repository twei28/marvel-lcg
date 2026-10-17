from . import *

# * Hidden Passage — SOUTIEN unique 1 [mental], Ninjutsu (TMNT Shinobi, Inkwire). LOCATION. NYC. SEWERS.
# Alter-Ego Action: Exhaust Hidden Passage and discard a cloaked status card from your identity -> draw 1 card.
# Hero Response: After you change form, exhaust Hidden Passage -> cloak your identity.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md).
#
# Cartes de reference :
#  - `ub058` Upstate Farmhouse : « Alter-Ego Action: Exhaust X ... » = `WhenInYourPlayTurn(AbilityType.AlterEgoAction, ..)`
#    + `CostFunc.Exhaust("This")` ;
#  - `ub042` Ready to Rumble : « Hero Response: After you change ... form » = `AfterUnitChangeForm(HeroResponse, "You", fn)` ;
#  - `CoutDefausserCloaked("identity")` : cout « discard a cloaked status card from your identity » (modele `sk049`).
#
# TEXTE CONTRE CODE
#  ⚠ « from your IDENTITY » (et non « your hero ») : l'identite, quelle que soit sa forme ; l'Action ne se joue qu'en forme
#    ALTER-EGO ; sans Cloaked sur l'identite, elle n'est pas proposee.
#  ⚠ « Exhaust Hidden Passage AND discard a cloaked status card » : DEUX couts, tous deux obligatoires.
#  ⚠ « Hero Response: After you change form » : Reponse de HEROS (forme heros seulement) ; apres un changement de forme
#    le joueur est en forme heros : donc apres un passage alter-ego -> heros (lecture litterale : un Hero Response ne
#    part pas apres un passage heros -> alter-ego, le joueur n'etant plus en forme heros). « cloak your IDENTITY » :
#    l'identite (la carte qui vient d'arriver en forme heros).
#  ⚠ Unique (✦).


def GetAbilities() -> Sequence['Ability']:

    def passage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    def se_cacher(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        ShinobiCloak(effect, joueur.GetIdentity())

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            passage,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CoutDefausserCloaked("identity")),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            se_cacher,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
