from . import *

# hs155 Voracious Ambush
# When Revealed (Hero) : Vulture (James Natale) attaque votre heros. Sinon, defaussez 6 cartes de rencontre et, s'il est
# dans la defausse de rencontre, mettez-le en jeu engage avec vous.

def GetAbilities() -> Sequence['Ability']:

    def est_natale(f: 'CardFace') -> bool:
        return f.IsCardId("hs151")

    def embuscade(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        en_jeu = Worlds.FindCardOnField(effect, check_face_fn=est_natale)
        if en_jeu is not None:
            en_jeu.CastTo(Enemy).DoAttackYou(joueur, effect)
            return
        Worlds.DiscardEncounterCards(6, effect)
        if any(est_natale(c) for c in Worlds.GetEncounterDiscardPileCards(effect)):
            Find.FindAndPutIntoPlay(
                effect, joueur,
                finder=CardFinder(card_type=Minion, check_face_fn=lambda f: f.IsCardId("hs151") and not f.IsInPlay()),
            )

    return [
        AbilityFactory.WhenThisRevealed("Hero", embuscade),
    ]
