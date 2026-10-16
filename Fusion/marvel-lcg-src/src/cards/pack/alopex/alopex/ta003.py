from . import *

# Bold Strategy (x3) — EVENEMENT, cout 1, [mental]. TACTIC.
# Hero Action: Cloak Alopex. You may spend up to 3 [mental] resources to daze
#   an enemy for each [mental] resource spent this way.
#
# Cartes de reference :
#  - « Cloak X » : `td005` Improvised Tactics / fiche mots-cles/cloak.md :
#    `Faces.GiveStatus([cible], "Cloaked", effect)` ;
#  - « Daze X » : fiche mots-cles/daze.md, meme mecanique avec la carte d'etat
#    « Dazed » : `Faces.GiveStatus([ennemi], "Dazed", effect)` ;
#  - « spend up to N resources » : `dt107` Zenpool (`AskSpendResourcesInternal`
#    dans le corps) + `26022` Machine Man (`Cost(..., up_to=True)`) ;
#  - choix d'un ennemi : `tl013` (`joueur.AskChooseFace`).
#
# Mots-pieges :
#  - « Cloak ALOPEX » : l'identite (face heros, l'action est une Hero Action) ;
#    TOUJOURS, avant et sans rapport avec la depense facultative ;
#  - « You MAY spend UP TO 3 [MENTAL] » : 0 a 3, ressources [mental] (ou wild) ;
#  - « daze AN enemy FOR EACH resource » : un ennemi PAR ressource, choisi
#    chaque fois par le joueur (un meme ennemi ne porte qu'un Dazed : on ne
#    propose que les ennemis pas deja Dazed) ;
#  - pas de label (« Hero Action » nue, pas une attaque ni un contre).


def GetAbilities() -> Sequence['Ability']:

    def bold_strategy(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Cloaked", effect)

        depenses = RessourcesMentalesDepensees(joueur, effect, 3)
        for _ in range(depenses):
            ennemis = [f for f in Worlds.GetOnFieldEnemies(effect)
                       if not f.IsDefeated() and not f.IsDazed()]
            if not ennemis:
                break
            choisi = joueur.AskChooseFace(ennemis, effect, prompt="Daze an enemy")
            Faces.GiveStatus([choisi or ennemis[0]], "Dazed", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            bold_strategy,
        ).SetPlay(),
    ]
