from . import *

# * Spider-Man (Peter Parker) — ALLIE, cout 3, [wild]. SYMBIOTE. WEB-WARRIOR.
#   PV 4, CTR 2, ATQ 2 — AUCUN DEGAT CONSECUTIF IMPRIME (voir plus bas).
# [star] Forced Interrupt: When Spider-Man uses a basic power, discard the top
#   card of the encounter deck. For each boost icon ([boost]) discarded this
#   way, he gets +1 to that power for that use and takes +1 consequential
#   damage.
#
# ⚠ CETTE CARTE ET `bc003` SONT DEUX VERSIONS DU MEME NUMERO DE SET
# (« BLACK CAT 1/15 »), toutes deux nommees « * Spider-Man ». Statistiques,
# traits et capacites DIFFERENTS : deux `card_id`. C'est `bc003` qui porte le
# mot-cle `Multiverse` — fiche `docs/reference/mots-cles/multiverse.md`, creee
# pour ce pack, ZERO ligne de code.
#
# ⚠ « * Spider-Man » EXISTE QUINZE FOIS AU DEPOT (`01001a` en tete). Aucun
# `CardFinder(name=...)` ici : la carte ne parle que d'elle-meme (`"This"`).
#
# CARTES DE REFERENCE
#  - `bw003` * Ironheart (pack brawn, meme famille d'allie alternatif) : la
#    capacite branchee sur les pouvoirs de base d'un allie.
#  - `Message.WhenUnitUseBasicPower.GainValue` (sender_unit.py:21) : LA
#    primitive qui rend « +1 to THAT POWER for that use » sans savoir lequel
#    des quatre c'est. Elle aiguille seule vers `GainATKForThisAttack`,
#    `GainTHWForThisThwart`, `GainDEFForThisAttack` ou
#    `GainRECForThisRecover`.
#  - `33016` Coordinated Attack (pack cyclops) :
#    `ally.GainForThisActive(effect, message, attack_consequential_damage=-1)`,
#    la seule voie propre pour changer les degats consecutifs d'un allie sur
#    UN pouvoir. La carte de Cyclope les BAISSE de 1, celle-ci les MONTE.
#
# TEXTE CONTRE CODE
#  ⚠ « For each BOOST ICON ([boost]) » -> LES ICONES CHIFFREES SEULEMENT.
#    C'est la SEULE carte du pack avec `bc008` a ne PAS ecrire
#    « ([star] and [boost]) », et l'ecart est imprime : on emploie donc
#    `IconesSeules`, pas `IconesEtEtoiles`.
#  ⚠ « to THAT POWER » -> celui qui est en cours, pas ATQ par defaut.
#    `message.GainValue` le sait ; un `GainATKForThisAttack` ecrit en dur
#    aurait fait un contre a +0.
#  ⚠ « FOR THAT USE » -> le bonus ne survit pas au pouvoir. C'est exactement
#    la portee des `Gain...ForThis...`, qui vivent dans le message d'usage.
#  ⚠⚠ CETTE CARTE N'A AUCUN DEGAT CONSECUTIF IMPRIME. Le bloc de
#    statistiques porte « 2★ » — l'etoile de la capacite Special — et PAS
#    l'eclat des degats consecutifs, que `bc003` porte, lui. Verifie par
#    DECOUPE D'IMAGE des deux blocs cote a cote, jamais a vue (lecon Lockjaw).
#    Dans les donnees, l'eclat s'ecrit avec un ASTERISQUE dans la valeur
#    (`can_attack.py:47-52`, `value.count('*')`) : d'ou `"ATK": "2"` ici et
#    `"ATK": "2*"` sur `bc003`.
#    CONSEQUENCE DIRECTE SUR LE CODE : `WhenAllyWouldTakeConsequentialDamage`
#    n'est envoye QUE si la valeur imprimee est deja > 0 (ally.py:41-46). Sur
#    cette carte elle vaut 0 : un temp accroche a ce message ne serait JAMAIS
#    parti, et le cas de test serait reste vert en ne mesurant rien. On
#    augmente donc la VALEUR, pas le message.
#  ⚠ Les degats consecutifs n'existent que pour ATQ et CTR (ally.py:60,
#    `powers=["ATK","THW"]`). Sur une DEFENSE, la moitie « +1 degat » ne tombe
#    donc pas — et c'est le moteur qui le dit, pas nous.
#  « discard the top card of the encounter deck » -> inconditionnel, meme si
#    la carte n'a aucune icone : la defausse a lieu quand meme.


def GetAbilities() -> Sequence['Ability']:

    def symbiote(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)

        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return
        # « For each BOOST ICON ([boost]) » : sans l'etoile.
        bonus = IconesSeules([face])
        if bonus <= 0:
            return

        # « he gets +1 to THAT POWER for that use »
        message.GainValue(bonus, effect)

        # « and takes +1 consequential damage »
        # ⚠ PAS `WhenAllyWouldTakeConsequentialDamage.IncreaseDamage` : ce
        # message n'est envoye QUE si l'allie a deja des degats consecutifs
        # IMPRIMES (`ally.py:41-46`, garde `> 0`). Or cette carte-ci n'en a
        # AUCUN — son bloc de statistiques ne porte pas l'eclat, contrairement
        # a `bc003`. Un temp accroche a ce message ne se serait donc JAMAIS
        # declenche, et le cas serait reste vert en ne mesurant rien.
        # On AUGMENTE la valeur elle-meme, modele `33016` Coordinated Attack
        # (qui la baisse de 1 par le meme appel), borne au pouvoir en cours.
        this.GainForThisActive(
            effect,
            message.would_message,
            attack_consequential_damage=bonus,
            thwart_consequential_damage=bonus,
        )

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.ForcedInterrupt,
            "This",
            symbiote,
        ),
    ]
