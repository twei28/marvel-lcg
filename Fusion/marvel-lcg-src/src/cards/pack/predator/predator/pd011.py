from . import *

# * Self Destruct — AMELIORATION, cout 2, [energy][energy]. TECH. WEAPON.
# Hero Action: Exhaust this card → place 2 glyph counters here.
# Hero Action: Remove this card from the game → deal 1 damage to the villain and each minion engaged with you (to a maximum
#   of 10) for each glyph counter here.
#
# Cartes de reference :
#  - `Faces.PlaceCountersOn([this], n, 'glyph', effect)` (compteur `glyph` ajoute a l'enum `COUNTER`, 25/10/2026) ;
#    `CostFunc.Exhaust("This")` pour « Exhaust this card → » (`core/01051`, tr009 Raphael pour un cout qui lit un compteur).
#  - `CostFunc.RemoveFromGame("This")` : « Remove this card from the game → ». ⚠ Il retire la carte AVANT l'effet : le nombre de
#    glyphes doit etre lu dans le cout, donc un `CostFunc.Custom` qui memorise le compteur sur l'effet PUIS retire la carte.
#  - `this.DealDamage(unites, n, effect)` (`core/01051`), `player.GetEngagedMinions()` (ra002).
#
# ⚠ Mots-pieges :
#  - « each minion engaged WITH YOU » : les sbires engages avec le joueur qui joue, pas ceux des autres joueurs.
#  - « (to a maximum of 10) » : ARBITRAGE PROVISOIRE (25/10/2026) = plafond de 10 glyphes comptes, soit 10 degats au plus par
#    cible (1 degat par glyphe). Question posee a l'auteur (QUESTIONS-AUTEUR.md) : ces lectures donnent le meme resultat par cible.
#  - « for EACH glyph counter » : 1 degat par glyphe, au vilain ET a chaque sbire engage.
#  - Les deux Actions sont distinctes : l'une incline (chargement), l'autre detruit l'objet ; aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def charger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.PlaceCountersOn([this], 2, 'glyph', effect)

    def memoriser_et_retirer(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        this = effect.this.CastTo(Upgrade)
        effect._pd_glyphes = this.GetCounters('glyph')  # type: ignore
        return Faces.RemoveAllFromGame([this], effect) == [this]

    def detruire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        glyphes = min(int(getattr(effect, "_pd_glyphes", 0)), 10)
        joueur = JoueurDeCetteCarte(effect) or effect.GetInitiator()
        if glyphes <= 0 or joueur is None:
            return
        cibles = [Worlds.FindVillain(effect)] + list(joueur.GetEngagedMinions())
        this.DealDamage([c for c in cibles if c is not None], glyphes, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            charger,
        ).SetCostFunc(CostFunc.Exhaust("This")).SetName("Charge"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            detruire,
        ).SetCostFunc(CostFunc.Custom(None, memoriser_et_retirer)).SetName("Self Destruct"),
    ]
