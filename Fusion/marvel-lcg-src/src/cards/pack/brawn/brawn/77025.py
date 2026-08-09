from . import *

# Brains and Brawn (team-up) — custom « Rainy »
# Team-Up (Brawn and Ironheart). Max 1 per deck.
# Hero Action: For each printed resource in your hand and reserve, if it is a:
#   [physical] - Deal 1 damage to an enemy.
#   [mental] - Remove 1 threat from a scheme.
#
# ARBITRAGE (utilisateur, 7/8/2026) : meme montage que Strong as Silk 77024 —
# Ironheart est l'alliee signature 77003, pas une identite, donc la restriction
# est une condition de jeu et non la cle `TeamUp`.
#
# Seule carte du pack qui lit la MAIN et la RESERVE ensemble : c'est la
# recompense de la mecanique, et la raison pour laquelle elle compte les icones
# IMPRIMEES (rien n'est depense ici).
#
# Une icone [wild] compte pour chaque couleur, comme chez Hulk 01050.

# Meme piege que Strong as Silk 77024 : `only_if_you_control_face` ne regarde
# que les cartes ATTACHEES a l'identite, jamais les allies.
def _ironheart_en_jeu(effect: 'Effect') -> 'CardFace|None':
    joueur = effect.GetInitiator()
    if not isinstance(joueur, Player):
        return None
    for face in joueur.allies.Get():
        if face.IsName("Ironheart"):
            return face
    return None


def GetAbilities() -> Sequence['Ability']:

    def brains_and_brawn(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        joueur = effect.GetInitiator()

        # `this` est deja parti en zone de traitement quand on arrive ici : il
        # ne se compte donc pas lui-meme, ce qui est bien le comportement voulu
        # (« in your hand and reserve », et la carte n'y est plus).
        cartes = list(joueur.hand_cards.Get()) + list(joueur.reserve.Get())
        icones = FacesCounter.GetPrintedResources(cartes)
        physiques = icones.r + icones.g
        mentales = icones.b + icones.g

        for _ in range(physiques):
            ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))
            if not ennemis:
                break
            cible = joueur.AskChooseFace(ennemis, effect, not_move=True)
            if cible is None:
                break
            this.DealDamage([cible], 1, effect)

        for _ in range(mentales):
            plans = list(Worlds.FindCardsOnField(effect, card_type=Scheme2))
            if not plans:
                break
            cible = joueur.AskChooseFace(plans, effect, not_move=True)
            if cible is None:
                break
            this.RemoveThreatFromSchemes([cible], 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            brains_and_brawn,
            conditions=[lambda effect, message: _ironheart_en_jeu(effect) is not None],
        ).SetPlay(hero_form_only=True),
    ]
