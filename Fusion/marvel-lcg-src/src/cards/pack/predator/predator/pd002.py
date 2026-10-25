from . import *

# * Infralocked — AMELIORATION, cout 0, Permanent. TACTIC. UNIQUE, un seul exemplaire (1/16), mise de cote puis mise en jeu
# par le Setup de l'alter-ego (pd001b), deplacee de sbire en sbire par la Reponse du heros (pd001a).
# Permanent.
# Hero Interrupt: When Predator defeats attached minion, remove 2 threat from a scheme (3 threat instead from a side
#   scheme). Then, return this card to your play area.
#
# Cartes de reference :
#  - `yd012` Yaka Arrow (pack yondu) : amelioration unique qui change d'hote (ennemi / identite) par `AttachTo2` ; son
#    Interrupt part de l'ENNEMI porteur (`WhenUnitWouldBeDefeated`) ; `AttachToFaceWhenPutIntoPlay("YourIdentity")`
#    (`sk147`, `mf016`) pour l'entree en jeu sur l'identite.
#  - `WhenUnitBeDefeated(.., "AttachedCharacter", op, attacker=...)` (`pu092`, sl040) : « attached minion is defeated ».
#  - `RetirerMenaceDUneManigance` (alligator_loki / web_of_deceit) : « remove N threat from a scheme », choix du joueur.
#
# ⚠ Mots-pieges :
#  - « Permanent » : base automatique (`desc.Permanent`), AUCUN code. ⚠ L'amelioration ne quitte donc jamais le jeu par
#    l'effet d'un AUTRE set : si son sbire hote disparait autrement que par Predator, elle reste en jeu (a verifier au harnais).
#  - « Return this card TO YOUR PLAY AREA » : le moteur n'a pas d'amelioration libre ; la carte revient sur l'IDENTITE du
#    joueur (decision d'implementation, signalee a l'utilisateur) : `AttachTo2(identite)`.
#  - « 2 threat from a scheme (3 threat INSTEAD from a SIDE scheme) » : la valeur depend de la manigance CHOISIE ; le
#    complot principal vaut 2, une manigance annexe 3 (pas 2+1).
#  - « When PREDATOR defeats attached minion » : le heros Predator lui-meme (nom propre : face HEROS seulement), pas un
#    allie ; l'Interrupt part AVANT la defaite (le sbire porte encore la carte).


def GetAbilities() -> Sequence['Ability']:

    def marque_vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        manigances = [x for x in (list(Worlds.GetMainSchemes(effect)) + list(Worlds.GetAllSideSchemes(effect)))
                      if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
        if manigances:
            cible = joueur.AskChooseFace(manigances, effect, prompt="Remove threat from")
            cible = cible or manigances[0]
            valeur = 3 if cible in list(Worlds.GetAllSideSchemes(effect)) else 2
            Faces.RemoveTokensOn([cible], valeur, 'threat', effect)
        identite = joueur.GetIdentity()
        if identite is not None:
            this.AttachTo2(identite, effect)

    def hote_quitte_le_jeu(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        # Permanent : la carte ne quitte pas le jeu avec son hote (HasPermanent la retient), elle ne doit pas rester
        # accrochee a un sbire disparu : elle revient sur l'identite, comme « return this card to your play area ».
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        identite = joueur.GetIdentity() if joueur is not None else None
        if identite is not None:
            this.AttachTo2(identite, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.Rule,
            "AttachedCharacter",
            hote_quitte_le_jeu,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.HeroInterrupt,
            "AttachedCharacter",
            marque_vaincue,
            attacker=CardFinder(name="Predator", card_type=Hero),
        ),
    ]
