from . import *

# Shi'ar Throne (face A) — MANIGANCE ANNEXE (Majestrix's Verdict), menace de depart 3[per_hero]. Hazard.
# When Defeated: The defeating player flips this card and takes control of it.
#
# Cartes de reference :
#  - Hazard : BASE AUTOMATIQUE (`desc.Hazard`), aucun module.
#  - « When Defeated: flip this card and take control of it » : modele OFFICIEL 32172a Enemy of My Enemy
#    (`card.Flip` puis `PutIntoPlay(joueur, under_control=True)` de la face retournee).
#    ⚠ Mesure du 20/10/2026 : fait DANS le « When Defeated », le retournement est defait par la regle de defaite
#    (`Scheme.OnBeDefeated`, scheme.py : « if self.IsInPlay(): Faces.DiscardAll([self]) » defausse la CARTE
#    retournee, le soutien finissait dans la defausse du joueur). Le « When Defeated » note donc le joueur, et le
#    retournement se fait juste APRES la defausse de regle (`AfterSchemeBeDefeated`, usage unique) : le soutien
#    entre en jeu depuis la defausse sous le controle de ce joueur. Aucun fichier moteur touche.
#
# ⚠ Mots-pieges : « the DEFEATING player » (`message.defeating_player`, repli sur le premier joueur si la
# manigance est vaincue sans joueur) ; la face B est un SOUTIEN unique, pas une amelioration.


def GetAbilities() -> Sequence['Ability']:

    def conquerir(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(SchemeSide2)
        # `GetDefeatingPlayer()` affirme qu'il y en a un (sender_scheme.py) : on lit le champ, repli premier joueur.
        joueur = message.defeating_player or Worlds.GetFirstPlayer(effect)

        def apres_la_defaite(effect2: 'Effect', message2: 'Message.AfterSchemeBeDefeated') -> None:
            carte = this.card
            if SchemeSide2.IsType(carte.face):
                carte.Flip(effect2, call_reveal=False)
            soutien = carte.face
            if Support.IsType(soutien) and not soutien.IsInPlay():
                soutien.CastTo(Support).PutIntoPlay(joueur, effect2, under_control=True)

        this.effect.RegisterTemp(
            AbilityFactory.AfterSchemeBeDefeated(AbilityType.Temp0, "This", apres_la_defaite).NoOutOfPlayLimit(),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", conquerir),
    ]
