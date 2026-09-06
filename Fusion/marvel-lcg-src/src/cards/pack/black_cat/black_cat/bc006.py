from . import *

# Lucky Hit — EVENEMENT, cout 1, [physical]. ATTACK. SUPERPOWER. x2.
# Hero Action (attack): Discard the top 2 cards of the encounter deck and deal
#   1 damage to an enemy for each icon ([star] and [boost]) discarded this way.
#   Tuck one of those cards under Black Cat.
#
# CARTES DE REFERENCE
#  - `15004` / `ho014` : `Worlds.DiscardEncounterTopCard`, qui rend la carte
#    defaussee.
#  - `bc005` : la meme economie, cote contre.
#
# TEXTE CONTRE CODE
#  ⚠ PAS DE FLECHE : defausser n'est pas un cout, c'est le debut de l'effet.
#    Deck de rencontre vide, la carte reste jouable et inflige 0 degat.
#  ⚠ « DISCARD the top 2 » et non « look at » : les deux cartes partent, on ne
#    choisit pas lesquelles. C'est la difference avec `bc005`.
#  ⚠ « for each icon DISCARDED THIS WAY » -> le total des DEUX cartes, pas de
#    la meilleure.
#  ⚠ « each icon ([star] AND [boost]) » -> `IconesEtEtoiles`.
#  ⚠ ON COMPTE AVANT DE DEFAUSSER — impossible ici, `DiscardEncounterTopCard`
#    defausse ET rend la carte d'un seul geste. On compte donc APRES, sur des
#    cartes qui sont en defausse de rencontre. `CountBoostIconsInternal`
#    (has_boost_icon.py:36) envoie alors `WhenBoostIconsWouldBeCount`, ce qui
#    OUVRE LA PORTE A `bc001a` Tychokinesis : la joueuse peut substituer une
#    carte glissee au comptage. Ce n'est pas un defaut, c'est la combinaison
#    que le pack cherche — et c'est ecrit ici pour qu'un futur lecteur ne
#    « corrige » pas l'ordre.
#  ⚠ « Tuck ONE OF THOSE CARDS » -> une des deux defaussees, au choix de la
#    joueuse. Pas les deux, et pas une carte prise ailleurs.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_chance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)

        defaussees: List['CardFace'] = []
        for _ in range(2):
            face = Worlds.DiscardEncounterTopCard(effect)
            if face is not None:
                defaussees.append(face)

        degats = IconesEtEtoiles(defaussees)
        if degats > 0:
            this.DealDamage(effect.targets, degats, effect)

        if defaussees and joueur is not None:
            choisie = joueur.AskChooseFaces(
                defaussees, (1, 1), effect,
                prompt="Tuck one of those cards under Black Cat")
            if choisie:
                GlisserSousIdentite(effect, list(choisie), joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            coup_de_chance,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
