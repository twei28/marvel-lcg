from . import *

# Inspection of the Vault — OBLIGATION. « Give to the first player. »
# Alter-Ego Action: Exhaust your identity and spend a [mental] resource → set this card aside, out of play.
#
# Cartes de reference :
#  - « Give to the first player » : `desc.GiveTo = ""` (modele 04163 Zola's Algorithm) : l'obligation va au joueur a qui elle est REVELEE ; ses deux
#    seules sources (vt017b et vt034) la revelent toujours au PREMIER JOUEUR. `"first player"` ne marche pas : `Worlds.FindPlayerByName` le
#    cherche comme un NOM de joueur, ne trouve rien et RETIRE l'obligation de la partie.
#  - « Exhaust your identity and spend a [mental] resource → set this card aside » : `WhenInYourPlayTurn(AlterEgoAction, ...)`
#    + `.SetCost(Cost("B"))` + `.SetCostFunc(CostFunc.Exhaust("YourIdentity"))` (modele 04163 Zola's Algorithm, qui DEFAUSSE) ;
#    `Faces.SetAside([this], effect)` (modele ta011 Prey : de cote, hors jeu, et NON defaussee : Riot in the Vault et
#    l'interruption de vt017b la retrouveront).
#
# ⚠ Mots-pieges : « [mental] » = `Cost("B")` (icone « noeuds relies » du scan, verifiee sur le glyphe M de ChampionsIcons.ttf) ;
# « set aside » != « discard » ; « Alter-Ego Action » : utilisable seulement en forme alter-ego du joueur qui la porte ;
# la carte n'a AUCUNE autre capacite : elle sert de DRAPEAU (« if Inspection is in play ») aux cartes de rencontre.


def GetAbilities() -> Sequence['Ability']:

    def mettre_de_cote(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        Faces.SetAside([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, mettre_de_cote)
        .SetCost(Cost("B"))
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
