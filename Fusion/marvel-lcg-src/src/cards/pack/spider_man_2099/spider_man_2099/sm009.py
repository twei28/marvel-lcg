from . import *

# Fangs and Talons — AMELIORATION, cout 2 [physical]. CONDITION. SUPERPOWER.
# Your hero gets +1 ATK.
# Hero Interrupt: When you play an ATTACK event using your Acceleration
#   ability, exhaust Fangs and Talons -> increase the amount of damage that
#   event deals by 1 and its attacks gain piercing.
#
# CARTES DE REFERENCE
#  - `ho006` * Norman Osborn : MOT POUR MOT le meme declencheur et le meme
#    effet de base — `WhenPlayerPlayCard(HeroInterrupt, "You",
#    CardFinder2("ATTACK", Event), op)` + un `RegisterTemp` de
#    `WhenUnitWouldAttack(Temp0, "You", DealAdditionalDamage(1),
#    by_effect=message.played_effect)`, borne par
#    `until_resolve_effect=message.played_effect`. `32047` et `54002` sont les
#    cartes officielles derriere ce montage.
#  - `27078`, `ho016`, `bl007` Bandolier of Stakes : « gains piercing » sur
#    une attaque en cours = `atk_message.GainPiercing(effect)`, pose sur le
#    MEME temp que les degats (Blade a paye l'ordre des deux : le bonus
#    s'applique avant tout doublement, `can_attack.py:374`).
#  - `an008`, `ho008` : « Your hero gets +1 ATK » =
#    `GiveKeywordToAttached("You", attack=1)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR HERO gets +1 ATK » est ecrit `GiveKeywordToAttached("You", ...)`,
#    c'est-a-dire sur l'IDENTITE, et c'est volontaire : l'ATK n'existe pas sur
#    une face alter-ego, le bonus y est donc inerte de lui-meme. La nuance
#    « nom propre vs you » de `an002` Sera (RECETTES §3), trouvee en partie
#    reelle, mordrait sur une taille de main ou des PV — pas ici. Le contre-cas
#    dans l'AUTRE forme reste du, justement pour le prouver.
#  ⚠ La fabrique rend une LISTE d'abilities : elle se deballe avec `*`
#    (modeles `ho008`, `an008`). Sans l'etoile, la liste entiere serait passee
#    comme une seule ability.
#  ⚠ « USING YOUR ACCELERATION ABILITY » : sans ce filtre, la carte se
#    declencherait sur TOUT evenement ATTACK joue normalement — soit, dans ce
#    deck, Rapid Strikes et Shock and Awe a chaque fois. C'est la difference
#    entre cette carte et `ho006`, qui elle n'a aucune condition. Le filtre va
#    dans `conditions` (RECETTES §1) : une Interruption est PROPOSEE des que le
#    message part, un `return` en tete de corps ne l'evite pas (lecon `bc010`).
#  ⚠ « EXHAUST Fangs and Talons → » : la fleche en fait un COUT. Inclinee, la
#    carte ne peut plus servir ce tour : c'est ce qui borne le Q/R de l'insert
#    (« Using Fangs and Talons, each attack would deal 3 damage » — le bonus
#    vaut pour TOUT l'evenement, pas pour une seule des repetitions de Rapid
#    Strikes, puisqu'il est pose sur l'effet joue et non sur une attaque).
#  ⚠ « increase the amount of damage THAT EVENT deals by 1 » : c'est
#    l'evenement joue qui est vise (`by_effect=message.played_effect`), pas le
#    heros ni une attaque quelconque.
#  ⚠ « ITS ATTACKS gain piercing » : le pluriel compte. Rapid Strikes frappe
#    jusqu'a 4 fois ; toutes ses attaques percent, pas seulement la premiere.
#    Le temp n'est donc PAS `unregister_after_exec=True`.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet (l'inclinaison joue ce
#    role, et un cas doit le montrer : deux evenements ATTACK dans la meme
#    phase, le second sans bonus).


def GetAbilities() -> Sequence['Ability']:

    def via_acceleration(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        Unused(message)
        return AccelerationEnCours(effect)

    def crocs(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Upgrade)

        def renforcer(e2: 'Effect', atk_message: 'Message.WhenUnitWouldAttack') -> None:
            atk_message.DealAdditionalDamage(1, e2)
            atk_message.GainPiercing(e2)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                renforcer,
                by_effect=message.played_effect,
            ),
            unregister_after_exec=False,
            until_resolve_effect=message.played_effect,
        )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            # ⚠ `Hero` et non `"You"` : le texte dit « YOUR HERO gets ». Sur
            # cette carte-ci la nuance est invisible (ni ATQ ni DEF n'existent
            # en alter-ego), mais `sm012` Web Cape a montre le 08/09/2026 que
            # `"You"` fait bien fuir le bonus sur l'autre face — on s'aligne.
            Hero,
            attack=1,
        ),

        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            CardFinder2("ATTACK", Event),
            crocs,
            conditions=[via_acceleration],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
