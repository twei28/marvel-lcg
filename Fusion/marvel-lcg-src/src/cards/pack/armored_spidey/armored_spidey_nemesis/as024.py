from . import *

# « The Kingpin of Crime » — complot ANNEXE nemesis. Menace de depart 2,
# Entrave 1, Boost 2.
# Hinder 1.
# Treat the printed text box of each non-permanent support as if it were
#   blank.
#
# Cartes de reference :
#  - **`27127`** Panic in the Streets : MEME FORME — un complot annexe qui
#    neutralise une famille de soutiens,
#    `GiveKeywordToInPlayWhenApplyThis(CardFinder(... Support),
#    treat_as_blank=True)`. Voir aussi `12026` Tech Theft.
#  - Le filtre « non-permanent » n'a pas de parametre dedie dans `CardFinder`
#    (`is_permanent` y est commente, finder.py:46) : `check_face_fn` est le
#    point d'entree prevu pour ce genre de test.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Hinder 1.** » : base automatique lue dans `desc.Hinder`, AUCUN
#    script (fiche mots-cles/hinder.md). Un module qui la recoderait
#    doublerait la menace posee.
#  - « **each** non-permanent support » : TOUS les soutiens de la table, de
#    tous les joueurs, sans restriction « you control ».
#  - « **non-permanent** » : les soutiens PERMANENTS sont epargnes. C'est le
#    mot qui fait toute la carte, et l'oublier neutraliserait aussi le Milano,
#    Alias Investigations et compagnie.
#  - « the **printed** text box » : le texte imprime, pas les traits ni les
#    mots-cles ; `treat_as_blank` est le mecanisme du moteur pour exactement
#    ca. ⚠ Le texte imprime de la carte ne dit PAS « except for [[TRAITS]] »,
#    contrairement a 27127 et 12026 — mais la regle du jeu conserve toujours
#    les traits, et le moteur n'expose aucun autre niveau. Aucune difference
#    de code.
#  - Rien ne vise les AMELIORATIONS : `as002a/b` Spider Armor, `as012` et
#    `as013` continuent de fonctionner. C'est bien ce qui est imprime.


def GetAbilities() -> Sequence['Ability']:

    def soutien_non_permanent(face: 'CardFace') -> bool:
        return not getattr(face, "permanent", False)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Support, check_face_fn=soutien_non_permanent),
            treat_as_blank=True,
        ),
    ]
