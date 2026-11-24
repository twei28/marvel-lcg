from . import *

# Quantum Jump — amelioration signature (QUASAR 15/16). SUPERPOWER.
# Cout 2, [wild].
# Hero Interrupt: When you pay for a THWART event with Quantum Bands, that
#   thwart removes 2 additional threat and ignores the crisis icon ([crisis])
#   and the patrol keyword.
#
# Cartes de reference :
#  - **`34020`** Passion for Justice : au paiement d'un evenement THWART,
#    `RegisterTemp(WhenUnitWouldThwart(Temp0, "You", RemoveAdditionalThreat(1),
#    conditions=[for_effect == thw_message.by_effect]), unregister_after_exec=True,
#    until_resolve_effect=for_effect)` ; ici +2, et la fenetre est le paiement
#    PAR LES BANDES (helper `QuandLesBandesPaient`, voir gs313).
#  - **`15012`** Crisis Averted / **`hc006`** On the Prowl : l'ignorance de la
#    Crise / Patrouille qui DEPEND DU PAIEMENT. Le moteur choisit les cibles
#    AVANT de payer (effect_checker : `check_target` puis `check_pay`) : tant
#    que rien n'est paye, le complot principal doit rester ciblable si les
#    Bandes PEUVENT payer ; a la resolution, on tranche sur ce qui a vraiment
#    ete fait. `UnitIgnoreKeywordIcons` (factory/play.py) montre la forme : une
#    capacite NonKeyword qui repond a `Message.CheckIfEffectIsIgnoreKeyWord`.
#
# Montage, en deux temps :
#  1. capacite CONSTANTE (ciblage) : un evenement THWART de ce joueur, pas
#     encore paye, ignore Crise et Patrouille si ses Bandes sont en jeu, pretes,
#     en forme heros ;
#  2. l'Interruption (paiement par les Bandes, acceptee) enregistre, le temps
#     de la resolution de l'evenement, +2 menace sur son contre (Temp0) et
#     MARQUE le paiement ; la capacite constante relit la marque a la
#     resolution (l'ignorance tient alors).
#  Paye SANS les Bandes, ou Interruption refusee : la Crise mord a la
#  resolution (rien n'est retire du complot principal, comme 15012 paye sans
#  [mental]) et la Patrouille aussi (CORRECTIF moteur du 20/10/2026,
#  scheme_main.py : la Patrouille levee AU CIBLAGE est reverifiee a la
#  resolution).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « THAT thwart » : le contre de l'evenement paye, une fois
#    (`unregister_after_exec=True`).
#  - « 2 ADDITIONAL threat » : en plus du texte de l'evenement ; sans contre
#    (No Holding Back paye sans [mental]), rien a augmenter (FAQ p.22).
#  - « ignores the crisis icon AND the patrol keyword » : les deux.
#  - « [[THWART]] event » : trait THWART + type evenement (Flight of Light, No
#    Holding Back, Multitalented...).


def GetAbilities() -> Sequence['Ability']:

    MOTS = ("Crisis", "Patrol")

    def evenement_contre_de(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and Event.IsType(face) and face.HasTrait("THWART") \
            and face.GetControlByOrOwner() == joueur

    def offert(effect: 'Effect', message: 'Message.CheckIfEffectIsIgnoreKeyWord') -> bool:
        cible = message.effect
        if message.keyword not in MOTS or not evenement_contre_de(effect, cible.this):
            return False
        # Resolution : l'Interruption a ete acceptee pour CE paiement. La marque
        # est la LISTE des payeurs de l'activation (`paid_this_res_effects`),
        # recreee par `EffectContext.ResetAfterOperation` a chaque activation :
        # comparee par identite (`is`), elle ne survit pas a l'activation.
        payeurs = cible.context.paid_this_res_effects
        if any(marque is payeurs for marque in getattr(effect.this.card, "sauts_quantiques", [])):
            return True
        # Ciblage : rien n'est encore paye, les Bandes PEUVENT payer.
        return RienPayeEncore(cible) and BandesPeuventPayer(JoueurDeCetteCarte(effect))

    def saut(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)
        paye = message.for_effect

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldThwart(
                AbilityType.Temp0,
                "You",
                lambda effect2, thw_message: thw_message.RemoveAdditionalThreat(2, effect2),
                conditions=[lambda effect2, thw_message: thw_message.by_effect == paye],
            ),
            unregister_after_exec=True,
            until_resolve_effect=paye,
        )
        # ⚠ Pas un Temp0 sur `CheckIfEffectIsIgnoreKeyWord` : mesure au harnais
        # le 20/10/2026, un effet temporaire n'y est jamais consulte (la Crise
        # mordait a la resolution malgre l'Interruption). On marque donc le
        # paiement et la capacite CONSTANTE ci-dessous le relit. On ne garde que
        # les deux dernieres marques (une activation a la fois).
        marques = list(getattr(this.card, "sauts_quantiques", []))[-1:]
        marques.append(paye.context.paid_this_res_effects)
        this.card.sauts_quantiques = marques

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfEffectIsIgnoreKeyWord,
            [offert],
            lambda effect, message: message.SetIgnore(),
        ),
        QuandLesBandesPaient(
            AbilityType.HeroInterrupt,
            CardFinder2("THWART", Event),
            saut,
        ),
    ]
