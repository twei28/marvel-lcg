from . import *

# Save The Day — amelioration signature, x1 (n/15 = 14).
# PREPARATION. Cout 1, ressource [energy].
# Hero Interrupt: When a treachery is revealed, discard Save The Day and
#   remove 1 reactor counter from Iron Man -> cancel all of that treachery's
#   effects and discard it.
#
# Cartes de reference :
#  - **`dz013` Velvet Sky** et `09007` Protective Ward :
#    `WhenPlayerRevealCard(HeroInterrupt, "AnyPlayer", Treachery, "All", op)`
#    puis `message.CancelAllEffectsAndDiscardIt(effect)` ;
#  - `08018` Spycraft pour `CostFunc.Discard("This")` ;
#  - `hk005` Interception (pack hulk_rainy) pour le meme texte au cout pres.
#
# ⚠ « cancel ALL of its effects » : niveau d'annulation « All », et PAS le
# `CancelWhenRevealedEffect`, qui ne couvre que le « When Revealed » et
# laisse passer les mots-cles, Surge compris. Leçon dz013, payee en partie
# reelle.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - Le cout a **DEUX parties** : defausser CETTE carte ET retirer 1 compteur.
#    Oublier l'une des deux est le piege `wd005`. Sans compteur, la carte ne
#    peut pas etre jouee — c'est ce que rend le `CostFunc.Custom`, dont le
#    False bloque le paiement.
#  - « When a treachery is revealed » sans « you » : n'importe quel joueur de
#    la table, d'ou `"AnyPlayer"`. Et sans « from the encounter deck » : pas
#    de `from_encounter`.
#  - ⚠ `im012` Hulkbuster Armor porte le MEME numero imprime 14/15 : l'auteur
#    la donne comme « alternative replacement » de celle-ci. Les deux cartes
#    existent dans le jeu, mais c'est CELLE-CI qui est au deck de depart
#    (decision de l'utilisateur, 03/09/2026).


def GetAbilities() -> Sequence['Ability']:

    def cout_du_reacteur(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        if identite is None:
            return False
        return RetirerUnReacteur(identite, effect)

    def save_the_day(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            save_the_day,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_du_reacteur)),
    ]
