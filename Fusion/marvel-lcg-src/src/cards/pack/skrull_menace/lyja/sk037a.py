from . import *

# * Lyja (face HEROS) — FANTASTIC FOUR. SKRULL. THW 2, ATK 1, DEF 2, main 5, 10 PV.
# Skrull Spy — Action: Spend up to 1[per_hero] resources of any type → search the
#   encounter deck for a TREACHERY card for each resource spent this way, shuffle
#   the encounter deck, and place those cards on the top of the encounter deck in
#   any order.
#
# Cartes de reference :
#  - **`16093`** Nebula's Ship : « spend up to 2 resources » = `SetCost(Cost("2",
#    up_to=True))`, le nombre depense se lit par `effect.GetPaidResources().val`.
#  - **`SetCost(<fonction>)`** (ability.py:346) : le cout peut etre une fonction de
#    l'effet ; c'est la voie pour « 1[per_hero] » (le nombre de joueurs n'est connu
#    qu'a la partie).
#  - **`40004`** Precognition / **`hd001b`** : `PlaceOnTopInAnyOrder` pour l'ordre.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « up to 1[per_hero] » : 1 par HEROS (donc par joueur), de zero a N ressources.
#  - « of any type » : cout generique (Cost("N")), n'importe quelle couleur.
#  - « for EACH resource spent » : une carte par ressource, dans la limite des
#    traitrises que le deck contient.
#  - « shuffle ... and place on top » : l'ORDRE compte, melange AVANT la pose.
#  - « TREACHERY card » : type Treachery OU trait TREACHERY (decision du 15/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def cout_par_joueur(effect: 'Effect', targets: Sequence['CardFace']) -> 'Cost':
        # « up to 1[per_hero] » : au plus un nombre de ressources egal au nombre de heros.
        n = Worlds.ConvertPerPlayerIconToInt("1*", effect)
        return Cost.FromText(str(max(1, min(4, n))), up_to=True)

    def espionne_skrull(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        joueur = effect.GetInitiator()
        # Le cout « up to » est verifie par le moteur (`Resources.IsMatchCost`, resources.py:97) :
        # jamais plus de 1[per_hero] ressources depensees.
        depense = effect.GetPaidResources().val
        trouvees = ChercherTraitrisesRencontre(effect, joueur, depense)
        PoserSurLeDeckRencontre(effect, joueur, trouvees)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            espionne_skrull,
        ).SetName("Skrull Spy")
        .SetCost(cout_par_joueur),
    ]
