from . import *

# Destructive Dunderheads (environnement, face A)

def GetAbilities() -> Sequence['Ability']:

    # « Double Trouble -- During step two of the villain phase, both villains
    # activate against each player. »  Hook moteur `GettingVillainsToActivate`
    # (enemies.py) : tant que cette face est en jeu, les deux vilains s'activent.
    # L'ORDRE : le premier joueur choisit, pour chaque joueur, lequel s'active
    # d'abord (`Enemies.OrdreDesVilainsActives` ; tranche par l'utilisateur le
    # 16/10/2026, bebop-questions.md Q8, regle des effets simultanes).
    def les_deux_activent(effect: 'Effect', message: 'Message.GettingVillainsToActivate') -> None:
        vilains = VilainsEnJeu(effect)
        if len(vilains) >= 2:
            message.SetReturn(vilains)

    # « Choose either Bebop or Rocksteady as the target for each card that
    # references "the villain". » Le joueur qui resout la carte choisit UN vilain
    # (encart : « the player who revealed the encounter card chooses a singular
    # villain for that effect »). Memorise par effet : une seule question par carte.
    def le_vilain_au_choix(effect: 'Effect', message: 'Message.GettingVillain') -> 'Villain|None':
        by_effect = message.by_effect
        if by_effect is None:
            return None
        vilains = VilainsEnJeu(effect)
        if len(vilains) < 2:
            return None
        deja = getattr(by_effect, "_tk_vilain_choisi", None)
        if deja is not None and deja in vilains:
            return deja
        joueur = JoueurQuiResout(by_effect)
        choisi = joueur.AskChooseFace(vilains, by_effect, prompt="Choose Bebop or Rocksteady")
        if choisi is not None:
            by_effect._tk_vilain_choisi = choisi
        return choisi

    # « Forced Interrupt: When Bebop or Rocksteady is defeated, set that villain
    # and their TEMPER attachment aside. Flip the remaining villain to their ALERT
    # side, and this card to its FERAL side. »
    def vilain_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        vaincu = message.trigger
        reste = AutreVilain(effect, vaincu)
        temper = TemperDe(vaincu)
        a_ranger = [vaincu] if temper is None else [temper, vaincu]
        Faces.SetAside(a_ranger, effect)
        if reste is None:
            # Les deux vilains sont vaincus : les joueurs gagnent.
            Worlds.SetGameOver(True, effect)
            return
        MettreAlerte(reste, effect)
        this.card.Flip(effect)
        berserk = this.card.face
        if berserk.paper.card_id == "tk006b":
            berserk.CastTo(CanAttach).AttachTo2(reste, effect)

    return [
        Ability(AbilityType.NonKeyword, Message.GettingVillainsToActivate, [], les_deux_activent),
        AbilityFactory.GetVillain(le_vilain_au_choix),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            Villain,
            vilain_vaincu,
            conditions=[
                lambda effect, message: NomDuVilain(message.trigger) != ""
            ],
        ),
    ]
