from . import *

# * Alopex — ALLIE Leadership (TMNT Aspects, Inkwire), cout 3, [mental]. CLAW CLAN. FOX. NINJA.
# THW 2* / ATQ 2* / PV 3.
# Retaliate 1.
# Response: After Alopex enters play, cloak her.
#
# MOTS-CLES (fiches lues AVANT le code)
#  - Retaliate : `desc.Retaliate = "1"`, lu par le moteur (fiche retaliate.md) : AUCUNE ligne ici.
#  - Cloak : fiche cloak.md = poser une carte d'etat Cloaked (`Faces.GiveStatus(..., "Cloaked", ...)`) ;
#    regle de la carte d'etat : cloaked.md (une seule par personnage, sauf mention contraire).
#
# CARTES DE REFERENCE
#  - `03013` Squirrel Girl / `01067` Maria Hill : « Response: After X enters play » =
#    `AfterCardEnterPlay(Response, "This", op)`.
#  - `ta002` Nobody : « cloak her » = `Faces.GiveStatus([this], "Cloaked", effect)` sur l'allie lui-meme.
#
# TEXTE CONTRE CODE
#  ⚠ « cloak HER » : Alopex elle-meme, pas l'identite.
#  ⚠ « Response » : facultative (le joueur peut decliner), pas une Reponse forcee.
#  ⚠ Unicite : une identite « * Alopex » (ta001) existe. Question ouverte (fichier des questions ul).


def GetAbilities() -> Sequence['Ability']:

    def se_camoufler(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Cloaked", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            se_camoufler,
        ),
    ]
