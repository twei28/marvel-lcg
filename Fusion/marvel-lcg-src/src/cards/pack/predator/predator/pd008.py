from . import *

# Jungle Stalk — EVENEMENT, cout 0, [mental]. TACTIC.
# Hero Action: Find a minion and put it into play engaged with you → heal damage from your hero for each icon (★ and Y) in
#   that card's boost area and give Predator a cloaked status card.
#
# Cartes de reference :
#  - `br011` Hammer Time (pack beta_ray_bill) : « search ... for a minion and put it into play engaged with you → ... » : la
#    carte convoque un sbire (COUT, fleche), puis agit sur lui ; ici `Find.Find` (regle « Find » du 23/10/2026).
#  - `core/01051` : `this.HealthUnits(unites, n, effect)` pour soigner.
#  - `FacesCounter.CountTotalBoostIcons` / `CountTotalBoostStar` (15004, ho014) : les icones du cadre de boost.
#
# ⚠ Mots-pieges :
#  - « each icon (★ AND Y) in THAT card's boost area » : icones de boost ordinaires + icone a etoile du sbire convoque.
#  - « heal damage FROM YOUR HERO » : le HEROS du joueur (pas un allie, pas l'identite alter-ego) : 1 PV par icone.
#  - « AND give Predator a cloaked status card » : meme si 0 PV soigne ; une seule Cloaked par personnage.
#  - « Find a minion » est un COUT (fleche) : sans sbire a trouver, rien ne se passe (pas de Cloaked).


def GetAbilities() -> Sequence['Ability']:

    def traque(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        sbire = TrouverUnSbire(effect, joueur)
        if sbire is None:
            return
        icones = IconesDeBoost(sbire)
        if icones > 0:
            this.HealthUnits([joueur.GetHero()], icones, effect)
        Camoufler(effect, joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            traque,
        ).SetPlay().SetLabel(),
    ]
