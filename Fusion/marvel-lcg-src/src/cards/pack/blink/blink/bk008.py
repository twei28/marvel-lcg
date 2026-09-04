from . import *

# * Blink's Quiver — AMELIORATION, cout 2, [wild]. ITEM.
# ⚠ NOM DE FICHIER TROMPEUR : le zip l'appelle « 10 javelin quiver », la
#   CARTE dit BLINK'S QUIVER. Le scan fait foi (meme piege que night_thrasher,
#   ou trois fichiers portaient un autre nom que leur carte).
# Hero Action: Exhaust Blink's Quiver -> search your deck for a [[PORTAL]]
#   upgrade and add it to your hand.
# Hero Action: Put a [[PORTAL]] upgrade from your hand into play.
#
# TEXTE CONTRE CODE
#  DEUX Hero Actions distinctes, la premiere a cout d'inclinaison, la seconde
#  GRATUITE : c'est elle qui rend le moteur explosif, et elle n'a volontairement
#  aucun cout imprime.
#  « PUT into play » -> mise en jeu sans payer le cout de la carte.


def GetAbilities() -> Sequence['Ability']:

    def chercher_un_portail(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        # ⚠ `Search.PlayerCard` rend UNE face ou None (`-> TC|None`,
        # search.py:146), PAS une liste : c'est `Search.SearchForCards` qui
        # rend une liste. Indexer le resultat levait
        # « 'Upgrade' object is not subscriptable », que le moteur AVALE — la
        # carte ne faisait donc rien, en silence, et seul le journal le disait.
        face = Search.PlayerCard(
            effect, joueur,
            include_player_deck=True,
            trait=TRAIT_PORTAIL,
            card_type=Upgrade,
        )
        if face is not None:
            joueur.GainCard(face, effect)

    def poser_un_portail(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for face in joueur.hand_cards.Get():
            if face.HasTrait(TRAIT_PORTAIL):
                face.PutIntoPlay(joueur, effect)
                return

    def un_portail_en_main(effect: 'Effect', message: 'Message2') -> bool:
        """⚠ SANS CETTE GARDE, LA CARTE PROPOSE UNE ACTION MORTE.

        La seconde Hero Action n'a aucun cout : le moteur l'offrait donc
        toujours, meme sans portail en main, ou elle ne faisait rien. Elle
        passait alors DEVANT la recherche dans l'ordre des options, et le cas
        de test declenchait cette action vide en croyant fouiller le deck.
        """
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return any(f.HasTrait(TRAIT_PORTAIL) for f in joueur.hand_cards.Get())

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chercher_un_portail,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            poser_un_portail,
            conditions=[un_portail_en_main],
        ),
    ]
