from . import *

# * Ego — SBIRE (Minion, type de base). ELITE. LIVING. PLANET. COSMIC.
# SCH 2, ATK 2, HP 12. Planet deck personnel (5/5) : entre en jeu par
# l'Action de pc001b (« put the top card of the planet deck into play »),
# jamais joue depuis la main -- type `Minion` simple, PAS `PlayerMinion`
# (qui n'ajoute que l'ability « jouable depuis la main », inutile ici et qui
# exigerait `Cost`/`RES` non imprimes sur cette carte, modele `pc003`
# Zenn-La/`pc007` Xandar qui restent eux aussi de simples `Support` sans
# cout).
#
# Texte imprime :
#  « Ego engages Silver Surfer. »
#  « Arrive: Deal 6 damage to Ego. »
#  « When Defeated: Put the set aside Ego The Living Planet ally into play
#    under your control. Remove this card from the game. »
#
# CARTES DE REFERENCE
#  - `minion.py:57` `Minion.OnPutIntoPlay` : engage DEJA automatiquement
#    `message.GetToPlayer()` des qu'un sbire est mis en jeu -- comportement
#    de BASE de n'importe quel sbire (pas reserve a `PlayerMinion`), donc
#    « Ego engages Silver Surfer » n'a besoin d'AUCUN code supplementaire :
#    `PutIntoPlay(joueur, effect, under_control=True)` (pc001b.py) suffit.
#  - `bf031` Faith (buffy_hellmouth) : `AbilityFactory.WhenUnitBeDefeated
#    (WhenDefeated, "This", op)` + `Search.SearchForCard(effect, joueur,
#    include_set_aside=True, card_type=Ally, name=...)` +
#    `allie.PutIntoPlay(joueur, effect, under_control=True)` -- modele EXACT
#    pour « When Defeated: put the set aside ... ally into play ».
#  - `desc.Linked` sur `pc018` (Ego The Living Planet) : cree l'allie dans
#    `world.aside_deck` des que CETTE carte (Ego, pc017) est fabriquee,
#    fiche docs/reference/mots-cles/linked.md.
#
# TEXTE CONTRE CODE
#  « Ego engages Silver Surfer » : automatique a l'entree en jeu sous
#    controle du joueur, rien a coder de plus.
#  « Arrive: deal 6 damage to EGO » : a LUI-MEME (6 des 12 PV), pas a un
#    autre personnage.
#  « the set-aside Ego The Living Planet ALLY » : filtre `Ally` + nom exact,
#    jamais le sbire homonyme lui-meme.
#  « Remove this card from the game » : `Faces.RemoveAllFromGame`, pas une
#    simple defausse (la carte ne doit plus jamais reapparaitre).


def GetAbilities() -> Sequence['Ability']:

    def arrivee(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        this.DealDamage([this], 6, effect)

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = message.GetKillerPlayer() or Worlds.GetFirstPlayer(effect)
        allie = Search.SearchForCard(
            effect, joueur,
            include_set_aside=True,
            card_type=Ally,
            name="Ego The Living Planet",
        )
        if allie:
            allie.PutIntoPlay(joueur, effect, under_control=True)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            arrivee,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite,
        ),
    ]
