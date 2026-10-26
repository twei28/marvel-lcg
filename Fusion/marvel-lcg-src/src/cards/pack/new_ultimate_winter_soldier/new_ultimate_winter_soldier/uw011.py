from . import *

# Mission Objective — amelioration signature. Cout 2, [mental].
# Hero form only. Attach to a minion.
# Hero Response: After the attached minion is defeated by Winter Soldier, remove 3 threat from a scheme. Winter Soldier may
# take 1 damage to attach this card to another minion.
#
# Cartes de reference :
#  - `01007` Spider-Tracer : « Attach to a minion. ... When attached minion is defeated, remove 3 threat from a scheme »
#    = `CanPlayThisUpgradeCard(Minion)` + `SetTarget(Scheme2)` + `RemoveThreatFromSchemes(effect.targets, 3, effect)` ;
#  - `01007` pour la FENETRE : ⚠ `AfterUnitBeDefeated` est envoye APRES la defausse du sbire ET de ses ameliorations
#    (`unit.py:OnBeDefeated`) : une amelioration attachee n'y entend plus rien (mesure du 25/10/2026, la Response restait
#    muette ; `dt067` Bounty a le meme defaut, jamais teste). On ecoute donc `WhenUnitBeDefeated` (le sbire est encore en
#    jeu, avec ses ameliorations) en `HeroResponse`, ce qui permet aussi de DEPLACER la carte avant qu'elle soit defaussee ;
#  - `pd002` (modele `yd012`) : `AttachTo2(hote, effect)` pour DEPLACER une amelioration.
#
# Mots-pieges : « Hero form only » (`hero_form_only`) ; « defeated BY WINTER SOLDIER » (le tueur est le heros du porteur,
# pas un allie ni un sbire) ; « may take 1 damage → attach » : facultatif, un autre sbire en jeu est requis ; le sbire vaincu
# n'est jamais la cible du deplacement.


def GetAbilities() -> Sequence['Ability']:

    def tue_par_le_heros(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return MortParLeHeros(effect, message)

    def mission_objective(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = this.GetControlByPlayer()
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
        DeplacerSurUnAutreSbire(effect, message, joueur, this)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Minion,
        ).SetPlay(hero_form_only=True),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.HeroResponse,
            "AttachedMinion",
            mission_objective,
            conditions=[tue_par_le_heros],
        ).SetTarget(Scheme2),
    ]
