from . import *

# hs121 / hs122 Big Game Hunter
# When Revealed : Kraven attaque le heros dont les PV imprimes sont les plus eleves ; les autres personnages ne peuvent pas defendre. Sans attaque, distribue un piege.

def GetAbilities() -> Sequence['Ability']:

    def gibier(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        kraven = Kraven(effect)
        attaque = False

        if kraven is not None:
            heros = [p for p in Worlds.GetPlayers(effect) if p.IsHero()]
            if heros:
                maximum = max(p.GetIdentity().printed_health_numeral for p in heros)
                a_egalite = [p for p in heros if p.GetIdentity().printed_health_numeral == maximum]
                cible = a_egalite[0]
                if len(a_egalite) > 1:
                    noms = {p.GetIdentity(): p for p in a_egalite}
                    choisi = joueur.AskChooseFaces(list(noms), (1, 1), effect, prompt="Big Game Hunter")
                    if choisi:
                        cible = noms[choisi[0]]

                resultat = kraven.DoAttackYou(cible, effect, other_characters_cannot_defend=True)
                attaque = resultat is not None

        if not attaque:
            DonnerPiege(effect, joueur)

    return [AbilityFactory.WhenThisRevealed(None, gibier)]
