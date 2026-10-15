from . import *

# Cloning Program — COMPLOT ANNEXE x2 (Skrull Elite - War Skrull). Menace 4 (fixe), 1 icone de boost,
# aucune icone au milieu de la boite de texte.
# Each SKRULL minion activates 1 additional time during the step two of the villain phase.
# Threat cannot be removed from this scheme while there is no SKRULL minion in play.
#
# Cartes de reference :
#  - « cannot be removed ... while there is no X in play » : **`sk033`** DNA Masking
#    (`ThreatCannotBeRemovedFromWhile("This", conditions=[...])`, condition INVERSE).
#  - « activates 1 additional time » : `AfterEnemyActivationEnd` (activate.py) + `Enemy.DoActivate(joueur,
#    effect)` (modele **`sk154`** Devos : `this.DoActivate(joueur, effect)`) ; l'activation de SURCROIT est
#    declenchee une seule fois par activation (marque `activation_clone`), sinon elle se rappellerait sans fin.
#  - « step two of the villain phase » : `world.phase.IsVillainPhaseStep(2)` (world/phase.py).
#
# ⚠ Mots-pieges : « EACH SKRULL MINION » (les sbires seulement, pas le mechant Skrull) ; « ADDITIONAL time »
# (1 activation de plus, pas un doublement : l'activation de surcroit n'en cree pas d'autre) ; « DURING THE STEP
# TWO » (une activation hors etape 2, par une carte, n'est pas doublee) ; elle vise le MEME joueur que
# l'activation d'origine, juste apres elle ; « no SKRULL minion in play » : aucun sbire Skrull du tout.


def GetAbilities() -> Sequence['Ability']:

    def aucun_sbire_skrull(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        Unused(message)
        return not SbiresSkrull(effect)

    def en_etape_deux(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        sbire = message.trigger
        return effect.world.phase.IsVillainPhaseStep(2) and sbire.IsInPlay() and \
            not getattr(sbire, "activation_clone", False)

    def encore_une_fois(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        sbire = message.trigger.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        sbire.activation_clone = True
        try:
            sbire.DoActivate(joueur, effect)
        finally:
            sbire.activation_clone = False

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This", conditions=[aucun_sbire_skrull]),
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.NonKeyword,
            CardFinder(card_type=Minion, trait="SKRULL"),
            encore_une_fois,
            conditions=[en_etape_deux],
        ),
    ]
