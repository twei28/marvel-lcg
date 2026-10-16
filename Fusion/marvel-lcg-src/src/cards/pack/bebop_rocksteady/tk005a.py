from . import *

# Demolition Crew (1A) : mise en place (« Put the Destructive Dunderheads
# environment, Welcome to the Jungle side scheme, Hog Wild attachment, and Rhino
# Rage attachment into play. »). Les deux vilains sont mis de cote par le
# scenario et mis en jeu ICI, comme Sinister Six (27100a).

def GetAbilities() -> Sequence['Ability']:

    def debut_de_mise_en_place(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        message.skip_put_villain_into_play = True

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)
        joueur = Worlds.GetFirstPlayer(effect)
        aside = Worlds.GetSetAsideAreaCards(effect)

        def trouver(card_id: str):
            for face in aside:
                if face.paper.card_id == card_id:
                    return face
            return None

        # Les vilains (A1 en normal, B1 en expert) : Bebop puis Rocksteady.
        vilains = [f for f in aside if Villain.IsType(f)]
        vilains.sort(key=lambda f: 0 if f.IsName("Bebop") else 1)
        for vilain in vilains:
            vilain.PutIntoPlay(joueur, effect)

        # Environnement, manigance annexe, puis les deux Temper (qui s'accrochent
        # a leur vilain en entrant en jeu).
        for card_id in ("tk006a", "tk101", "tk007a", "tk008a"):
            face = trouver(card_id)
            if face:
                face.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenGameBeginSetup(debut_de_mise_en_place),
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
