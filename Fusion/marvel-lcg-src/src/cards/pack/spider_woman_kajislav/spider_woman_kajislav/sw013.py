from . import *

# * Shroud — ALLIE d'aspect PROTECTION, cout 3, 2 PV, CTR 2*, ATQ 1*,
# RES [mental]. HERO FOR HIRE.
# Interrupt: When you reveal an encounter card, exhaust Shroud and deal 2
#   damage to him -> cancel the effects of that card and discard it.
#
# ⚠ DEUX PV, ET LE COUT EST DE DEUX DEGATS : Shroud annule UNE carte, puis
# meurt. C'est un consommable a 3, pas un allie.
#
# CARTES DE REFERENCE
#  - `30005` "I Don't Think So!" (pack spiderham) : le montage exact —
#    `WhenPlayerRevealCard(HeroInterrupt, "You", None, "All", op,
#    from_encounter=True)` puis `message.CancelAllEffectsAndDiscardIt(effect)`.
#    La primitive existe et dit mot pour mot la phrase imprimee.
#
# TEXTE CONTRE CODE
#  ⚠ « Interrupt », PAS « Hero Interrupt » : Shroud annule aussi en forme
#    civile, ce qui est rare et vaut son prix.
#  ⚠ DEUX COUTS avant la fleche : l'inclinaison ET les 2 degats. Les deux
#    `SetCostFunc` sont chaines ; s'il ne peut pas payer l'un, la fenetre n'est
#    pas offerte.
#  ⚠ « deal 2 damage TO HIM » : a Shroud, pas a un personnage au choix. Et
#    c'est bien un COUT, donc il MEURT AVANT que l'annulation ne resolve.
#
#    ⚠⚠ CETTE CARTE A COUTE TROIS CORRECTIFS, dont un DANS LE MOTEUR. Elle
#    payait son prix et ne faisait rien, sans une ligne de journal. Dans
#    l'ordre ou ils ont ete trouves, le 10/09/2026, chacun par le harnais :
#      1. `CostFunc.TakeDamage("This", 2)` : arguments a l'envers, c'est
#         `(valeur, cible)`. TypeError avale par le moteur.
#      2. `TakeDamageOnCall` (cost_func.py:15) declarait le cout IMPAYE des
#         lors que le payeur tombait. Shroud a 2 PV et se met 2 degats : la
#         carte etait donc INJOUABLE PAR CONSTRUCTION. La ligne est retiree,
#         avec sa justification sur place.
#      3. `.NoOutOfPlayLimit()` : sans elle, une capacite dont la carte a
#         quitte le jeu est abandonnee (deja employe par `sw002` Madame Web).
#      4. Et la condition maison ci-dessous, pour la meme raison.
#  ⚠ « that card » : celle qu'on est en train de reveler, d'ou `"All"` en
#    quatrieme argument (toutes les cartes de rencontre, pas un type).


def GetAbilities() -> Sequence['Ability']:

    def revele_par_son_proprietaire(effect: 'Effect',
                                    message: 'Message.WhenPlayerRevealCard') -> bool:
        """« When YOU reveal an encounter card » — mais ecrit a la main.

        ⚠⚠ `which_player="You"` NE MARCHE PAS ICI, et le defaut est muet.
        « You » se resout par le CONTROLEUR de la carte porteuse, et les
        conditions sont relues APRES le paiement du cout. Or le cout tue
        Shroud : au moment ou le moteur reverifie, l'allie est dans la
        defausse, il n'a plus de controleur, la condition tombe, et
        l'operation n'est JAMAIS lancee. Aucune trace, aucune exception : la
        carte payait son prix et ne faisait rien. Trouve le 10/09/2026 en
        posant une sonde `print` dans l'operation, faute d'autre signal.

        Le PROPRIETAIRE, lui, survit a la defausse (`card.GetOwner()`), et
        c'est bien lui que la carte designe.
        """
        proprietaire = effect.this.card.GetOwner()
        return Player.IsType(proprietaire) and proprietaire is message.to_player

    def linceul(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        Unused(effect.this)
        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.Interrupt,
            "AnyPlayer",
            None,
            "All",
            linceul,
            from_encounter=True,
            conditions=[revele_par_son_proprietaire],
        ).NoOutOfPlayLimit()
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(2, "This")),
    ]
