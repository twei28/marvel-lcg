from . import *

# Spiderlings — ALLIE, cout 1 [physical], THW 1 / ATK 1 (1 degat consequent
# chacun), 2 PV. HENCHMAN. SOLDIER.
# [star] Interrupt: When Spiderlings thwart, track a minion instead of removing
#   threat.
# [star] Spiderlings take -1 consequential damage after attacking a tracked
#   minion.
#
# CARTES DE REFERENCE
#  - `aa010`, `ag012`, `av002`, `tg016` : « ... INSTEAD » sur un pouvoir de base
#    = `message.SetBeInstead(effect)` sur le message `WhenUnitWould...`.
#    ⚠ RECETTES §2 : PAS depuis `WhenUnitUseBasicPower`, envoye APRES le test de
#    remplacement — le `SetBeInstead` arriverait toujours trop tard.
#  - `33016` Coordinated Attack (qui la BAISSE de 1) et `bc002` (qui la monte) :
#    les degats consequents se modifient par
#    `ally.GainForThisActive(effect, would_message, attack_consequential_damage=N)`.
#    ⚠ RECETTES §5 : `Message.WhenAllyWouldTakeConsequentialDamage` n'est envoye
#    que si la valeur imprimee est DEJA > 0 — ici elle vaut 1 (l'asterisque de
#    `"ATK": "1*"`), le message part donc bien.
#
# TEXTE CONTRE CODE
#  ⚠ « INSTEAD of removing threat » : le contre de Spiderlings ne retire RIEN
#    de la manigance par la voie normale ; c'est le `track` qui deplace 1
#    menace. Coder « contre puis track » ferait retirer DEUX fois.
#  ⚠ « track A MINION » : un sbire au choix, pas forcement engage (insert).
#  ⚠ « after attacking A TRACKED MINION » : la reduction ne vaut que contre un
#    sbire qui PORTE de la menace au moment de l'attaque. Contre un sbire non
#    trace, Spiderlings prend bien son degat consequent.
#  ⚠ Les deux capacites sont des `[star]` : permanentes, pas des Boost.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def contre_en_track(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not PeutTracer(effect):
            return
        message.SetBeInstead(effect)

        def puis_le_complot(sbires: Sequence['CardFace']) -> None:
            # ⚠ DEUX choix, et il en faut bien deux : `track` prend UN sbire ET
            # UNE manigance (« move 1 threat FROM A SCHEME TO a minion »). Un
            # seul `SetTarget` ne peut pas porter les deux types (RECETTES §6 :
            # « deux types de cibles dans un meme effet : la seconde par
            # ChooseAbilities dans l'operation »).
            sbire = sbires[0] if sbires else None
            if sbire is None:
                return
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Move 1 threat from that scheme to the minion",
                    lambda complots: Tracer(effect, sbire, complots),
                ).SetTarget(Scheme2, range=(1, 1)),
            )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Track a minion instead of removing threat",
                puis_le_complot,
            ).SetTarget(Minion, range=(1, 1)),
        )

    def moins_un_degat(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        vises = [c for c in (getattr(message, "attacked_targets", None) or [])
                 if c is not None]
        if not any(MenaceSurSbire(c) > 0 for c in vises):
            return
        this.GainForThisActive(
            effect,
            getattr(message, "would_atk_message", None),
            attack_consequential_damage=-1,
        )

    return [
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.Interrupt,
            "This",
            contre_en_track,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.NonKeyword,
            "This",
            moins_un_degat,
        ),
    ]
