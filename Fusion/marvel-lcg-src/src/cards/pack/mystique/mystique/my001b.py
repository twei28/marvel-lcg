from . import *

# * Raven Darkhölme (face ALTER-EGO) : MUTANT. REC 4, main 6, PV 10.
# Setup: Put the Shapeshifter upgrade into play. Put all 3 shapeshift form upgrades into play, facedown.
# Fast Heal — Action: Heal 1 damage or remove a status card from Raven Darkhölme. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `36001b` Ororo Munroe (storm) : `BeginGameWithSetAside([...])` + `WhenCardSetup("This", op)` + `face.CastTo(..).PutIntoPlay(joueur, effect)` pour mettre en jeu des cartes mises de cote.
#  - `my002` : Shapeshifter est PERMANENT + `Setup` dans `desc` : le moteur la met en jeu a la mise en place (RECETTES §3 ; `60113a`), sans script ici.
#  - `25024` Godlike Stamina : `HealthUnits` + `components.status.GetDeck()` pour « heal ... or remove a status card from <identite> ».
#
# TEXTE CONTRE CODE
#  « Put all 3 shapeshift form upgrades into play, FACEDOWN » : chaque forme est creee face `b` en premiere face (id « my00Nb,my00Na »), posee en jeu sous le controle du joueur ; AUCUN declenchement
#    « turned faceup ». « Fast Heal » : Action d'alter-ego (pas d'exigence d'exhaustion), « heal 1 damage OR remove a status card » : UN des deux, a la volonte, jamais les deux ; le moteur n'offre une branche que
#    si elle est possible. « from RAVEN DARKHOLME » : l'identite. « Limit once per round » : `LimitOncePerRound`.
#  Chiffres : PV 10, main 6, REC 4, soin 1.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        deja = [IdDe(f)[:5] for f in Formes(joueur)]
        for face in list(joueur.set_aside_deck.Get()):
            if EstUneForme(face) and IdDe(face)[:5] not in deja:
                face.CastTo(Upgrade).PutIntoPlay(joueur, effect, under_control=True)
                deja.append(IdDe(face)[:5])

    def a_des_degats(identite: 'CardFace') -> bool:
        return Degats(identite) > 0

    def soin_rapide_possible(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        return a_des_degats(identite) or identite.components.status.GetStatusSize() > 0

    def soin_rapide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        statuts = list(identite.components.status.GetDeck().Get(True))

        def soigner(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            this.HealthUnits([identite], 1, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(cibles, effect)

        soin = AbilityFactory.ForChoiceAbility("Heal 1 damage from Raven Darkhölme", soigner, condition=a_des_degats(identite)).SetHasNoTargetEffect()
        statut = AbilityFactory.ForChoiceAbility("Remove a status card from Raven Darkhölme", retirer)
        if statuts:
            statut.SetTarget(statuts)
        else:
            statut = AbilityFactory.ForChoiceAbility("Remove a status card from Raven Darkhölme", retirer, condition=False).SetHasNoTargetEffect()
        joueur.ChooseAbilities(effect, soin, statut)

    return [
        AbilityFactory.BeginGameWithSetAside(["my003b,my003a", "my004b,my004a", "my005b,my005a"]),
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            soin_rapide,
            conditions=[soin_rapide_possible],
        ).SetName("Fast Heal").LimitOncePerRound(),
    ]
