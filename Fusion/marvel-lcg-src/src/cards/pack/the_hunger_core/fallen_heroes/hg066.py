from . import *

# Zombie Thing — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). FANTASTIC. SCH 0. ATK 2.
# PV 7. Guard. Boost 3.
# Guard.
# When Revealed: This minion gets 2 tough status cards. It can have 2 tough status cards at the same time.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, lue depuis `desc.Guard` ("1"). Aucun script requis.
# - [[toughness]] (mots-cles/toughness.md) : la carte n'imprime PAS "Toughness." elle-meme (contrairement a
#   hg059/hg069) -- aucun `desc.Toughness` sur hg066 (verifie dans `cards_custom.json`, seules les cles SCH/
#   ATK/HP/Guard/Boost y figurent). Le texte parle de "tough status cards" (la CARTE D'ETAT elle-meme), pas
#   du mot-cle Toughness (qui ne fait qu'EN DONNER UNE A L'ENTREE EN JEU) : deux notions distinctes du meme
#   lexique, Zombie Thing n'a que la seconde, geree a la main ci-dessous.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « It can have 2 tough status cards at the same time » : plafond `tough_max` (`can_status.py`, propriete
#   calculee via le message `Message.GettingUnitAdditionalTough`) -> `AbilityFactory.ThisCanHaveAdditionalTough
#   (1)` (1 carte EN PLUS du plafond de base = 1, total 2), modele EXACT `62001a` Luke Cage / `32001a` Colossus
#   (« can have up to N tough status cards »), et commentaire-modele deja laisse sur
#   `tmnt_aspect_protection/up016.py` Herman (meme fabrique, meme lecture « up to 3 » = base 1 + 2).
# - « This minion gets 2 tough status cards » (a la revelation) : `AbilityFactory.WhenThisRevealed` (meme
#   fabrique que `hg028`/`hg029`, ce pack) + boucle `Faces.GiveStatus([this], "Tough", effect)` deux fois,
#   modele structurel `up016.py` Herman (boucle `for _ in range(valeur): Faces.GiveStatus(...)`, ou `valeur`
#   y est variable -- ici fixe a 2, imprime en dur) ; la seconde pose n'est acceptee par `GainStatus` QUE parce
#   que `ThisCanHaveAdditionalTough(1)` a deja releve `tough_max` a 2 AVANT que cette ability ne s'execute
#   (meme ordre que Herman : la carte "peut avoir" d'abord, "recoit" ensuite, les deux abilities coexistent
#   sans dependance d'ordre d'enregistrement puisque `tough_max` est une PROPRIETE recalculee a chaque appel
#   de `GainStatus`, pas une valeur figee a l'enregistrement de l'ability).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. » -> natif (`desc.Guard`), rien a coder.
# « When Revealed » -> `AbilityFactory.WhenThisRevealed(None, ...)`, declencheur a la revelation de CETTE carte
#   (sbire pioche depuis le deck de rencontre, pas depuis un deck signature).
# « This minion gets 2 TOUGH STATUS CARDS » -> deux appels `Faces.GiveStatus([this], "Tough", effect)`, PAS
#   un seul appel avec un parametre de quantite (`GiveStatus` ne pose qu'UNE carte par appel, verifie sur tous
#   les modeles grep (Herman, Tiger Shark, Vibranium Armor...) : aucune fabrique native ne prend de compte en
#   argument).
# « It can have 2 tough status cards AT THE SAME TIME » -> `ThisCanHaveAdditionalTough(1)`, PERMANENT (pas
#   limite a la revelation : la carte reste plafonnee a 2 tant qu'elle est en jeu, meme si elle perd puis
#   regagne des cartes Tough plus tard dans la partie par un autre effet du scenario).
#
# A CONFIRMER : aucune autre carte du depot ne pose DEUX cartes Tough EN MEME TEMPS a la revelation (modele le
# plus proche, Herman, pose un nombre VARIABLE selon le surpaiement, jamais un "2" fixe imprime tel quel) --
# lecture retenue : deux appels distincts a `GiveStatus`, strictement equivalente au texte imprime, aucune
# autre lecture plausible identifiee.
#
# Bloc nombres texte <-> code : "2" (nombre de cartes Tough donnees) -> `range(2)` dans le script ; "2" (le
# plafond, "at the same time") -> `ThisCanHaveAdditionalTough(1)` (1 carte EN PLUS du plafond de base 1 =
# 2 au total, `CanStatus.BASE_MAX_TOUGH = 1`, `can_status.py:4`). Les deux "2" imprimes sont donc bien
# distincts dans le code (un compte d'actions, un plafond), mais leur valeur numerique coincide par construction
# (on ne peut pas accumuler plus de cartes que le plafond autorise au moment ou on les donne).


def GetAbilities() -> Sequence['Ability']:

    def zombie_thing_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        for _ in range(2):
            Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.ThisCanHaveAdditionalTough(1),
        AbilityFactory.WhenThisRevealed(
            None,
            zombie_thing_revele,
        ),
    ]
