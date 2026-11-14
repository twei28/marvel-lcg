from . import *

# * Blink (Clarice Ferguson) : allie RECRUITED, cout 3, PV 2, THW 1*, ATK 1*.
# Any of the players may play Blink from the Recruited Mutants discard pile during their own turn (paying its resource cost).
# Forced Response: When Blink is defeated, shuffle her into the Recruited Mutants deck.
#
# Cartes de reference : dz014 / 53021 (`AbilityFactory.YouMayPlayCardLikeInHand(..., from_where="YourDiscardPile", during="YourTurn")`,
# play.py:436), `RecruitedMutants` (__init__.py : le deck de table, E2).
# ⚠ La PERMISSION de jouer Blink depuis la defausse Recruited n'est PAS portee par cette carte (une capacite de carte endormie dans une defausse
# n'est pas active) : voir `PermissionDeJouerLesRecrutes` (__init__.py), portee par Xavier's Institute (hf048) et Rally the Survivors (hf045).
def GetAbilities() -> Sequence['Ability']:
    # ⚠ CORRIGE le 01/11/2026 : l'ancienne version (`AfterUnitBeDefeated`, Forced Response) ne partait JAMAIS : au moment de la reponse, Blink est
    # deja dans la defausse du joueur et la capacite d'une carte defaussee dort (cas `hf014 Blink : vaincue` rouge des que le verificateur a ete
    # bien branche : deux fonctions `hf_etat` homonymes, la bonne ecrasee). Meme schema que Wild Sentinel (hf382) : un drapeau a la defaite,
    # puis un REMPLACEMENT du passage en defausse (`WhenCardWouldDiscard` + `SetBeInstead`) qui la remet dans le deck Recruited Mutants.
    def vaincue(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        effect.this.vers_les_recrutes = True

    def a_defausser(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this
        this.vers_les_recrutes = False
        message.SetBeInstead(effect)
        deck, _ = RecruitedMutants(effect)
        Faces.MoveAllTo([this], deck, effect)
        deck.Shuffle(effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        AbilityFactory.WhenCardWouldDiscard(AbilityType.ForcedInterrupt, "This", a_defausser,
                                            conditions=[lambda effect, message: getattr(effect.this, "vers_les_recrutes", False)]),
    ]
