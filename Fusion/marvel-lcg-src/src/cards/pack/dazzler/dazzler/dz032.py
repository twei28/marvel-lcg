from . import *

# Captivating Performance
# SONG.
# Hero Action: If the next card you play this turn is a SONG event, stun an
#   enemy.
#
# La carte pose une PROMESSE : elle ne fait rien tout de suite, elle arme une
# reponse a la PROCHAINE carte jouee ce tour. On enregistre donc une capacite
# temporaire, a usage unique, qui se desarme des qu'une carte est jouee — que
# ce soit un [[SONG]] ou non, sinon « the NEXT card » deviendrait « la
# prochaine chanson », ce qui n'est pas ecrit.
#
# Elle est enregistree sur l'IDENTITE et non sur cette carte : celle-ci part
# aussitot dans la Setlist ou a la defausse.


def GetAbilities() -> Sequence['Ability']:

    def performance(effect: 'Effect',
                    message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        def a_la_prochaine(eff: 'Effect',
                           msg: 'Message.AfterPlayerPlayedCard') -> None:
            jouee = msg.played_face
            if jouee is None or not EstUnSong(jouee):
                return
            ennemis = [e for e in Worlds.FindCardsOnField(eff, card_type=Enemy)]
            if not ennemis:
                return
            cible = joueur.AskChooseOneText(ennemis) if len(ennemis) > 1 \
                else ennemis[0]
            if cible is not None:
                Faces.GiveStatus([cible], "Stunned", eff)

        def pas_elle_meme(eff: 'Effect',
                          msg: 'Message.AfterPlayerPlayedCard') -> bool:
            # CORRECTIF (partie reelle) : sans cette condition, la promesse se
            # declenchait sur CAPTIVATING PERFORMANCE ELLE-MEME. Elle est
            # enregistree pendant la resolution de son « Hero Action », donc
            # AVANT le `AfterPlayerPlayedCard` de sa propre pose : le moteur la
            # lui servait aussitot, et comme elle porte le trait [[SONG]], un
            # ennemi etait etourdi sur-le-champ. Mesure : Rhino etourdi des la
            # pose, sans qu'aucune autre carte n'ait ete jouee.
            # Le texte dit « the NEXT card you play » : c'est une AUTRE carte.
            # La condition est portee par l'ABILITY et non par l'operation,
            # sinon `unregister_after_exec` consommerait la promesse sur ce
            # faux declenchement.
            return msg.played_face is not this

        identite.effect.RegisterTemp(
            AbilityFactory.AfterPlayerPlayedCard(
                AbilityType.Temp2,
                "You",
                None,
                a_la_prochaine,
                conditions=[pas_elle_meme],
            ),
            unregister_after_exec=True,
            # « this TURN » : la promesse tombe a la fin du tour (20/10/2026,
            # backlog 12 ; avant, elle attendait la prochaine carte jouee,
            # meme des rounds plus tard).
            until_turn_end=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            performance,
        ).SetPlay().SetLabel(),
    ]
