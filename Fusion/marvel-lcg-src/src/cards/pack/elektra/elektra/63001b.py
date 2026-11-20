from . import *

# * Elektra Natchios — ALTER-EGO. REC 3, main 6, 9 PV. ASSASSIN.
# Elektra Natchios begins the game with a NINJA deck. (See insert.)
# Ninja Training — Interrupt: When you change to hero form, shuffle the top card of the NINJA deck into the
#   encounter deck.
#
# CARTES DE REFERENCE
#  - « begins the game with a deck » : `fne/daredevil/60001b.py` (deck Sense) : `BeginGameWithSetAside([...ids])` met
#    les cartes dans `set_aside_deck` (= `additional_discard_pile`), puis on les pose face cachee dans
#    `additional_deck` et on melange. Meme alter-ego, meme besoin d'un paquet annexe consultable.
#  - « Interrupt: When you change to hero form » : `ares/ares/ar001b.py` (`WhenUnitWouldChangeForm(Interrupt, "You")`),
#    avec `to_form=Hero` : seul le passage civil -> heros declenche (la face alter-ego n'est active qu'a ce moment).
#
# TEXTE CONTRE CODE
#  ⚠ « shuffle the top card of the NINJA deck into the ENCOUNTER deck » : paquet de RENCONTRE (pas la main, pas la
#    defausse). Paquet Ninja vide : rien ne se passe (aucune carte a melanger).
#  ⚠ Les six cartes Ninja sont face cachee et le proprietaire peut les consulter (comme le deck Sense, rapport n°100).
#  Chiffres : six cartes (2 + 2 + 2), une seule carte melangee par passage en forme heros.


def GetAbilities() -> Sequence['Ability']:

    def avec_paquet_ninja(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        initiator = effect.GetInitiator()
        faces = list(initiator.set_aside_deck.Get())
        Faces.MoveAllTo(faces, initiator.additional_deck, effect)
        initiator.additional_deck.Shuffle(effect)
        for face in initiator.additional_deck.Get():
            face.FlipTo(effect, face_up=False)
            face.card.visible.Set(initiator)

    def formation_ninja(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        MelangerDessusNinja(joueur, effect)

    return [
        AbilityFactory.BeginGameWithSetAside([*NINJA_IDS], avec_paquet_ninja),
        AbilityFactory.WhenUnitWouldChangeForm(
            AbilityType.Interrupt,
            "You",
            formation_ninja,
            to_form=Hero,
        ).SetName("Ninja Training"),
    ]
