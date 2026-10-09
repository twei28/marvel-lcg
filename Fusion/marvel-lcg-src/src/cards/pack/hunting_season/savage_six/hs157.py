from . import *

# hs157 The Savage Six
# When Revealed : chaque serviteur SAVAGE SIX attaque le heros avec qui il est engage. Aucune attaque : cherche un
# serviteur SAVAGE SIX (paquet et defausse de rencontre) et le met en jeu engage avec le premier joueur.

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        attaques = 0
        for m in Worlds.FindCardsOnField(effect, trait=TRAIT, card_type=Minion):
            joueur = m.CastTo(Minion).engaged_player
            if joueur is not None and m.CastTo(Minion).DoAttackYou(joueur, effect) is not None:
                attaques += 1
        if attaques == 0:
            Find.FindAndPutIntoPlay(
                effect, Worlds.GetFirstPlayer(effect),
                finder=CardFinder(trait=TRAIT, card_type=Minion, check_face_fn=lambda f: not f.IsInPlay()),
            )

    return [AbilityFactory.WhenThisRevealed(None, revelation)]
