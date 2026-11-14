from . import *

# We've Got This : EVENEMENT, cout 3, [physical]. ATTACK. DUPLICATE. SUPERPOWER. (mm008 et mm009 : deux exemplaires)
# Hero Action (attack): Deal 4 damage to an enemy. Then, choose a player and deal 1 damage to the villain and each enemy engaged with that player for each Dupe ally in play.
#
# CARTES DE REFERENCE : `ca012` (Chomp : `this.DealDamage(effect.targets, n, effect, property=AttackProperty(..))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)`).
# TEXTE CONTRE CODE : « Then, choose a player » : le joueur choisit lui-meme en multijoueur (un seul joueur : lui). « the villain AND each enemy engaged with that player » : le vilain + les sbires
#  engages avec ce joueur ; 1 degat PAR Dupe en jeu, EN PLUS pour chacun (donc N degats a chaque cible). Ces degats ne sont PAS une attaque. Chiffres : cout 3, 4 degats.


def GetAbilities() -> Sequence['Ability']:

    def weve(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        this.DealDamage(effect.targets, 4, effect, property=AttackProperty())
        if joueur is None:
            return
        nombre = len(DupesEnJeu(effect))
        if nombre <= 0:
            return
        joueurs = list(effect.world.const_players)
        choisi = joueur
        if len(joueurs) > 1:
            choisi = joueur.AskChooseOneText(joueurs, [j.GetIdentity().paper.name.lstrip("* ") for j in joueurs], "Choose a player")
        cibles = []
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain is not None:
            cibles.append(vilain)
        for f in Worlds.GetOnFieldEnemies(effect):
            if Minion.IsType(f) and f.IsInPlay() and f.CastTo(Minion).engaged_player is choisi and f not in cibles:
                cibles.append(f)
        if cibles:
            this.DealDamage(cibles, nombre, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            weve,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
