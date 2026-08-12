from cards.pack import *

################################################################################
# Système de bulles (speech bubbles) de Gwenpool — custom « ekAugust ».
#
# Chaque carte Gwenpool porte une bulle dans son illustration. Quand une
# capacité contient « ____ », Medium Awareness (gp001a) permet de remplacer le
# blanc par la phrase d'une bulle disponible : la carte jouée, l'identité, une
# carte Gwenpool en jeu, ou la carte attachée à Unbelievable Gwenpool.
# Limite : chaque bulle une fois par phase.
#
# Interactions :
# - THE END (gp010) en jeu : aucune bulle utilisable, le blanc reste vide.
# - Rules of the Universe (gp011) en jeu : remplacement FORCÉ par la bulle
#   d'Evil Gwenpool (« Gwenpool takes 1 damage. »), sans limite de phase.
#
# LENIENT : « a card you spend » (bulles des cartes défaussées en paiement)
# n'est pas suivi, hors Endless Storylines dont la Response couvre le cas.
################################################################################


def _bulle_draw1(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    player.DrawUp(1, effect)

def _bulle_deal2_villain(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    villain = Worlds.FindVillain(effect)
    if villain:
        source.DealDamage([villain], 2, effect)

def _bulle_confuse_villain(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    villain = Worlds.FindVillain(effect)
    if villain:
        Faces.GiveStatus([villain], "Confused", effect)

def _bulle_tough(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    Faces.GiveStatus([player.GetHero()], "Tough", effect)

def _bulle_remove2_main(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    source.RemoveThreatFromSchemes("MainScheme", 2, effect)

def _bulle_remove1_scheme(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    player.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Remove 1 threat from a scheme",
            lambda targets:
                source.RemoveThreatFromSchemes(targets, 1, effect)
        ).SetTarget(Scheme2)
    )

def _bulle_heal1(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    source.HealthUnits([player.GetHero()], 1, effect)

def _bulle_deal1_enemy(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    player.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Deal 1 damage to an enemy",
            lambda targets:
                source.DealDamage(targets, 1, effect)
        ).SetTarget(Enemy)
    )

def _bulle_look_top(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    # LENIENT : « any deck » proposé = ton deck ou le deck Rencontre.
    def regarder(deck):
        def action(targets):
            faces = player.LookAtDeck(deck, 1, effect)
            if faces:
                player.PlaceOnTopAndOrBottomInAnyOrder(faces, effect)
        return action

    player.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Look at the top card of your deck",
            regarder(player.player_deck)
        ),
        AbilityFactory.ForChoiceAbility(
            "Look at the top card of the encounter deck",
            regarder("EncounterDeck")
        ),
    )

def _bulle_ready(effect: 'Effect', player: 'Player', source: 'CardFace') -> None:
    Faces.ReadyAll([player.GetHero()], effect)


# card_id -> [(libellé, opération)]
BULLES = {
    "gp001a": [("Gwenpool: “Draw 1 card.”", _bulle_draw1)],
    "gp002": [("“Here I Come!”: “Deal 2 damage to the villain.”", _bulle_deal2_villain)],
    "gp003": [("“It Can't End Like This!”: “Confuse the villain.”", _bulle_confuse_villain)],
    "gp004": [("Fun Background Noise: “Give Gwenpool a tough status card.”", _bulle_tough)],
    "gp005": [("“Sorry, Gotta Run!”: “Remove 2 threat from the main scheme.”", _bulle_remove2_main)],
    "gp006": [("Endless Storylines: “Remove 1 threat from a scheme.”", _bulle_remove1_scheme),
              ("Endless Storylines: “Heal 1 damage from Gwenpool.”", _bulle_heal1),
              ("Endless Storylines: “Deal 1 damage to an enemy.”", _bulle_deal1_enemy)],
    "gp007": [("Gwen's Room: “Heal 1 damage from Gwenpool.”", _bulle_heal1)],
    "gp008": [("Comicbook Panels: “Look at the top card of any deck.”", _bulle_look_top)],
    "gp009": [("Unbelievable Gwenpool: “Ready Gwenpool.”", _bulle_ready)],
}


def _bulles_utilisees(effect: 'Effect') -> set:
    w = effect.world
    s = getattr(w, '_gwenpool_bulles_utilisees', None)
    if s is None:
        s = set()
        setattr(w, '_gwenpool_bulles_utilisees', s)
    return s


def _sources_de_bulles(effect: 'Effect', player: 'Player') -> list:
    faces = []
    if effect.this is not None:
        faces.append(effect.this)
    identity = player.GetIdentity()
    if identity is not None:
        faces.append(identity)
    for f in Worlds.FindCardsOnField(effect, set_name="Gwenpool"):
        if f.GetControlBy() == player:
            faces.append(f)
    # Carte attachée à Unbelievable Gwenpool (ses bulles sont utilisables).
    ug = Worlds.FindCardOnField(effect, name="Unbelievable Gwenpool", card_type=Upgrade)
    if ug:
        faces.extend(ug.GetInventoryDeck().FindCards())
    vus, uniques = set(), []
    for f in faces:
        if id(f) not in vus:
            vus.add(id(f))
            uniques.append(f)
    return uniques


def ResolveBlank(effect: 'Effect', count: int = 1) -> None:
    """Résout `count` blancs « ____ » via Medium Awareness (gp001a)."""
    player = effect.GetInitiator()

    for _ in range(count):
        # Rules of the Universe : remplacement forcé par la bulle d'Evil Gwenpool.
        if Worlds.FindCardsOnField(effect, name="Rules of the Universe"):
            hero = player.GetHero()
            effect.this.DealDamage([hero], 1, effect)
            continue

        # THE END : bulles interdites, le blanc reste sans effet.
        if Worlds.FindCardsOnField(effect, name="THE END", card_type=Obligation):
            continue

        utilisees = _bulles_utilisees(effect)
        options = []
        for face in _sources_de_bulles(effect, player):
            cid = face.paper.card_id
            for idx, (libelle, operation) in enumerate(BULLES.get(cid, [])):
                cle = (id(face), idx)
                if cle in utilisees:
                    continue

                def fabriquer(face=face, cle=cle, operation=operation):
                    def choisir(targets):
                        if not utilisees:
                            RunAt.TheEndOfThePhase(effect, utilisees.clear)
                        utilisees.add(cle)
                        operation(effect, player, face)
                    return choisir

                options.append(AbilityFactory.ForChoiceAbility(libelle, fabriquer()))

        if options:
            player.MayChooseOneAbility(effect, *options)


################################################################################
# Suivi « le Méchant a intrigué la manche dernière » (pour gp003).

def NoterVillainScheme(effect: 'Effect') -> None:
    w = effect.world
    s = getattr(w, '_gwenpool_manches_intrigue', None)
    if s is None:
        s = set()
        setattr(w, '_gwenpool_manches_intrigue', s)
    s.add(w.round_id)


def VillainSchemedLastRound(effect: 'Effect') -> bool:
    s = getattr(effect.world, '_gwenpool_manches_intrigue', None)
    if not s:
        return False
    return (effect.world.round_id - 1) in s
