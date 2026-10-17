from . import *

# * Kōshō — AMELIORATION unique ✦ OATH. TITLE. TRAINING., classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [physical].
# Uses (2 samurai counters). Attach to an ally you control.
# Max 1 TRAINING upgrade per ally.
# Hero Action: Exhaust this card and remove 2 samurai counters from it -> heal 2 damage from attached ally and ready it.
#
# Mots-cles (fiches lues AVANT le code) : Uses (uses.md, NATIF) ; samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « Attach to an ally » + « Max 1 TRAINING upgrade per ally » : `mut_gen/32013` Protective Training,
#    `tmnt_aspect_protection/up027` Protection Training (`CanPlayThisUpgradeCard(...)` ; le plafond « Max 1 TRAINING per ally »
#    est porte par le moteur, `ability.py` `filter_training_upgrade_per_ally`, lu sur le trait TRAINING de la carte) ;
#  - « you control » : le selecteur de l'attache est restreint aux allies du joueur (`GetControlAllies`) ;
#  - action d'amelioration attachee a un allie dont le cout DEFAUSSE la carte : `patriot/pt016` (la cible porteuse est lue AVANT
#    le paiement) ; ici `SetTarget("Attached")` (le porteur est choisi AVANT les couts, donc reste cible apres que Uses a defausse
#    Kosho) ; `Faces.ReadyAll` / `HealHealth`.
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to AN ALLY YOU CONTROL » : un allie SOUS SON CONTROLE (pas l'identite, pas l'allie d'un autre joueur).
#  ⚠ « Max 1 TRAINING upgrade per ally » : un allie ne porte qu'UNE amelioration TRAINING (moteur, trait de la carte).
#  ⚠ « Exhaust this card AND remove 2 samurai counters FROM IT » : deux couts ; les 2 compteurs sont TOUS les compteurs (Uses 2) :
#    l'usage defausse Kosho, une fois ; l'effet se resout quand meme sur l'allie porteur.
#  ⚠ « heal 2 damage FROM ATTACHED ALLY AND ready IT » : l'allie porteur, les DEUX effets ; Hero Action : forme heros seule.
#  ⚠ Unique ✦ : une seule Kosho en jeu (le nom porte « * »).


def GetAbilities() -> Sequence['Ability']:

    def allies_sous_controle(effect: 'Effect') -> 'Sequence[CardFace]':
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return list(joueur.GetControlAllies())

    def kosho(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        for ami in effect.targets:
            ami.CastTo(Ally).HealHealth(2, effect)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Select.From(allies_sous_controle)),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kosho,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 2, 'samurai'))
        .SetTarget("Attached"),
    ]
