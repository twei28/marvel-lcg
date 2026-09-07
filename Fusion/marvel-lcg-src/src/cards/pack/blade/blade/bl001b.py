from . import *

# * Eric Brooks — ALTER-EGO. VAMPIRE. REC 4 — main 6 / 12 PV.
# Slayer — Setup: Shuffle each card in your nemesis set other than Dracula into
#   the encounter deck.
# Serum Injection — Action: Spend a [physical] resource -> place 2 blood
#   counters on Eric Brooks. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `an001b` Aldrif / `ok001b` Okoye : `WhenCardSetup("This", op)`, resolu a
#    l'etape 16 de la mise en place (world.py:597), donc APRES la construction
#    et le melange du deck rencontre.
#  - `01190` Shadow of the Past : la pile `player.set_aside_nemesis_sets` et
#    `Faces.ShuffleAllTo(faces, Worlds.GetEncounterDeck(effect), effect)`.
#  - `39048` Bandolier of Stakes (Mojo) : `Cost("1")` ; ici `Cost("R")`, la
#    lettre impose la couleur physique (element/cost.py:35).
#  - `23001a` War Machine : `Faces.PlaceCountersOn([identite], n, 'ammo')`.
#
# TEXTE CONTRE CODE
#  ⚠ « other than DRACULA » -> filtre par NOM, sans l'etoile (paper.py la
#    retire). Aucun homonyme au depot. Blood Hunt, les deux Vampires, le
#    Bandolier, les deux Embraced et Turned partent dans le deck rencontre ;
#    Shadow of the Past ne trouvera plus que Dracula dans la pile.
#  ⚠ « Spend a [physical] resource » -> `CostFunc.Spend(Cost("R"))`, pas
#    n'importe quelle icone.
#  ⚠ « Action » sur la face ALTER-EGO -> forme civile de fait (la face heros
#    ne porte pas cette capacite). `AbilityType.Action` comme ar001a.
#  ⚠ Les pions vont sur l'IDENTITE : Blade les depensera apres le changement de
#    forme (cas de test dedie).


def GetAbilities() -> Sequence['Ability']:

    def slayer(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)
        joueur = this.GetControlByPlayer()
        if not EstJoueur(joueur):
            return
        pile = getattr(joueur, "set_aside_nemesis_sets", None)
        if pile is None:
            return
        faces = [f for f in list(pile.Get()) if f is not None and not f.IsName(NOM_DRACULA)]
        if not faces:
            return
        Faces.ShuffleAllTo(faces, Worlds.GetEncounterDeck(effect), effect)

    def serum_injection(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)
        Faces.PlaceCountersOn([this], 2, COMPTEUR_SANG, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            slayer,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            serum_injection,
        ).SetName("Serum Injection")
        .SetCostFunc(CostFunc.Spend(Cost("R")))
        .LimitOncePerRound(),
    ]
