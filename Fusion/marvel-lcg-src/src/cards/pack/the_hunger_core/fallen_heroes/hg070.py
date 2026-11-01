from . import *

# Zombie Falcon — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). AVENGER. SCH 1. ATK 1.
# PV 4. Guard. Villainous. Boost 1.
# Guard. Villainous.
# This minion cannot be attacked by allies.
# When Revealed: Exhaust your identity; it is stunned.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, `desc.Guard` = "1". Aucun script requis.
# - [[villainous]] (mots-cles/villainous.md) : BASE NATIVE, `desc.Villainous` = "1". Aucun script requis.
# - « Stunned » (Etourdi) : statut DE BASE du moteur (comme Confused), pas un mot-cle maison ni officiel a
#   ficher -- meme heuristique deja retenue sur `hg010` Zombie Spider-Man (meme pack) : seuls les termes
#   imprimes EN GRAS sont catalogues dans `mots-cles/`, « stunned » ne l'est pas ici.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « This minion cannot be attacked by allies » : `*AbilityFactory.UnitCannotAttackTarget(Ally,
#   cannot_attack="This")`, modele EXACT `49039` Selene (Hellfire, deck Magneto) : « Allies cannot attack X »
#   -> meme fabrique, meme forme (`cannot_attack="This"`, attaquant restreint = `Ally`) ; meme lecture deja
#   confirmee sur `gs132` Majestrix's Verdict (« Allies cannot attack X » -> `UnitCannotAttackTarget(Ally,
#   cannot_attack=Villain)`, seule la CIBLE differe : un Villain nomme la-bas, "This" ici puisque la restriction
#   porte sur CETTE carte precise, pas sur tout vilain de la table).
# - « When Revealed: Exhaust your identity » : `AbilityFactory.WhenThisRevealed(None, ...)` +
#   `Faces.ExhaustAll([identite], effect)`, modele EXACT `01191` Exhaustion (« When Revealed: Exhaust your
#   identity card » -> meme paire fabrique/appel, meme usage de `message.GetToPlayer()` pour resoudre « your »
#   = le joueur a qui/avec qui cette carte a ete revelee -- deja confirme sur `45065` Infinite Hunter, un
#   MINION comme hg070, pas seulement sur une Treachery).
# - « ...; it is stunned » (suite de la meme phrase, meme capacite) : `Faces.GiveStatus([identite], "Stunned",
#   effect)`, modele EXACT `hg010` Zombie Spider-Man (meme pack, meme appel natif pour poser Etourdi).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. Villainous. » -> natifs, rien a coder.
# « This minion CANNOT BE ATTACKED BY ALLIES » : restriction au cote ATTAQUANT (Ally seulement) -- le
#   heros/l'identite attaquante PEUT toujours attaquer Zombie Falcon normalement ; si le texte avait dit
#   « cannot be attacked » (sans « by allies »), le modele aurait ete `UnitCannotBeAttacked` generique (sans
#   filtre d'attaquant) -- ici il nomme explicitement « allies », modele Selene/Majestrix's Verdict.
# « When Revealed » -> `WhenThisRevealed`, declencheur a la revelation de CETTE carte (sbire pioche depuis le
#   deck de rencontre).
# « Exhaust YOUR identity » : « your » = le joueur a qui cette carte a ete revelee (`message.GetToPlayer()`),
#   jamais un joueur fixe par le code ni Zombie Falcon lui-meme (qui n'a pas d'identite).
# « ; IT is stunned » : « it » = l'identite QUI VIENT D'ETRE EXHAUST (la MEME carte que celle nommee juste
#   avant, piege « that <nom> » du gabarit PROCESSUS-CARTE) -- jamais Zombie Falcon, jamais un autre
#   personnage controle par ce joueur (pas « each ally », seulement l'identite). Les deux effets de la phrase
#   (exhaust, puis stun) s'appliquent donc a la MEME carte, dans l'ORDRE imprime (exhaust d'abord, stun
#   ensuite) -- sans consequence pratique sur l'ordre ici (aucun des deux appels ne depend de l'etat pose par
#   l'autre), mais le code suit le texte dans l'ordre par coherence et tracabilite.
#
# A CONFIRMER : aucune autre carte du depot n'a ete trouvee combinant EXACTEMENT « exhaust your identity » et
# « it is stunned » dans la MEME phrase de When Revealed d'un MINION (les occurrences officielles grep'ees
# combinent plutot exhaust/stun comme alternatives d'un choix, ex. `mw013` Spider-Woman « Choose to either
# take 2 indirect damage or exhaust your identity », jamais les deux en sequence obligatoire) -- lecture
# retenue, au mot pres du texte imprime (« ; » lu comme une suite, pas une alternative) : les deux effets sont
# OBLIGATOIRES et s'appliquent l'un apres l'autre, sans choix du joueur. Aucune autre lecture plausible
# identifiee.
#
# Bloc nombres texte <-> code : aucune valeur numerique imprimee sur cette carte (ni `desc` au-dela de SCH/
# ATK/HP/Guard/Villainous/Boost, ni coefficient dans le script) -- rien a verifier a l'etape 6.


def GetAbilities() -> Sequence['Ability']:

    def falcon_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        identite = joueur.GetIdentity()
        Faces.ExhaustAll([identite], effect)
        Faces.GiveStatus([identite], "Stunned", effect)

    return [
        *AbilityFactory.UnitCannotAttackTarget(
            Ally,
            cannot_attack="This",
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            falcon_revele,
        ),
    ]
