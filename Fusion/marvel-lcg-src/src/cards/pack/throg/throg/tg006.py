from . import *

# Thunderous Charge — EVENEMENT, cout 2, [mental]. SUPERPOWER. x2.
# Hero Interrupt: When you make a basic thwart against a scheme, resolve that
#   thwart against each scheme in play instead, ignoring the crisis icon
#   (in the order of your choice, including any bonuses to your THW for that
#   thwart).
#
# CARTES DE REFERENCE
#  - `25013` * Thor: Odinson : le jumeau cote ATTAQUE — un Interrupt qui
#    AJOUTE des cibles a l'activation en cours par `message.AddTarget(...)`,
#    avec `.SetTarget(fn, range="All")`. La resolution du contre lit la meme
#    liste (`would_thw_message.targets`, can_thwart.py:122), donc le montage
#    se transpose tel quel.
#  - `21191` * Fandral : « When Fandral uses his basic THW, ignore any crisis
#    icons in play » -> `UnitIgnoreKeywordIcons(<face>, crisis=True,
#    while_use_basic_thw=True)`. C'est la SEULE carte du depot qui passe
#    `while_use_basic_thw`, et le parametre a ete repare le 02/09/2026.
#  - `ho006` : `RegisterTemp(..., until_...)`, la capacite temporaire posee
#    par un evenement le temps d'une resolution.
#
# TEXTE CONTRE CODE
#  ⚠ « INSTEAD », comme sur tg005 : la manigance visee fait partie de « each
#    scheme in play », elle reste donc dedans. On AJOUTE les manquantes
#    (`AddTarget`), on ne remplace pas la liste. Et JAMAIS un doublon : la
#    resolution multiplie la valeur par le nombre d'occurrences
#    (`schemes_dict[target] * thwart`, can_thwart.py:148).
#  ⚠ « including any BONUSES to your THW for that thwart » -> c'est le
#    comportement natif : `property.GetThwart(this)` est recalcule pour
#    CHAQUE cible de la liste (can_thwart.py:145). Un +2 CTR s'applique donc
#    bien a chaque manigance. Rien a coder, et c'est ce que le cas mesure.
#  ⚠ « ignoring the CRISIS icon » -> fiche `mots-cles/crisis.md`. La crise
#    est lue dans `MainScheme.RemoveThreatInternal` (scheme_main.py:150), sur
#    l'effet du CONTRE DE BASE, pas sur celui de l'evenement : un
#    `.SetIgnoreKeyword('Crisis')` pose sur CETTE carte (montage `42006`,
#    `44023`) ne servirait a rien. Il faut une capacite TEMPORAIRE qui vise
#    la face du heros, d'ou le `RegisterTemp` ci-dessous, borne par
#    `until_event_end=message`.
#  ⚠ ECART ASSUME : « in the order of YOUR CHOICE ». Le moteur resout les
#    manigances dans l'ordre de la liste (can_thwart.py:139), le joueur ne
#    choisit pas. Sans consequence tant qu'aucune manigance ne declenche un
#    effet en etant vaincue ; a rouvrir le jour ou une carte du jeu rendra
#    l'ordre observable.


def GetAbilities() -> Sequence['Ability']:

    def charge_tonnante(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Event)

        # ⚠ LES CIBLES SONT CALCULEES ICI, PAS DANS UN `SetTarget` — meme leçon
        # que tg005 : sur un EVENEMENT joue en Interruption, le selecteur est
        # evalue AVANT que l'effet ne soit lie au message, et rend une liste
        # vide. L'abilite n'est alors jamais proposee. Le texte dit « each
        # scheme in play » : il n'y a aucun choix a faire.
        # ⚠ JAMAIS UN DOUBLON : `schemes_dict[target] * thwart`
        # (can_thwart.py:148) multiplierait la valeur sur une manigance visee
        # deux fois.
        deja_visees = list(message.targets)
        ajouts = [x for x in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                  if x is not None and x not in deja_visees]
        if ajouts:
            message.AddTarget(*ajouts)

        # « ignoring the crisis icon » : la crise est lue sur l'effet du
        # contre de base, pas sur celui de cet evenement.
        # ⚠ LA CAPACITE TEMPORAIRE EST PORTEE PAR LE HEROS, PAS PAR CETTE CARTE.
        # Un evenement joue quitte le jeu, et ses effets temporaires partent
        # avec lui AVANT que le contre ne retire la menace : l'ignorance de la
        # crise ne s'appliquait donc jamais, et le complot principal gardait
        # ses menaces (mesure du 05/09/2026). Meme leçon que `ah007`.
        contreur = message.trigger
        Unused(this)
        if contreur is not None:
            contreur.effect.RegisterTemp(
                AbilityFactory.UnitIgnoreKeywordIcons(
                    contreur,
                    crisis=True,
                    while_use_basic_thw=True,
                ),
                unregister_after_exec=False,
                until_event_end=message,
            )

    return [
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.HeroInterrupt,
            "You",
            Scheme2,
            charge_tonnante,
            is_basic_thwart=True,
        ).SetPlay(),
    ]
