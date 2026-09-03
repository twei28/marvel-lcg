from . import *

# * Spider-Verse — soutien BASIC, x1. LOCATION. Cout 2, ressource [wild].
# Play only if your identity has the [[WEB-WARRIOR]] trait or "Spider" in its
#   title.
# Increase your ally limit by 1.
# Action: Exhaust Spider-Verse -> generate a [energy] resource for an ally
#   with the [[WEB-WARRIOR]] trait or with "Spider" in its title for any
#   player.
#
# Cartes de reference :
#  - **`17022`** * Knowhere et `01073` * The Triskelion :
#    `GiveKeywordToInPlayWhenApplyThis("You", ally_limit=1)` pour « Increase
#    your ally limit by 1 » (environment.py:78). Rien d'autre a ecrire.
#  - **`14017`** Nerves of Steel : `CanGenerateResources(Resource,
#    Resources("Y"), <CardFinder>)` — le troisieme argument `for_card` est
#    exactement « generate a [x] resource FOR <telle carte> ».
#  - **`16142`** * Milano : `.AnyPlayerCanDoThis()` pour « for any player ».
#  - `mw001b` * Cassandra Webb (pack madame_web, meme auteur Kajislav) pour la
#    formule « WEB-WARRIOR trait or "Spider" in their title », deja rencontree.
#  - `CanPlayThisSupportCard(conditions=[...])` (play.py:8) pour la condition
#    de mise en jeu, qui n'est pas exprimable par `SetPlay` seul.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the [[WEB-WARRIOR]] trait **or** "Spider" in its title » : une
#    ALTERNATIVE. `SetPlay(only_if_your_identity_has_trait=...)` ne rend que
#    la moitie gauche — d'ou la condition ecrite a la main. Elle sert DEUX
#    fois : pour la mise en jeu (l'identite) et pour la ressource (l'allie).
#  - « "Spider" **in its title** » : une sous-chaine du nom, majuscule
#    comprise — « Spider-Man », « Spider-Bot », « Six-Armed Spider-Man ».
#    `face.TitleContain(...)` (face_name.py:73) est l'API du moteur : elle
#    couvre aussi les noms d'emprunt (`consider_as`), ce qu'un `in` sur
#    `face.name` raterait.
#  - « for **any player** » : la ressource sert aussi a un AUTRE joueur, d'ou
#    `.AnyPlayerCanDoThis()`. Sans lui, le soutien ne financerait que son
#    proprietaire.
#  - « a [energy] resource » : `Resources("Y")`, pas `"G"` (wild). Le [wild]
#    est le cout IMPRIME de la carte, pas ce qu'elle genere — deux choses
#    differentes sur la meme carte, c'est le piege classique de lecture.
#  - ⚠ ECART ASSUME, arbitrage technique (§9 du GUIDE) : la carte imprime
#    « **Action**: Exhaust ... -> generate ... ». Le moteur ne sait produire
#    une ressource que pendant un paiement, par `CanGenerateResources`, dont
#    le type doit valoir `Resource`, `HeroResource` ou `AlterEgoResource`
#    (assert de resources.py:277). C'est donc `AbilityType.Resource` qui est
#    ecrit, comme sur les 15 cartes officielles au meme texte (14017, 14030,
#    04010...). Aucune consequence de jeu : une « Action » qui genere une
#    ressource ne pourrait de toute facon servir qu'a payer une carte.
#  - ⚠ **UNE SEULE `CanGenerateResources` par carte** (assert du moteur).


def GetAbilities() -> Sequence['Ability']:

    def est_du_spider_verse(face: 'CardFace') -> bool:
        """« the [[WEB-WARRIOR]] trait or "Spider" in its title »."""
        if face is None:
            return False
        if face.HasTrait("WEB-WARRIOR"):
            return True
        return face.TitleContain("Spider")

    def identite_du_spider_verse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return est_du_spider_verse(joueur.GetIdentity())

    return [
        AbilityFactory.CanPlayThisSupportCard(
            conditions=[identite_du_spider_verse],
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            ally_limit=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
            CardFinder(card_type=Ally, check_face_fn=est_du_spider_verse),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]
