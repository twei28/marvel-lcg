from . import *

# * Mondo Gecko — ALLIE 2 [mental], aspect Justice (TMNT Allies, Inkwire). GECKO. MUTANIMAL.
# PV 2, THW 1 (1 degat consecutif), ATK 1 (1 degat consecutif).
# Response: After Mondo Gecko enters play, cloak him.
#
# MOTS-CLES (fiches lues AVANT le code) : CLOAK — docs/reference/mots-cles/cloak.md (« Cloak X » = poser une
# carte d'etat Cloaked sur X) ; CLOAKED — cloaked.md (un seul effet, le premier qui arrive : +2 au prochain
# pouvoir de base OU -2 aux prochains degats, puis la carte part ; UNE seule Cloaked par personnage).
#
# CARTES DE REFERENCE
#  - `td005` Improvised Tactics : « Cloak <personnage ami> » = `Faces.GiveStatus([face], "Cloaked", effect)`.
#  - `tl016` Foot Soldiers : « Cloak <cette carte> » sur l'entree en jeu.
#  - RECETTES §1 : « After <allie> enters play » = `AfterCardEnterPlay(Response, "This", op)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « cloak HIM » : Mondo Gecko lui-meme. Deja Cloaked (maximum 1) : rien ne se pose (`GainStatus` refuse),
#    la Reponse n'est alors pas proposee.
#  ⚠ « enters play » : toute entree en jeu.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def camoufler(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        Faces.GiveStatus([this], "Cloaked", effect)

    def peut_etre_camoufle(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)
        this = effect.this.CastTo(CanStatus)
        return this.cloaked < this.cloaked_max

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            camoufler,
            conditions=[peut_etre_camoufle],
        ),
    ]
