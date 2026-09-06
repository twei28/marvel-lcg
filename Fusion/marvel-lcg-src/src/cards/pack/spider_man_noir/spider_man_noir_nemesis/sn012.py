from . import *

# Power Struggle — COMPLOT ANNEXE nemesis (N 1/5). 3 icones de boost.
#   Menace de depart 2[per_hero]. Icone AMPLIFY.
# Forced Interrupt: When a character thwarts this scheme, they take 1 damage.
#
# MOT-CLE : AMPLIFY — fiche `docs/reference/mots-cles/amplify.md`. BASE
# AUTOMATIQUE, `desc.Amplify = "1"`, AUCUN SCRIPT : le moteur ajoute une icone
# de boost par icone Amplify en jeu quand une carte de boost est retournee
# (`ResolveAmplify`, can_boost.py:71).
# ⚠ L'icone a ete identifiee PAR COMPARAISON D'IMAGE avec `16054` Vendetta,
# une carte officielle dont le `desc` declare `"Amplify": "1"` — jamais a vue.
# C'est un « + » fondu dans l'icone de boost, a ne pas confondre avec le « + »
# sur carte inclinee (hazard) ni avec celui sur maison soulignee
# (acceleration). Lecon Lockjaw.
#
# CARTE DE REFERENCE
#  - `WhenSchemeBeingThwart` / `WhenUnitWouldThwart` : la fenetre « when a
#    character thwarts THIS scheme ». On prend la fabrique qui porte le
#    complot vise, pour ne pas punir un contre dirige ailleurs.
#
# TEXTE CONTRE CODE
#  ⚠ « When A CHARACTER thwarts this scheme » -> N'IMPORTE QUEL personnage,
#    pas seulement le heros : un allie qui contre ce complot prend le degat
#    lui aussi. C'est ce qui rend la carte penible, et c'est imprime.
#  « THEY take 1 damage » -> celui qui contre, pas le joueur. Un allie encaisse
#    donc a la place de l'identite.
#  ⚠ « FORCED INTERRUPT » : le degat tombe AVANT que la menace ne parte. Un
#    allie a 1 PV meurt donc sans avoir contre.


def GetAbilities() -> Sequence['Ability']:

    def le_prix_du_contre(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        contreur = message.trigger
        if contreur is not None:
            this.DealDamage([contreur], 1, effect)

    return [
        AbilityFactory.WhenUnitMakeThwart(
            AbilityType.ForcedInterrupt,
            None,
            "This",
            le_prix_du_contre,
        ),
    ]
