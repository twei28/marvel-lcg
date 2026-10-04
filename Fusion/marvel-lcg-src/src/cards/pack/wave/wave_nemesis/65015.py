from . import *

# Triumph Probation — OBLIGATION, WAVE NEMESIS.
# Give to the Pearl Pangan player.
# Search your hand, deck, discard and play area for Wave's Swords and Wave's
# Crown and place them facedown under this card. Wave loses the TRIUMPH
# DIVISION trait.
# Alter Ego Action: Exhaust Pearl Pangan -> add Wave's Sword and Wave's Crown
# to your hand and remove Triumph Probation from the game.
#
# Modele de l'obligation « Give to the X player » : 01175 Family Emergency
# (`AbilityFactory.WhenThisObligationGiveToYou`, `message.GetGaveToPlayer()`).
# Modele de la recherche multi-zones : `Search.PlayerCard(effect, joueur,
# include_player_deck=True, include_discard_pile=True,
# include_player_hand_cards=True, include_player_area=True, name=...)`
# (game/operate/search.py:130) -- litteralement « hand, deck, discard and
# play area », les quatre drapeaux exacts. `name=` compare au NOM SANS
# L'ASTERISQUE (`printed_name`/`this.name` ne portent jamais le prefixe « * »
# des cartes signature -- c'est une decoration d'affichage separee, verifie
# le 22/9/2026 en imprimant `joueur.hand_cards`).
#
# Modele du glissement sous la carte : `CardFace.TuckCardUnderHere`, meme
# mecanisme que `black_cat` (`GlisserSousIdentite`) et Wave's Crown
# (`65010.py`) -- ici SANS `peek`, le texte imprime dit bien « facedown »,
# sans exception de visibilite pour le proprietaire.
#
# ⚠ « Wave loses the TRIUMPH DIVISION trait » : NI `AbilityFactory.
# GiveKeywordToInPlayWhenApplyThis` (suppose un effet d'ENVIRONNEMENT
# continu « en jeu », qu'une obligation n'est jamais -- `apply` n'etait
# simplement jamais rappelee), NI un `GainTraits(-1, ..., effect)` naif
# APPELE UNE FOIS avec `effect` (celui de l'obligation elle-meme) : trouve
# le 22/9/2026 en testant la carte, `CardFace.GainTraitInternal` (game/card/
# face/model/trait.py) attribue chaque trait au GRANTOR (`by_effect.this`),
# jamais a la face modifiee. Un trait IMPRIME est enregistre par `ResetTrait`
# sous LA FACE ELLE-MEME (`traits_internal[trait] = [this]`) : y retirer une
# entree exige un effet dont `.this` EST CETTE FACE, pas l'obligation --
# sans quoi `list.remove(x)` leve `ValueError` (avale en silence par le
# moteur, aucun message d'erreur visible). D'ou `GameRule(hero_face)`
# (game/effect/rule.py), un effet dont `.this` est explicitement la face
# heros, symetrique a l'entree posee par `ResetTrait`. Le trait est retire
# UNE FOIS quand l'obligation est donnee et rendu UNE FOIS quand elle quitte
# la partie -- exactement la duree imprimee, sans mecanisme continu.
# `Identity.GetHeroFace()` (game/card/face/card_type/identity.py) retrouve
# la face HEROS quelle que soit la face ACTIVE au moment ou la capacite
# s'execute (l'obligation peut etre donnee en alter-ego).
#
# « Exhaust Pearl Pangan » -> `CostFunc.Exhaust("YourIdentity")` en
# AlterEgoAction, modele ar010 Ire of Athena (« Exhaust your alter-ego »).

def GetAbilities() -> Sequence['Ability']:

    def triumph_probation(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        from game.effect.rule import GameRule

        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        for nom in ("Wave's Swords", "Wave's Crown"):
            face = Search.PlayerCard(
                effect, joueur,
                include_player_deck=True,
                include_discard_pile=True,
                include_player_hand_cards=True,
                include_player_area=True,
                name=nom,
                may=True,
            )
            if face is not None:
                this.TuckCardUnderHere(face, effect)

        hero_face = joueur.GetIdentity().GetHeroFace()
        hero_face.GainTraits(-1, ["TRIUMPH DIVISION"], GameRule(hero_face))

    def recuperer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        from game.effect.rule import GameRule

        this = effect.this.CastTo(Obligation)
        Unused(message)

        cartes = list(this.GetPlacedCardArea().Get(True))
        joueur = effect.GetInitiator()
        if isinstance(joueur, Player):
            if cartes:
                Faces.AddToHand(cartes, joueur, effect)
            hero_face = joueur.GetIdentity().GetHeroFace()
            hero_face.GainTraits(1, ["TRIUMPH DIVISION"], GameRule(hero_face))
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            triumph_probation,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            recuperer,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
