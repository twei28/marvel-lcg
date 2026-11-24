from . import *

# * Rogue — SBIRE nemesis (Binary Nemesis 1/5). MNG 2, ATQ 2, PV 5. 2 icones de boost.
# BROTHERHOOD OF MUTANTS. ELITE.
# Forced Response: After the player phase begins, find Touched and attach it to
#   a character other than Rogue. If it is a friendly character, exhaust that
#   character.
# When Defeated: Discard Touched.
# (Binary's nemesis minion.)
#
# Cartes de reference :
#  - **`rogue/38001a`** * Rogue (heros officiel) : « Forced Response: After the
#    player phase begins, find Touched ... » = `AfterPhaseBegin(ForcedResponse,
#    "Player", op)` + `Find.Find(effect, name="Touched", ...)` + `AttachTo2`.
#  - choix entre plusieurs personnages par le PREMIER JOUEUR (`AskChooseFace`),
#    comme le fait `AttachToFaceWhenPutIntoPlay` pour une egalite (`Filter.One`).
#  - **`skrull_menace/new_revengers/sk163`** : `WhenUnitBeDefeated(WhenDefeated,
#    "This", op)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « AFTER the player phase begins » : a chaque round, tant que Rogue est en
#    jeu ; Reponse FORCEE, aucune question « voulez-vous ».
#  - « FIND Touched » : partout (en jeu, deck/defausse de rencontre, mise de
#    cote) ; deja attachee ailleurs, elle se DEPLACE (detachee puis attachee).
#  - « a character OTHER THAN Rogue » : identite, allie, vilain ou autre sbire.
#  - « If IT is a FRIENDLY character, exhaust THAT character » : le personnage
#    qui recoit Touched (identite ou allie), pas un autre ; un ennemi n'est pas
#    incline.
#  - « When Defeated: Discard Touched » : la carte Touched EN JEU part a la
#    defausse de rencontre ; si elle n'est pas en jeu (encore dans le deck), il
#    n'y a rien a defausser (lecture notee au gabarit).
#  - Les statistiques (MNG 2, ATQ 2, PV 5, boost 2) sont dans `desc`.


def AttacherTouched(effect: 'Effect') -> 'CardFace|None':
    """Trouve Touched et l'attache a un personnage autre que Rogue ; incline ce
    personnage s'il est amical. Rend le personnage choisi."""
    touched = TrouverTouched(effect)
    if touched is None:
        return None
    candidats = PersonnagesSaufRogue(effect)
    if not candidats:
        return None
    # ⚠ PAS `Filter.One` : il filtre par le TYPE du premier candidat
    # (`Filter.All(faces, type(faces[0]))`), ce qui ecarterait les vilains si le
    # premier personnage est une identite. Le premier joueur choisit lui-meme,
    # comme pour l'egalite tranchee par `Filter.One`.
    if len(candidats) == 1:
        cible = candidats[0]
    else:
        cible = effect.world.GetFirstPlayer().AskChooseFace(
            candidats, effect, prompt="Attach Touched to a character other than Rogue")
    if cible is None:
        return None
    if not touched.CastTo(Attachment).AttachTo2(cible, effect):
        return None
    if Friend.IsType(cible):
        Faces.ExhaustAll([cible], effect)
    return cible


def GetAbilities() -> Sequence['Ability']:

    def debut_de_phase(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)
        AttacherTouched(effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        touched = TouchedEnJeu(effect)
        if touched is not None:
            Faces.DiscardAll([touched], effect)

    return [
        AbilityFactory.AfterPhaseBegin(
            AbilityType.ForcedResponse,
            "Player",
            debut_de_phase,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            vaincue,
        ),
    ]
