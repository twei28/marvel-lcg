from . import *

# Portal to Hell — MANIGANCE ANNEXE NEMESIS. 2 menaces, 3 boost, 1 crise,
#   Hinder 1 par joueur.
# When Revealed: Find Demonic Limbs attachment and reveal it.
#
# MOTS-CLES : HINDER et CRISIS — fiches lues avant d'ecrire, et les deux
# disent la meme chose : ce sont des BASES AUTOMATIQUES du moteur, lues dans
# `desc.Hinder` et `desc.Crisis`. AUCUN script ne doit les recoder. Hinder
# pose sa menace SUR CETTE CARTE, jamais sur le complot principal (piege
# nomme dans sa fiche), et le `1*` de `desc` signifie « par joueur ».
#
# CARTES DE REFERENCE
#  - `bk018` Timebroker et `dr012` Harness Violent Emotions : « find X and
#    reveal it » par `Search.SearchForCards` sur le deck de rencontre ET sa
#    defausse, puis `Reveal`.
#
# TEXTE CONTRE CODE
#  « FIND ... AND REVEAL IT » -> chercher NE SUFFIT PAS : sans le `Reveal`,
#    l'attachement resterait dans le deck et la manigance serait inoffensive.
#  ⚠ DEUX ZONES a fouiller, le deck de rencontre ET sa defausse : Demonic
#    Limbs peut deja etre passe une fois (le joueur l'a defausse en payant ses
#    deux energies), et c'est precisement le cas que cette carte existe pour
#    couvrir.
#  ⚠ AUCUNE CONDITION DE RETRAIT : la manigance reste en jeu tant qu'on ne la
#    contre pas, et sa crise bloque le retrait de menace sur le complot
#    principal. C'est voulu.


def GetAbilities() -> Sequence['Ability']:

    def ouvrir_le_portail(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(this, message)
        joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return
        faces = Search.SearchForCards(
            effect, joueur,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            name=NOM_MEMBRES,
        )
        if faces:
            faces[0].Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            ouvrir_le_portail,
        ),
    ]
