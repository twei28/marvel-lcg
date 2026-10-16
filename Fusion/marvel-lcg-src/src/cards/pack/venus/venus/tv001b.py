from . import *

# * Bonnie (face alter-ego) — TEENAGER. MUTANT. TURTLE. PV 10, REC 4, main 6.
# Setup: Discard cards from the top of your deck until you discard an [[ELEMENT]]
#   upgrade. Put that card into play.
# Action: Remove 1 dredge counter from Bonnie -> heal 2 damage from a friendly
#   character. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - Setup : `tm001b` Mikey (`WhenCardSetup("This", op)` sur une face d'identite) pour
#    l'accroche, et `br009` / `docs/reference/mots-cles/seek.md` pour « discard cards
#    from the top of your deck until you discard X » (`Player.DiscardDeckUntil`).
#  - Action : `ra001b` Jane Foster (`AlterEgoAction`, `SetTarget(Friend, canbe_heal=True)`,
#    `HealthUnits`, `LimitOncePerRound()`) ; cout en compteurs `tr013` (`CostFunc.Counter(
#    "YourIdentity", n, ...)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Setup » = capacite de MISE EN PLACE du personnage, pas le mot-cle `desc.Setup`
#    des cartes de rencontre : `WhenCardSetup`. Elle part APRES la pioche de depart.
#  ⚠ « until you discard AN [[ELEMENT]] UPGRADE » -> `DefausserJusquA(card_type=Upgrade,
#    verifier=ELEMENT)` : la carte trouvee est DEFAUSSEE puis MISE EN JEU (pas payee),
#    les cartes traversees restent en defausse. Deck sans ELEMENT : tout est defausse,
#    rien n'entre en jeu.
#  ⚠ « Remove 1 dredge counter from BONNIE -> » : FLECHE = COUT (retire avant le soin),
#    sur l'IDENTITE (la face Bonnie est la carte d'identite).
#  ⚠ « heal 2 damage from a FRIENDLY character » -> `Friend` (heros / allies / identite),
#    jamais un sbire ; une cible blessee (`canbe_heal`).
#  ⚠ « Limit once per round » -> `LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = DefausserJusquA(
            effect, joueur, card_type=Upgrade,
            verifier=lambda f: f.HasTrait(TRAIT_ELEMENT))
        if face is not None:
            face.CastTo(Upgrade).PutIntoPlay(joueur, effect)

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)
        cibles = [t for t in effect.targets if t is not None]
        if cibles:
            this.HealthUnits(cibles, 2, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            soigner,
        ).SetTarget(Friend, canbe_heal=True)
        .SetCostFunc(CostFunc.Counter("YourIdentity", 1, DREDGE))
        .LimitOncePerRound(),
    ]
