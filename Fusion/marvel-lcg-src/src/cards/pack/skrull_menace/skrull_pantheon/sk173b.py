from . import *

# Protect the Pantheon 1B (173B) — complot principal, face B. Menace 9[per_hero], depart 6[per_hero],
# escalade +1[per_hero]. (La face A, sk173a, n'a pas de capacite : « Contents » et « Setup », le
# scenario met l'environnement de cote par son `set_aside`.)
# Forced Interrupt: When the last threat is removed from this scheme, put the set-aside Skrull
#   Pantheon environment into play, DESTROYED side faceup. Advance to stage 2B.
# When Completed: Put the set-aside Skrull Pantheon environment into play, STRONGHOLD side faceup.
#   Advance to stage 2A.
#
# Cartes de reference :
#  - **`web_of_deceit/wd055b`** Chasing Down The Lizard 1B : `WhenLastThreatRemoveFromThisScheme(
#    ForcedInterrupt, ...)` + `this.Advance("2A", effect)` ; **`mut_gen/mansion_attack`** et
#    **`mut_gen/sabretooth/32064b`** : `WhenMainSchemeStageCompleted(WhenCompleted, "This", ...)`.
#  - Mise en jeu d'une carte mise de cote : `face.PutIntoPlay(joueur, effect)` (modele sk145a) ;
#    retournement : `card.Flip` (modele `fne/typhoid_mary/60112`).
#
# ⚠ Mots-pieges : « the LAST threat is removed » (derniere menace RETIREE, pas « complot a 0 au depart » ;
# le complot demarre a 6[per_hero]) ; « Advance to stage 2B » (la face B directement, SANS passer par la
# face A, donc sans la recherche de Strengthen the Faith) contre « Advance to stage 2A » (le chemin
# normal : face A puis face B) ; « DESTROYED » = face B de l'environnement, « STRONGHOLD » = face A ;
# « set-aside » : l'environnement vient de la zone mise de cote ; « When Completed » = menace >= 9[per_hero],
# avant l'avance normale du moteur.


def GetAbilities() -> Sequence['Ability']:

    def derniere_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        Unused(message)
        this = effect.this.CastTo(MainScheme)
        MettreLEnvironnementEnJeu(effect, detruit=True)
        AvancerAuStade2FaceB(effect, this)

    def accompli(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        Unused(message)
        MettreLEnvironnementEnJeu(effect, detruit=False)
        # L'avance au stade 2A est celle du moteur (`MainScheme.PlaceThreatInternal`, juste apres).

    return [
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, derniere_menace),
        AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.WhenCompleted, "This", accompli),
    ]
