from . import *

# Arc Nova — EVENEMENT, cout 2, [wild]. ATTACK. SUPERPOWER. x1.
# Hero Action (attack): Remove X dredge counters from Venus -> deal 4 damage to X enemies.
#
# CARTES DE REFERENCE
#  - `kb001a` / `16006` (We Are Groot) : X choisi par le joueur via `DeclareNumber` ;
#    `tg003` Great Courage : choix de plusieurs cibles dans le corps par `AskChooseFaces`.
#  - `td006` Singularity : degats d'un evenement d'attaque par `heros.DealDamage`.
#
# TEXTE CONTRE CODE
#  ⚠ « X » est CHOISI par le joueur, ZERO COMPRIS (un X nul est legal, il ne fait que
#    gaspiller la carte) : un `CostFunc.Counter` a minimum 1 le refuserait, et retirer
#    0 compteur echoue dans le moteur. Le retrait est donc fait ICI, a la main, AVANT
#    les degats (« -> » = cout), apres `DeclareNumber(0, compteurs)`.
#  ⚠ « 4 damage to X ENEMIES » -> X ennemis DISTINCTS au choix (villain ET sbires), 4 degats
#    chacun ; moins d'ennemis que X = tous les ennemis (les compteurs en trop sont perdus).
#  ⚠ « Venus » = l'identite : les compteurs sont retires de l'identite.
#  Evenement `Hero Action (attack)` : `SetLabel('attack')`.


def GetAbilities() -> Sequence['Ability']:

    def arc_nova(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if joueur is None or identite is None:
            return
        disponibles = Dragage(identite)
        if disponibles <= 0:
            return
        x = joueur.DeclareNumber(0, disponibles)
        if x <= 0:
            return
        Faces.RemoveCountersOn([identite], x, DREDGE, effect)
        ennemis = [f for f in Worlds.FindCardsOnField(effect, CardFinder(card_type=Enemy))
                   if f is not None and f.card.IsOnField()]
        nombre = min(x, len(ennemis))
        if nombre <= 0:
            return
        choisis = joueur.AskChooseFaces(ennemis, (nombre, nombre), effect,
                                        prompt="Arc Nova: choose %d enem%s" % (nombre, "y" if nombre == 1 else "ies"))
        heros = joueur.GetHero() or identite
        heros.DealDamage([c for c in choisis if c is not None], 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            arc_nova,
        ).SetPlay().SetLabel('attack'),
    ]
