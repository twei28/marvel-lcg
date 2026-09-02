from . import *

# Just a Phase — evenement signature, x2 (n/15 = 2 et 3). SUPERPOWER. THWART.
# Cout 1, ressource [mental].
# Hero Interrupt: When your hero makes a basic thwart, they get +3 THW and
#   ignore the patrol keyword and the crisis icon ([crisis]) for that thwart.
#   This thwart gains breakthrough.
#
# Cartes de reference :
#  - 61023 Grapnel Launcher (pack jj), src/cards/pack/jj/61023.py : la SEULE
#    carte du depot qui ignore `patrol`. Meme montage exact —
#    `WhenInYourPlayTurn(HeroAction, ...).SetLabel('thwart')
#    .SetTarget(Scheme2, range=(1, 1)).SetIgnoreKeyword('Crisis', 'Patrol')`
#    puis `hero.BasicThwart(effect.targets, effect,
#    property=ThwartProperty(additional_value=N))` ;
#  - 20013 Making an Entrance (pack vnm) pour l'effet de SUITE branche sur la
#    menee (`RegisterTemp` d'une abilite sur un message de menee, filtree sur
#    la menee en cours) : c'est le squelette du `breakthrough` ci-dessous ;
#  - 08013 Stealth Strike pour le choix d'une seconde manigance par
#    `ChooseAbilities` + `ForChoiceAbility(...).SetTarget(Scheme2)`.
#
# ---------------------------------------------------------------------------
# ⚠ ECART ASSUME, ARBITRE PAR L'UTILISATEUR LE 02/09/2026 :
# LE DECLENCHEUR PASSE DE « Hero Interrupt » A « Hero Action (thwart) ».
#
# Le moteur verifie `patrol` AU CHOIX DE LA CIBLE, pas a la resolution :
# `can_be_thwart_schemes` est pose sur le filtre du selecteur
# (`ability.py:970`) et appelle `MainScheme.CanBeThwartBy`
# (`scheme_main.py:204`), qui rend False des qu'un sbire Patrol est engage.
# La fenetre d'Interruption, elle, ne s'ouvre qu'APRES ce choix, dans
# `ThwartInternal` (`can_thwart.py:103`). Une Interruption fidele au mot
# imprime n'aurait donc JAMAIS pu lever `patrol` : avec un sbire Patrol
# engage, le complot principal n'apparait meme pas dans la liste des cibles.
# `crisis`, lui, est verifie a la RESOLUTION (`MainScheme.RemoveThreatInternal`,
# `scheme_main.py:151`) et aurait tres bien fonctionne en Interruption.
#
# On rend donc la carte comme 61023 : elle EXECUTE la menee elle-meme, ce qui
# met les deux mots-cles dans la fenetre ou le moteur les lit. `BasicThwart`
# produit une VRAIE menee de base, donc tout ce qui reagit a une menee de base
# continue de se declencher (`WhenUnitWouldThwart`, `AfterUnitThwartEnd`
# `is_basic_thwart=True`, et vv009 Insubstantial Flight qui guette
# l'epuisement du heros).
#
# PERTE ASSUMEE, la seule : en Interruption, la carte aurait pu bonifier une
# menee de base offerte par une AUTRE carte (« make a basic thwart »). En
# Action, elle ne bonifie que la sienne. Aucune carte du kit de Viv n'offre ce
# cas ; quelques cartes d'aspect si.
#
# ⚠ L'EPUISEMENT EST UN COUT AJOUTE. 61023 imprime « without exhausting », pas
# nous : une menee de base epuise le heros. `CostFunc.Exhaust("YourIdentity")`
# retablit ce que le passage en Action aurait offert gratuitement.
# ---------------------------------------------------------------------------
#
# ⚠ Le mot-cle maison `breakthrough` : voir docs/reference/mots-cles/
# breakthrough.md, qui porte la definition complete et les quatre pieges.
# En deux lignes : l'exces de menee se reporte sur une AUTRE manigance choisie
# par le joueur, exactement comme `overkill` reporte des degats. L'exces se
# lit sur `Message.AfterUnitThwartScheme`, envoye DANS la boucle de
# `ThwartInternal` juste apres `RemoveThreatInternal` — donc pendant que les
# bonus de menee sont encore actifs, ce qui n'est plus vrai a
# `AfterUnitThwartEnd`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « THEY get +3 THW » : le heros qui menee, pas la carte. Rendu par
#    `ThwartProperty(additional_value=3)`, que `BasicThwart` marque ensuite
#    `is_basic_power=True`.
#  - « for THAT thwart » : le bonus ne vit que le temps de la menee, ce que
#    `additional_value` garantit par construction (il vit sur la propriete de
#    CETTE menee, pas sur le heros).
#  - « ignore the patrol keyword AND the crisis icon » : les DEUX, d'ou
#    `SetIgnoreKeyword('Crisis', 'Patrol')`. Attention, `IsIgnoreKeyword`
#    refuse 'Patrol' si l'abilite n'est pas `is_like_thwart`
#    (`effect.py:491`) : le `.SetLabel('thwart')` n'est pas cosmetique.
#  - Le report de `breakthrough` passe par le MEME effet, donc il ignore lui
#    aussi crisis. C'est voulu : le texte dit « for that thwart », et le
#    report fait partie de cette menee.
#  - « ANOTHER eligible target » (definition du mot-cle) : la manigance visee
#    est exclue du choix (`exclude=`), et seules celles qui portent encore de
#    la menace sont proposees (`has_threat=True`).


def GetAbilities() -> Sequence['Ability']:

    def just_a_phase(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        hero = joueur.GetHero()
        if hero is None:
            return

        def cette_menee(thw_effect: 'Effect', thw_message: 'Message.AfterUnitThwartScheme') -> bool:
            Unused(thw_effect)
            return thw_message.would_thw_message.by_effect is effect

        def reporter_l_exces(thw_effect: 'Effect', thw_message: 'Message.AfterUnitThwartScheme') -> None:
            Unused(thw_effect)

            unit = thw_message.trigger
            propriete = thw_message.would_thw_scheme_message.property
            voulu = propriete.GetThwart(unit)
            exces = voulu - thw_message.remove_threat
            if exces <= 0:
                return

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Breakthrough",
                    lambda cibles: this.RemoveThreatFromSchemes(cibles, exces, effect),
                ).SetTarget(
                    Scheme2,
                    exclude=[thw_message.scheme],
                    has_threat=True,
                ),
            )

        # L'abonnement se pose AVANT la menee et meurt avec la resolution de
        # cet effet : la carte ne laisse rien derriere elle.
        this.effect.RegisterTemp(
            AbilityFactory.AfterUnitThwartScheme(
                AbilityType.Temp0,
                None,
                None,
                reporter_l_exces,
                conditions=[cette_menee],
            ),
            unregister_after_exec=False,
            until_resolve_effect=effect,
        )

        hero.BasicThwart(
            effect.targets,
            effect,
            property=ThwartProperty(additional_value=3),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            just_a_phase,
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetTarget(Scheme2, range=(1, 1))
        .SetIgnoreKeyword('Crisis', 'Patrol'),
    ]
