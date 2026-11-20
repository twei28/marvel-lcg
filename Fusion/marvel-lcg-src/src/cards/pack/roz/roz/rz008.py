from . import *

# * A.T.M.C.P. — SOUTIEN unique, cout 1, [physical]. VEHICLE. WAKANDA.
# You gain the [[Aerial]] trait.
# Special: Exhaust A.T.M.C.P. → choose 1: • Ready your identity. • Change form.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « You gain the [[Aerial]] trait » : `bw013` (`GiveKeywordToInPlayWhenApplyThis("You", ...)`) pour le
#    SOUTIEN, `09009` Cloak of Levitation (`GiveKeywordToAttached("You", trait="AERIAL")`) pour une amelioration.
#  - « choose 1 » : `45016` Side-by-Side (`ChooseAbilities` + `ForChoiceAbility`) ; `hc002` (« Ready your identity »).
#  - « Change form » : `01025` Split Personality (`identite.ChangeToOtherIdentityForm(effect)`).
#
# MOTS-PIEGES
#  - « you gain the AERIAL trait » : tant que le soutien est en jeu (trait continu, `trait="AERIAL"`).
#  - « Exhaust A.T.M.C.P. → » : le cout est l'inclinaison de la carte ; « choose 1 » : UN seul des deux.
#  - « Ready your IDENTITY » : le heros OU l'alter ego, selon la forme courante.
def GetAbilities() -> Sequence['Ability']:

    def choisir(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready your identity",
                lambda targets: Faces.ReadyAll([identite], effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Change form",
                lambda targets: identite.ChangeToOtherIdentityForm(effect),
            ),
        )

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            trait="AERIAL",
        ),
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            choisir,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
