from . import *

# Samurai — PATH (la Voie du Samourai), classe Bushido (Inkwire, TMNT Shinobi). BUSHIDO.
# Permanent. You get -1 hand size.
# Way of the Warrior — Hero Action: Exhaust this card and remove a total of 2 samurai counters from among
#   OATH upgrades you control -> ready your hero and draw 1 card.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; samurai counter / OATH (samurai-counter.md) ;
# Uses (uses.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « -1 hand size » : `sentinel/st005b` ;
#  - cout a compteurs d'une AUTRE carte : `jennika/tj006` Fearless Resolve (`CostFunc.Counter(..., 'samurai')`,
#    mais « ... from IT ») ; ici « from AMONG upgrades you control » : repartition libre, donc un cout
#    `CostFunc.Custom` dont le sélecteur ("This") porte la condition « au moins 2 compteurs samurai au total »
#    (meme montage que `CostFunc.LookAtDeck`, qui teste une condition globale par `check_effect_fn`) ;
#  - « ready your hero and draw 1 card » : `Faces.ReadyAll([hero])` (jennika/tj006) + `DrawUp(1)`.
#
# TEXTE CONTRE CODE
#  ⚠ « remove a TOTAL of 2 samurai counters FROM AMONG OATH upgrades YOU CONTROL » : 2 compteurs au plus
#    repartis librement entre toutes les ameliorations OATH sous SON controle (pas celles des autres joueurs,
#    pas d'autre trait) ; le joueur choisit sur quelle amelioration prendre chacun des deux.
#  ⚠ « Exhaust this card AND remove ... » : DEUX couts, tous deux obligatoires.
#  ⚠ « ready YOUR HERO » (et non l'identite) ; « AND draw 1 card » : les deux effets, sans condition (le heros
#    peut deja etre pret).
#  ⚠ Le livret ajoute « once per turn » : l'inclinaison de la carte realise cette limite (la Voie ne se
#    redresse qu'a la fin de la phase des joueurs) ; aucune limite imprimee sur la carte.
#  ⚠ Une amelioration OATH qui perd son dernier compteur est defaussee (Uses).


def GetAbilities() -> Sequence['Ability']:

    def oaths_avec_compteurs(effect: 'Effect') -> List['CardFace']:
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return [f for f in joueur.GetControlUpgrade(CardFinder(trait="OATH"))  # type: ignore
                if f.GetCounters('samurai') > 0]

    def assez_de_compteurs(effect: 'Effect', face: 'CardFace') -> bool:
        Unused(face)
        return sum(f.GetCounters('samurai') for f in oaths_avec_compteurs(effect)) >= 2

    def retirer_deux_compteurs(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        for _ in range(2):
            candidats = oaths_avec_compteurs(effect)
            if not candidats:
                return False
            if len(candidats) == 1:
                cible = candidats[0]
            else:
                choisies = joueur.AskChooseFaces(candidats, (1, 1), effect, prompt="Remove a samurai counter")
                if not choisies:
                    return False
                cible = choisies[0]
            if not Faces.RemoveCountersOn([cible], 1, 'samurai', effect):
                return False
        return True

    def way_of_the_warrior(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        Faces.ReadyAll([joueur.GetHero()], effect)
        joueur.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            way_of_the_warrior,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(
            Select.From("This", finder=CardFinder(check_effect_fn=assez_de_compteurs)),
            retirer_deux_compteurs,
        )),
    ]
