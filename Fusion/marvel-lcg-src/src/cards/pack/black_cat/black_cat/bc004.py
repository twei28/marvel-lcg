from . import *

# * Big Heist — MANIGANCE ANNEXE JOUEUR, cout 0, [mental]. Menace 4. UNIQUE.
# Only THIEF characters can remove threat from this scheme.
# When Defeated: Choose one:
#  • Search your collection for a basic or aspect upgrade and play it,
#    ignoring its resource cost.
#  • Tuck an attachment in play with the text "Hero Action" or "Hero Response"
#    under Black Cat.
#  • Draw 3 cards.
#
# ⚠ 4 MENACES ET UN VERROU : seuls les personnages VOLEUR peuvent les retirer.
# Au depot, le trait THIEF n'est porte que par TROIS cartes hors ce pack
# (`37001a`/`37001b` * Gambit et `48021` * Gambit allie) : en solo avec Black
# Cat, il n'y a donc qu'ELLE. C'est ce qui fait de cette carte un vrai
# investissement, et pas un cadeau.
#
# CARTES DE REFERENCE
#  - `40019` * Lock and Load / `40027` * Build Support : le squelette d'une
#    manigance annexe JOUEUR a « When Defeated »
#    (`WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", ...)`).
#  - `40006` * Technovirus Purge : `ThreatCannotBeRemovedFromWhile("This",
#    by_character=CardFinder(...))`, exactement le verrou d'ici, au filtre
#    pres (nom la-bas, trait ici).
#  - `dz031` Tribute (pack dazzler) : `Search.Collection` + `Faces.AddToHand`
#    + `PlayCardsLikeInTurn(..., ignore_resources_cost=True)`. LE modele de la
#    premiere branche, et la preuve que « votre collection » est REELLEMENT
#    implementable — contrairement a ce que suppose `wd029`, qui a assume un
#    ecart faute d'avoir vu `Search.Collection`.
#
# TEXTE CONTRE CODE
#  ⚠ « Only THIEF CHARACTERS » -> `by_character=CardFinder(non_trait="THIEF")` :
#    la fabrique interdit le retrait par tout ce qui NE porte PAS le trait. Le
#    filtre est donc la NEGATION, pas le trait lui-meme.
#  ⚠ « CHOOSE ONE » -> trois branches EXCLUSIVES. Le pilote prend la premiere
#    par defaut (RECETTES §2), les cas forcent celle qu'ils mesurent.
#  ⚠ « a BASIC OR ASPECT upgrade » -> tout sauf la classe `Hero` : c'est le
#    sens litteral, et c'est la lecture retenue par `dz031` pour
#    « non-identity event ». `card_classes="Any"` serait FAUX : il ne vaut que
#    les cinq aspects officiels et jetterait les ameliorations basiques.
#  ⚠ « and PLAY IT, ignoring its resource cost » -> la carte fabriquee arrive
#    dans la DEFAUSSE (`Search.Collection` la genere la) et n'y est PAS
#    jouable (`is_like_in_hand`, ability.py:235). Elle doit passer par la MAIN
#    d'abord. Piege paye par `dz031`.
#  ⚠ « an ATTACHMENT IN PLAY with the text ... » -> le TYPE `Attachment`, donc
#    une carte de RENCONTRE attachee a un ennemi ou a une manigance. Le filtre
#    est le TEXTE IMPRIME, lu sur `face.paper.text` : 132 attachements du
#    depot portent « Hero Action » ou « Hero Response », ce sont ceux qu'on
#    peut normalement payer pour defausser. Black Cat les VOLE au lieu de les
#    payer, et c'est tout le theme du pack.
#  ⚠ « under BLACK CAT » -> la pile de l'identite. Le nom n'est PAS employe
#    pour la retrouver : trois cartes du depot s'appellent deja « * Black
#    Cat ». La branche n'est offerte que s'il existe une cible.


def GetAbilities() -> Sequence['Ability']:

    def basique_ou_aspect(paper: 'Paper') -> bool:
        classes = (paper.desc.get("Class") or "").split(";")
        return "Hero" not in classes

    def porte_une_action_de_heros(face: 'CardFace') -> bool:
        texte = getattr(face.paper, "text", "") or ""
        return "Hero Action" in texte or "Hero Response" in texte

    def le_gros_coup(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return

        def chercher_en_collection(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            face = Search.Collection(
                effect, joueur, card_type=Upgrade, check_fn=basique_ou_aspect)
            if face is None:
                return
            # ⚠ Par la MAIN : une carte dans la defausse n'est pas jouable.
            Faces.AddToHand([face], joueur, effect)
            joueur.PlayCardsLikeInTurn([face], effect, ignore_resources_cost=True)

        def voler_un_attachement(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            candidats = [f for f in Worlds.GetOnFieldCards(effect)
                         if Attachment.IsType(f) and porte_une_action_de_heros(f)]
            if not candidats:
                return
            choisi = joueur.AskChooseFace(candidats, effect)
            if choisi is not None:
                GlisserSousIdentite(effect, [choisi], joueur)

        def piocher(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            joueur.DrawUp(3, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Search your collection for a basic or aspect upgrade",
                chercher_en_collection),
            AbilityFactory.ForChoiceAbility(
                "Tuck an attachment in play under Black Cat",
                voler_un_attachement),
            AbilityFactory.ForChoiceAbility(
                "Draw 3 cards", piocher),
        )

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(non_trait="THIEF"),
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            le_gros_coup,
        ),
    ]
