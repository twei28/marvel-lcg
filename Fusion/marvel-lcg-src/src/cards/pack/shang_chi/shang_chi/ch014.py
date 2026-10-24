from . import *

# Augmented Blow — EVENEMENT, cout 1, impression 12/15 : ressource(s) imprimee(s) physique. ATTACK. (card_id ch014)
# Hero Action (attack): Deal 1 damage to a minion. Place 1 additional counter on an upgrade with any type of counters on it.
# Flow: [energy] → choose up to 2 upgrades with any type of counter on them. Place 2 additional counters on each of them.
#
# ⚠ IMPRESSIONS : Augmented Blow existe en DEUX cartes (ch013) qui ne different que par l'ICONE DE RESSOURCE du coin ;
#   `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).
#
# Cartes de reference :
#  - `64004`/`10005` pour le Hero Action (attack) ; cible sbire : `bw002` (`SetTarget(Minion)`).
#  - compteurs : `Faces.PlaceCountersOn([amelioration], n, nom, effect)` (`dz002`) ; lecture `face.components.counter.counters`.
#  - liste de cibles fournie : `tc001b` (`SetTarget(liste, range=..., not_move=True)`).
#
# ⚠ Mots-pieges :
#  - DECISION UTILISATEUR (24/10/2026) : « ADDITIONAL counter » = un compteur du MEME TYPE que ceux deja presents (au choix s'il y a
#    plusieurs types) ; toute amelioration EN JEU avec au moins un compteur est cible (pas seulement celles de Shang-Chi).
#  - « an upgrade WITH counters » : une amelioration sans compteur n'est PAS ciblable.
#  - Flow : « up to 2 » ameliorations, 2 compteurs sur CHACUNE ; Flow [energy] exige un eclair imprime.


def AmeliorationsAvecCompteurs(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade)
            if any(v > 0 for v in f.components.counter.counters.values())]


def PoserCompteursAdditionnels(effect: 'Effect', joueur: 'Player', amelioration: 'CardFace', n: int) -> None:
    types = [nom for nom, v in amelioration.components.counter.counters.items() if v > 0]
    if not types:
        return
    if len(types) == 1:
        Faces.PlaceCountersOn([amelioration], n, types[0], effect)
        return
    options = [
        AbilityFactory.ForChoiceAbility(
            f"Place {n} {nom} counter(s)",
            lambda cibles, nom=nom: Faces.PlaceCountersOn([amelioration], n, nom, effect),
        )
        for nom in types
    ]
    joueur.ChooseAbilities(effect, *options)


def GetAbilities() -> Sequence['Ability']:

    def augmented_blow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        if joueur is None:
            return
        candidates = AmeliorationsAvecCompteurs(effect)
        if candidates:
            def poser_un(cibles: Sequence['CardFace']) -> None:
                for amelioration in cibles:
                    PoserCompteursAdditionnels(effect, joueur, amelioration, 1)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Place 1 additional counter on an upgrade", poser_un,
                ).SetTarget(candidates, range=(1, 1), not_move=True),
            )

        if AccepterFlow(effect, joueur, "Y"):
            candidates = AmeliorationsAvecCompteurs(effect)
            if candidates:
                def poser_deux(cibles: Sequence['CardFace']) -> None:
                    for amelioration in cibles:
                        PoserCompteursAdditionnels(effect, joueur, amelioration, 2)

                joueur.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Place 2 additional counters on each of up to 2 upgrades", poser_deux,
                    ).SetTarget(candidates, range=(1, 2), not_move=True),
                )
            FlowResolu(joueur, this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            augmented_blow,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Minion),
    ]
