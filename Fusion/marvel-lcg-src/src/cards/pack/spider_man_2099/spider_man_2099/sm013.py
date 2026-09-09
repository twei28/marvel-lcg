from . import *

# Future in Crisis — OBLIGATION. Boost 2. Icones Acceleration 1 et Crisis 1.
# Give to the Miguel O'Hara player.
# Action: Exhaust your identity -> remove Future in Crisis from the game.
#
# CARTES DE REFERENCE
#  - `an010`, `ho013` : « Give to the X player » =
#    `WhenThisObligationGiveToYou(op)` cote script, `desc.GiveTo` cote donnees.
#  - `bl011` The Thirst (meme auteur) : une obligation qui RESTE EN JEU apres
#    sa revelation, au lieu de se resoudre puis partir.
#  - `CostFunc.Exhaust("YourIdentity")` (RECETTES §5) pour « exhaust your
#    identity → ».
#  - `an010` Banished from Asgard : LA carte modele, qui porte mot pour mot
#    « Exhaust <identite> → remove <cette obligation> from the game » —
#    `Faces.RemoveAllFromGame([this], effect)` + `CostFunc.Exhaust(
#    "YourIdentity")`. ⚠ `Faces.RemoveFromGame` (au singulier) N'EXISTE PAS ;
#    `CostFunc.RemoveFromGame` existe mais c'est un COUT, pas un effet.
#
# TEXTE CONTRE CODE
#  ⚠⚠ CETTE OBLIGATION N'A AUCUN EFFET « When Revealed », ET C'EST LE PIEGE.
#    Ce qu'elle fait, elle le fait en RESTANT EN JEU : ses deux icones. C'est
#    pour cela que la carte offre une Action pour s'en debarrasser — sans
#    quoi il n'y aurait rien a « retirer du jeu ».
#  ⚠ LES DEUX ICONES SONT DES BASES AUTOMATIQUES (RECETTES §3) : `Acceleration`
#    et `Crisis` sont lues dans `desc` par le moteur, AUCUN script ne doit les
#    coder. Elles ont ete identifiees par comparaison d'image contre `ag011`,
#    temoin Acceleration du depot, le 08/09/2026 — jamais a vue (lecon
#    Lockjaw). Consequence en jeu, et elle est lourde : tant que la carte est
#    la, +1 menace sur le complot principal au debut de chaque phase vilain,
#    ET impossible de retirer la moindre menace du complot principal.
#  ⚠ HOMONYMIE DANGEREUSE : cette carte porte l'ICONE `Acceleration`, tandis
#    que le heros du meme pack porte une CAPACITE nommee « Acceleration » qui
#    n'a rien a voir (fiches `acceleration.md` et `acceleration-2099.md`). Ne
#    pas melanger les deux en lisant ce pack.
#  ⚠ « Action », pas « Hero Action » ni « Alter-Ego Action » : les deux formes
#    peuvent s'en debarrasser.
#  ⚠ « exhaust YOUR IDENTITY » : le cout incline l'identite, pas l'obligation.
#    Une identite deja inclinee ne peut donc pas payer.
#  ⚠ « REMOVE FROM THE GAME », pas « discard » : la carte ne revient pas dans
#    le deck rencontre et ne peut plus etre revelee (piege `defeated` vs
#    `damaged` de la meme famille : ne jamais coder l'un pour l'autre).
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.
#
# ⚠⚠ A VERIFIER EN PARTIE REELLE, ET CE N'EST PAS UN DETAIL : cette obligation
#    n'a AUCUN effet « When Revealed ». Il faut donc s'assurer que le moteur la
#    laisse EN JEU au lieu de la defausser aussitot revelee — sans quoi ses
#    deux icones ne s'appliqueraient jamais et l'Action n'aurait plus rien a
#    retirer. Temoin le plus proche : `bl011` The Thirst (meme auteur), qui
#    reste en jeu, mais elle porte une Interruption Forcee et des compteurs.
#    Si le moteur la defausse, le correctif est cote donnees, pas ici.


def GetAbilities() -> Sequence['Ability']:

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            retirer,
        ).SetName("Future in Crisis")
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
