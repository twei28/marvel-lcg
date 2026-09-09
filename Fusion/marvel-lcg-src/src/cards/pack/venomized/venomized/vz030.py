from . import *

# Durable Physiology — AMELIORATION, cout 2, RES [physical]. CONDITION. SYMBIOTE.
# Uses (2 klyntar counters).
# Hero Interrupt: When a minion would attack you, exhaust this card and remove
#   1 klyntar counter from it -> reduce all damage dealt to you this round by 1.
#
# MOT-CLE
#  - `Uses` (mots-cles/uses.md) : BASE NATIVE, `desc.Uses = "2,klyntar"`. Le
#    moteur pose les pions a l'entree en jeu ET defausse la carte au dernier
#    pion retire. NE PAS RECODER LA SORTIE.
#  - Le compteur `klyntar` a ete ajoute a l'enum `COUNTER` (`card_face.py`) le
#    09/09/2026, en meme temps que le sixieme aspect.
#
# CARTES DE REFERENCE
#  - `01080` Med Team : deux couts chaines, l'inclinaison ET le pion.
#  - `ReduceCharacterTakeDamageBy` (`damage.py:404`) : la reduction continue.
#  - `45131` (pack aoa) : `this.effect.RegisterTemp(..., unregister_after_exec=
#    False)` puis `Effects.UnRegister(...)`, le seul montage du depot pour une
#    capacite qui vit PLUS LONGTEMPS que l'effet qui la pose.
#
# TEXTE CONTRE CODE
#  ⚠ « reduce ALL damage dealt to you THIS ROUND » : ce n'est PAS la reduction
#    de cette seule attaque. La capacite temporaire reste posee jusqu'a la fin
#    du round (`RunAt.RoundEnd`) et s'applique a chaque paquet de degats, y
#    compris ceux d'une traitrise revelee apres.
#  ⚠ « When a MINION would attack you » : seuls les sbires ouvrent la fenetre.
#    Une attaque du vilain ne declenche rien — mais une fois posee, la
#    reduction vaut pour TOUS les degats, vilain compris. Les deux lectures
#    cohabitent dans le texte et ce n'est pas une contradiction.
#  ⚠ « to YOU » : votre identite.
def GetAbilities() -> Sequence['Ability']:

    def durable_physiology(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        temporaire = this.effect.RegisterTemp(
            AbilityFactory.ReduceCharacterTakeDamageBy(
                "YourIdentity",
                1,
            ),
            unregister_after_exec=False,
        )
        RunAt.RoundEnd(effect, lambda: Effects.UnRegister(temporaire))

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Minion,
            durable_physiology,
            against_player="You",
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'klyntar')),
    ]
