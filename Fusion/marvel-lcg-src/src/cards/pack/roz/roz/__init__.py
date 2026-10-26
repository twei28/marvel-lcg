from cards.pack import *

# Helpers partages du set « Roz » (jakxin, prefixe `rz`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un
# NameError avale par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
#
# LA CAPACITE « SPECIAL » (fiche mots-cles/special.md) : mot-cle officiel du pack Black Panther (51xxx).
# `Joueur.ResolveSpecialAbility(faces, effect)` envoie `WhenResolveSpecialAbility` a chaque carte ; chaque
# carte porte son Special par `AbilityFactory.WhenResolveSpecialAbility("This", op)`. Modeles : 51001a
# (le heros Black Panther declenche le Special de ses ameliorations), 51010/51013 (Specials d'ameliorations),
# 51025 Heart of the Panther (un evenement qui en resout plusieurs).

TRAIT_WAKANDA = "WAKANDA"
# Types de carte qui peuvent porter un Special : le heros Roz (rz001a), les ameliorations, le soutien A.T.M.C.P.,
# les allies Okoye / Aneka / Ayo du Black Panther officiel (51022-51024).
TYPES_AVEC_SPECIAL = "Hero|Ally|Upgrade|Support"

ID_THOR_JANE = "rz002"
ID_THOR_ODINSON = "rz003"
NOM_COMPTEUR_AGENT = 'agent'


def EstUnThor(face: 'CardFace') -> bool:
    """« Thor ally » : le NOM de la carte est « Thor » (l'etoile d'unicite ne compte pas)."""
    return str(face.name).lstrip("* ").strip() == "Thor"


def FinderThor() -> 'CardFinder':
    """Chaque allie Thor, de n'importe quel joueur (rz002, rz003 : « Each Thor ally gains ... »).

    ⚠ PAS `CardFinder(name="Thor")` : la regle des capacites REFERENTIELLES (`Referential.Check`, `v16_referential_ability`) fait qu'un
    nom cite par une carte ne designe pas une AUTRE carte du meme nom (« 1. The card on which the referential ability is printed ») :
    Jane ne voyait jamais Odinson, ni l'inverse, et chaque Thor ne recevait que SA propre Reponse (constate le 26/10/2026 au cas
    `rz_nb_reponses`). Un `check_face_fn` ne passe pas par le controle du nom."""
    return CardFinder(card_type=Ally, check_face_fn=EstUnThor)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier : il leve un assert
    quand l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def ADesSpecial(effect: 'Effect', face: 'CardFace') -> bool:
    """`check_fn` des selecteurs : la carte IMPRIME au moins une capacite « Special ».

    Lire les capacites DECLAREES (`face.ability`), jamais `face.effect` (les effets enregistres, qui dependent
    de la zone) : recette `special.md` / zeus.
    """
    Unused(effect)
    return bool(face.ability.Find(type=AbilityType.Special))


def CarteWakandaSousControle(ability: 'Ability', *, types: str = TYPES_AVEC_SPECIAL, autre: bool = False) -> 'Ability':
    """« a [[WAKANDA]] card you control » : le selecteur des cartes dont on peut resoudre le Special.

    Seules les cartes qui imprimient un Special sont proposees (une carte WAKANDA sans Special n'a rien a
    resoudre). `autre=True` : « ANOTHER [[WAKANDA]] card you control » (exclut la carte qui porte la capacite).
    """
    options = dict(trait=TRAIT_WAKANDA, from_where=["YouControlCards"], check_fn=ADesSpecial)
    if autre:
        options["exclude"] = "This"
    return ability.SetTarget(types, **options)


def SpecialsResolusCeTour(joueur: 'Player|None') -> int:
    """Combien de capacites « Special » ont ete resolues POUR ce joueur pendant ce tour.

    Alimente par `EffectInvoker._ResolveSelfInternal` (`PlayerStat.this_turn_resolved_specials`, CORRECTIF du
    25/10/2026) : `rz002` (« for each Special resolved this turn ») et `rz003` (« if you resolved a Special
    this turn »).
    """
    if joueur is None:
        return 0
    return len(joueur.stat.this_turn_resolved_specials)


def ResoudreSpecialSurAmelioration(effect: 'Effect', joueur: 'Player|None') -> None:
    """« Resolve the "Special" ability on a [[WAKANDA]] upgrade. » (Trained Shots, Negotiator.)

    Le joueur CHOISIT l'amelioration au moment de resoudre (modele 51025 : `ChooseAbilities` + `ForChoiceAbility`).
    Sans amelioration WAKANDA a Special, rien ne se passe.
    """
    if joueur is None:
        return
    joueur.ChooseAbilities(
        effect,
        CarteWakandaSousControle(
            AbilityFactory.ForChoiceAbility(
                "Resolve the \"Special\" ability on a WAKANDA upgrade",
                lambda targets: joueur.ResolveSpecialAbility(targets, effect),
            ),
            types="Upgrade",
        ),
    )


def ReponseDonneeParJane() -> 'Ability':
    """Octroyee a chaque allie Thor par rz002 : « Response: After this card uses a basic power, resolve the
    "Special" on a [[WAKANDA]] card you control. »"""

    def reponse(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.ResolveSpecialAbility(effect.targets, effect)

    return CarteWakandaSousControle(
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.Response, "This", reponse)
    )


def ReponseDonneeParOdinson() -> 'Ability':
    """Octroyee a chaque allie Thor par rz003 : « Response: After you resolve a "Special" ability on a card you
    control, deal 1 damage to an enemy (limit once per turn). »

    « limit once per TURN » (RR « Limit », CORRECTIF du 26/10/2026 : c'etait « une fois par round », ce qui bridait le
    multijoueur, ou chaque joueur a SON tour dans le round) : le numero de tour (`world.stat.turn_serial`, qui change a
    chaque debut ET a chaque fin de tour) est note SUR l'allie Thor qui recoit la Reponse, au moment ou elle se resout.
    Chaque Thor a SA limite (« each Thor ally gains ... ») : l'objet `Ability` est partage, pas la limite."""

    def pas_encore_ce_tour(effect: 'Effect', message: 'Message.AfterEffectResolved') -> bool:
        Unused(message)
        return getattr(effect.this, "rz003_tour", None) != effect.world.stat.turn_serial

    def reponse(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this
        Unused(message)
        this.rz003_tour = effect.world.stat.turn_serial
        this.DealDamage(effect.targets, 1, effect)

    return AbilityFactory.AfterPlayerResolveAbility(
        AbilityType.Response,
        "You",
        None,
        reponse,
        which_abilities=["Special"],
        control_by_you=True,
        conditions=[pas_encore_ce_tour],
    ).SetTarget(Enemy)
