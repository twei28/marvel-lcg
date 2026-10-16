from . import *

# * Casey Jones (face alter-ego) — CIVILIAN. REC 4, PV 10, main 6.
# Setup: Search your deck and discard pile for the Casey's Bag upgrade and put
#   it into play. (Shuffle.)
# Response: After you change to this form, return a WEAPON upgrade from your
#   discard pile to your hand.
#
# CARTES DE REFERENCE
#  - Setup + fouille : `michelangelo/tm001b` (Mikey) et `aa001b` :
#    `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, finder=CardFinder(card_ids=[...]))` puis
#    `PutIntoPlay`. Le « (Shuffle.) » est le comportement par defaut.
#  - Response : `01019a` She-Hulk / `bt001b` : `AfterUnitChangeForm(type,
#    "You", op, to_this_form=True)`.
#  - « return ... from your discard pile to your hand » : `hd013` :
#    `Faces.ReturnToHand([face], joueur, effect)`, choix par `ForChoiceAbility
#    .SetTarget(liste, range=(1, 1), not_move=True)` (modele tr003).
#
# TEXTE CONTRE CODE
#  ⚠ « SEARCH YOUR DECK AND DISCARD PILE » + MAIN : DECISION UTILISATEUR (16/10/2026,
#    Q2). Le Setup du moteur part APRES la pioche de depart et le mulligan : le Sac
#    peut etre dans la main de depart (environ 1 partie sur 3). On le met en jeu
#    quand meme : deck + defausse, puis la main (comme tm001b de Michelangelo).
#  ⚠ « the Casey's BAG upgrade » : cherche par card_id `tc013`, jamais par nom.
#  ⚠ « return A WEAPON upgrade » : n'importe quelle arme (pas seulement du set
#    Casey Jones), au choix du joueur ; rien n'est offert si la defausse n'en a
#    pas. La Response est une capacite optionnelle du moteur.
#  ⚠ « After you change TO THIS FORM » : `to_this_form=True`, pas au Setup (la
#    partie commence en alter-ego sans changement de forme).


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        sac = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(card_ids=[ID_SAC]),
        )
        if not sac:
            # DECISION UTILISATEUR (16/10/2026, Q2) : fouiller AUSSI la main. Le Setup part
            # APRES la pioche de depart et le mulligan : le Sac peut etre dans la main de
            # depart (environ 1 partie sur 3). Meme traitement que tm001b (Michelangelo).
            en_main = [f for f in initiator.hand_cards.GetAll()
                       if getattr(f.paper, "card_id", None) == ID_SAC]
            if en_main:
                sac = en_main[0]
        if sac:
            sac.PutIntoPlay(initiator, effect)

    def une_arme_retourne_en_main(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        armes = [f for f in joueur.discard_pile.Get() if EstUneArme(f)]
        if not armes:
            return

        def retourner(cibles: Sequence['CardFace']) -> None:
            Faces.ReturnToHand(list(cibles), joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Return a WEAPON upgrade from your discard pile to your hand",
                retourner,
            ).SetTarget(armes, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            une_arme_retourne_en_main,
            to_this_form=True,
        ),
    ]
