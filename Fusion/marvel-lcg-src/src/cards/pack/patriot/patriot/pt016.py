from . import *

# Working Together — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [mental], `MaxPerUnit "1"`, trait TACTIC.
#
# Attach to an ally. Max 1 per ally.
# Interrupt: When the attached ally would thwart, choose another friendly
#   character and discard Working Together -> add the friendly character's
#   THW value to this ally's thwart.
#
# ---------------------------------------------------------------------------
# « ATTACH TO AN ALLY. MAX 1 PER ALLY. »
#
# `CanPlayThisUpgradeCard(Ally)` (modeles `01074`, `03031`, `12018`).
# `MaxPerUnit` est lu NATIVEMENT : aucun module pour lui.
#
# ---------------------------------------------------------------------------
# DECLENCHEUR
#
# `WhenUnitWouldThwart(AbilityType.Interrupt, "AttachedAlly", ...,
# is_basic_thwart=True)` : `"AttachedAlly"` designe le porteur de cette
# amelioration s'il est un allie (condition/card_type.py:37 et 182).
#
# `is_basic_thwart=True` n'est pas une restriction arbitraire : le bonus est
# pose par `GainTHWForThisThwart` (sender_friend.py:69-73), qui porte un
# `assert self.IsBasicThwart()`. Sans ce filtre, un contre non basique ferait
# PLANTER la carte. Un allie ne contre de toute facon que par son pouvoir de
# base, la restriction ne retire donc rien de jouable.
#
# ---------------------------------------------------------------------------
# LA FLECHE EST UN COUT -> UN EFFET, ET LE COUT A **DEUX** PARTIES
#
# « choose ANOTHER friendly character AND discard Working Together » : la
# designation ET la defausse. Rendues respectivement par un `.SetTarget(...)`
# obligatoire porte par la capacite et par
# `.SetCostFunc(CostFunc.Discard("This"))`. Sans autre personnage ami en jeu,
# le selecteur n'a aucune cible legale et l'interruption n'est PAS proposee :
# cout impayable = rien ne se passe, le contre de l'allie se resout nu.
#
# ---------------------------------------------------------------------------
# « ANOTHER FRIENDLY CHARACTER »
#
# « friendly character » nu = les identites ET les allies de TOUS les
# joueurs : c'est exactement `Worlds.GetOnFieldFriendlyCharacters`, ce que
# rend la cible-chaine `"Friend"` (selector_target_helper.py:243-244).
#
# « ANOTHER » = pas l'allie porteur lui-meme. On ne peut pas l'obtenir avec
# `exclude=["This"]` : « This » designerait l'AMELIORATION, pas son porteur.
# La cible est donc une fonction, comme chez `29024` Vivian, qui retire
# explicitement le porteur de la liste.
#
# La valeur ajoutee est le CTR COURANT du personnage choisi (`face.thwart`,
# bonus compris), pas sa valeur imprimee. Un personnage sans CTR (un heros en
# a un, un allie aussi ; une identite en forme alter-ego, non) est ecarte par
# la garde `HasThwart.IsType`.


def GetAbilities() -> Sequence['Ability']:

    def autres_personnages_amis(effect: 'Effect') -> List['CardFace']:
        # `.bind_face` et non `GetBindFace()` : le second porte un `assert`
        # (card_face.py:977-980) qui explose si la carte n'a plus de porteur.
        # Ce selecteur est evalue avant le paiement du cout, donc avant la
        # defausse — mais le garde ne coute rien et evite la meme
        # AssertionError AVALEE que celle trouvee sur pt013 le 30/08/2026.
        porteur = effect.this.CastTo(Upgrade).bind_face
        return [face for face in Worlds.GetOnFieldFriendlyCharacters(effect)
                if face != porteur]

    def working_together(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        if not effect.targets:
            return
        ami = effect.targets[0]
        if not HasThwart.IsType(ami):
            return

        valeur = ami.thwart
        if valeur > 0:
            message.GainTHWForThisThwart(valeur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.Interrupt,
            "AttachedAlly",
            working_together,
            is_basic_thwart=True,
        ).SetTarget(autres_personnages_amis, range=(1, 1), not_move=True)
        .SetCostFunc(CostFunc.Discard("This")),
    ]
