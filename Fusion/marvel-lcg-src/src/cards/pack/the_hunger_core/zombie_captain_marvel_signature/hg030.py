from . import *

# Rotten Binary — TREACHERY (set signature Zombie Captain Marvel, carte 1/4). Trait COSMIC (saveur, pas de
# mot-cle moteur).
# When Revealed: Deal 1 damage to each hero and each ally in play.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - Aucun mot-cle maison ni officiel sur cette carte : texte de base (When Revealed, dommage direct). Grep sur
#   `docs/reference/mots-cles/README.md` : rien a ouvrir.
# - Trait imprime « COSMIC » : trait DE SAVEUR (meme statut que « ATTACK » sur `hg016` Thrown Shield), rien a
#   coder pour lui.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « When Revealed: Deal N damage to each hero and ally in play » : texte IDENTIQUE a `hg016` Thrown Shield
#   (meme scenario, set signature Zombie Captain America, carte 1/3), qui porte deja ce texte au mot pres
#   (seule la valeur change : 2 sur hg016, 1 ici) et cite elle-meme `24035` * Mister Hyde (pack hood, minion)
#   comme modele d'origine officielle. Repris tel quel ici plutot que de refabriquer le raisonnement :
#   `this.DealDamage(Worlds.GetOnFieldHeroes(effect) + Worlds.GetOnFieldAllies(effect), 1, effect)`.
#   `Worlds.GetOnFieldHeroes` (worlds.py:246) ne retient que les identites EN FORME HEROS, `Worlds.
#   GetOnFieldAllies` (worlds.py:250) prend TOUS les allies de TOUS les joueurs : exactement la portee de
#   « each hero » / « each ally in play », sans restriction a « that player » ni a « you » (contrairement a
#   `hg012` Zombie Thor qui vise un seul joueur).
# - Fabrique `AbilityFactory.WhenThisRevealed(None, op)` + `Message.WhenCardRevealed`, meme modele que `hg016`/
#   `wd014` Get Shocked! (Treachery, `this = effect.this.CastTo(Treachery)`).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « When Revealed » -> `AbilityFactory.WhenThisRevealed`, declencheur a la revelation de CETTE carte
#   (`Condition2.ThisIsTrigger` deja integre a la fabrique, aucune garde a ajouter).
# « Deal 1 damage » -> `this.DealDamage(..., 1, effect)` ; valeur imprimee = 1, identique dans `data/
#   cards_custom.json` (`text`) et dans le script (verification etape 6).
# « to EACH HERO » -> `Worlds.GetOnFieldHeroes(effect)`, PAS `GetPlayersIdentities`/`GetOnFieldFriendlyCharacters`
#   (ces deux ramassent l'identite quelle que soit sa forme) : une identite en forme ALTER-EGO n'encaisse pas ce
#   degat, meme piege que `hg016`.
# « and EACH ALLY IN PLAY » -> `Worlds.GetOnFieldAllies(effect)`, tous les allies de la table, de TOUS les
#   joueurs -- aucun filtre par joueur (pas de « that player »/« you control » dans le texte imprime).
# « Degats DIRECTS » (pas une attaque de `this`) : la Treachery n'a ni ATK ni cible choisie, meme forme que
#   `hg016`/`wd014`/`24035`.
# Pas de surge, pas de choix de cible, pas de restriction « unless »/« otherwise » dans le texte imprime : rien
#   d'autre a coder.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)

        this.DealDamage(Worlds.GetOnFieldHeroes(effect) + Worlds.GetOnFieldAllies(effect), 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
