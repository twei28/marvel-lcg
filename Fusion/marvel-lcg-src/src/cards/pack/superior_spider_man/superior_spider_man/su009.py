from . import *

# Mechanical Arms — AMELIORATION, cout 3 [physical]. TECH. WEAPON.
# Hero Interrupt (thwart): When you make a basic attack against a minion, track
#   that minion.
# Hero Response: After you use a basic power, exhaust Mechanical Arms -> ready
#   your hero.
#
# CARTES DE REFERENCE
#  - `14001a`, `tt001a`, `tg001a` : « After you use a basic power » =
#    `AfterUnitUseBasicPower(type, "You", op, powers="Hero")`.
#  - `an001a`, `31009`, `ho011` : `Faces.ReadyAll`.
#  - Le mot-cle maison `track` : helper `Tracer` du set.
#
# TEXTE CONTRE CODE
#  ⚠ « When you make a BASIC ATTACK against A MINION » : une attaque DE BASE,
#    pas un evenement ATTACK (`is_basic_attack=True`), et seulement contre un
#    sbire.
#  ⚠ Le libelle imprime de l'Interruption est « (thwart) » ALORS QUE LA CARTE
#    PARLE D'UNE ATTAQUE : c'est bien ce que dit le scan, et c'est logique —
#    `track` deplace de la menace, donc c'est un contre. `SetLabel('thwart')`.
#  ⚠ « track THAT minion » : le sbire attaque, pas un sbire au choix.
#  ⚠ « exhaust ... -> ready YOUR HERO » : la fleche fait de l'inclinaison le
#    COUT ; c'est le HEROS qu'on redresse, pas la carte.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet — l'inclinaison borne a un
#    usage par tour, et un cas doit le montrer.


def GetAbilities() -> Sequence['Ability']:

    def il_y_a_de_la_menace(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        return any(f is not None and getattr(f, "threat", 0)
                   for f in Worlds.GetOnFieldSchemes(effect))

    def tracer_la_cible(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        sbires = [c for c in (getattr(message, "targets", None) or [])
                  if c is not None and Minion.IsType(c)]
        if not sbires:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Move 1 threat from a scheme to that minion (track)",
                lambda complots: Tracer(effect, sbires[0], complots),
            ).SetTarget(Scheme2, range=(1, 1)),
        )

    def redresser(effect: 'Effect', message: Any) -> None:
        Unused(message)
        heros = HerosDuJoueur(effect)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "You",
            tracer_la_cible,
            is_basic_attack=True,
            conditions=[il_y_a_de_la_menace],
        ).SetLabel('thwart'),

        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            redresser,
            powers="Hero",
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
