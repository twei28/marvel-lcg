from . import *

# * Agent Anti-Venom (Flash Thompson) — ALLIE, cout 4, PV 3, CTR 2* / ATQ 2**.
# AVENGER. SYMBIOTE.
# Response: After Agent Anti-Venom enters play, discard cards from the top of
#   your deck until you discard an ally that shares a TRAIT with him -> put
#   that ally into play.
#
# MOT-CLE
#  ⚠ Ce n'est PAS le mot-cle maison `seek` (fiche `mots-cles/seek.md`), mais
#    c'est EXACTEMENT sa mecanique, ecrite en toutes lettres : « discard cards
#    from the top of your deck until you discard a <type> ». On emploie donc
#    la meme primitive, `Player.DiscardDeckUntil`.
#
# CARTES DE REFERENCE
#  - `21055` Summoning Spell : « Discard cards from the top of your deck until
#    you discard an ally » puis mise en jeu. Meme phrase, au filtre pres.
#  - `br005` Star Jump (maison) : l'usage direct de `DiscardDeckUntil` dans le
#    corps plutot que par `CostFunc`, quand un FILTRE est necessaire.
#
# TEXTE CONTRE CODE
#  ⚠ « that shares a TRAIT WITH HIM » : le filtre du moteur
#    (`CostFunc.DiscardDeckTopUntil`) ne connait que le TYPE de carte, pas le
#    partage de trait. D'ou l'appel direct a `DiscardDeckUntil` avec
#    `check_face_fn` — le point d'entree prevu pour un predicat maison.
#  ⚠ Le partage se lit contre CETTE carte (`face.ShareTrait(this)`), pas
#    contre l'identite : Agent Anti-Venom est AVENGER et SYMBIOTE.
#  ⚠ La carte trouvee est DEJA DANS LA DEFAUSSE quand on la met en jeu
#    (`Deck.DiscardUntil` defausse aussi la carte trouvee, cf.
#    `mots-cles/seek.md`) : c'est le comportement du moteur, pas un ecart.
#  ⚠ Deck epuise sans allie correspondant : `DiscardDeckUntil` rend None, on
#    ne met rien en jeu. Le texte ne prevoit pas de repli.
def GetAbilities() -> Sequence['Ability']:

    def agent_anti_venom(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return

        def partage_un_trait(face: 'CardFace') -> bool:
            return face.ShareTrait(this)

        trouve = joueur.DiscardDeckUntil(
            effect,
            card_type=Ally,
            check_face_fn=partage_un_trait,
        )
        if trouve:
            trouve.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            agent_anti_venom,
        ),
    ]
