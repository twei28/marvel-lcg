from . import *

# Hyper-Agility — AMELIORATION, cout 1 [physical]. CONDITION. SUPERPOWER.
# Your hero gets +1 DEF.
# Hero Response: After you resolve your hero's Acceleration ability WITHOUT
#   PLAYING AN EVENT, reduce the damage you take from attacks by 1 until the
#   end of the round. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `ab007` * Donald Pierce : reagir a une capacite nommee portee par une
#    AUTRE carte, `WhenResolveSpecialAbility(CardFinder(...), op)`. Ici sur le
#    message `NOM_ACCEL_FINI`, que `sm001a` envoie APRES coup — c'est ce qui
#    donne son sens au « After » et permet de savoir si un evenement a ete
#    joue (RECETTES : l'ordre entre effets d'un meme message n'est pas
#    garanti, d'ou deux messages distincts).
#  - `50159`, `16098`, `21117` : reduire les degats subis =
#    `WhenUnitWouldTakeDamage(..., op)` + `message.ReduceDamage(n, effect)`,
#    la brique derriere `ReduceCharacterTakeDamageBy`.
#  - `ab001a` : `RegisterTemp(..., until_round_end=True)` pour « until the end
#    of the round ».
#  - `an008`, `ho008` : « Your hero gets +1 DEF ».
#
# TEXTE CONTRE CODE
#  ⚠⚠ « WITHOUT PLAYING AN EVENT » : c'est CETTE carte qui distingue les trois
#    ecoutes du pack. `sm011` Spinnerets et `sm012` Web Cape partent apres
#    TOUTE resolution d'Acceleration ; Hyper-Agility exige que la resolution
#    n'ait joue AUCUN evenement — deck vide, aucun evenement trouve, ou
#    evenement trouve mais non joue. Trois portees, trois conditions
#    differentes : les lire mot a mot.
#  ⚠ « reduce the damage YOU take FROM ATTACKS » : les degats subis par
#    l'identite, et seulement ceux d'attaques (`is_from_attack=True`) — pas
#    les degats indirects de la nemesis, qui sont justement le danger du pack.
#  ⚠ « UNTIL THE END OF THE ROUND », pas « until the end of the phase » :
#    `until_round_end=True`.
#  ⚠ « Limit once per phase » -> `LimitOncePerPhase()`, ET RIEN D'AUTRE.
#    ⚠⚠ CORRECTIF DU 09/09/2026 — LA CARTE ETAIT MORTE. Un comptage maison
#    (`pas_encore_cette_phase`) doublait cette limite « par precaution ». Il
#    lisait `world.stat.once_per_phase_player_effects` — LE REGISTRE QUE
#    `LimitOncePerPhase` REMPLIT ELLE-MEME, et des le declenchement. La
#    condition etait donc FAUSSE des le premier passage : `esquiver` n'a jamais
#    tourne, et la reduction de degats n'a jamais existe. Mesure du 09/09/2026,
#    avec un compteur pose dans `esquiver` : `sonde_sm010=absent`, l'identite
#    encaisse 6 des 6 degats de deux attaques de Sandman. Condition RETIREE :
#    l'ability seule reduit bien (4 degats sur 6, cas « la reduction MORD »).
#    Lecon : une precaution qui n'est pas mesuree n'est pas une precaution.
#    ⚠ ET SA LIMITE EST INATTEIGNABLE PAR CONSTRUCTION, ce qui est desormais
#    MESURE et non suppose (cas « TEMOIN D'EPUISEMENT ») : l'Acceleration de
#    `sm001a` porte DEJA « Limit once per phase », donc il n'existe pas de
#    seconde resolution dans la meme phase a laquelle cette carte pourrait
#    reagir. Le temoin le prouve par deux chiffres : `sm011` ne porte qu'UN
#    pion de toile apres DEUX pouvoirs de base, et l'identite encaisse le
#    montant d'UNE seule reduction.
#  ⚠ « Your hero gets +1 DEF » : meme remarque que `sm009`, la DEF n'existe
#    pas en forme civile. Contre-cas dans l'autre forme du.


def GetAbilities() -> Sequence['Ability']:

    def sans_evenement(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> bool:
        """« WITHOUT PLAYING AN EVENT » : aucun evenement joue par la
        resolution qui vient de s'achever. Le marqueur du pack est remis a
        zero a l'ouverture de chaque Acceleration, il ne peut donc pas garder
        la trace d'une resolution precedente."""
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return EvenementJoueParAcceleration(joueur) is None

    def esquiver(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if identite is None or joueur is None:
            return

        # ⚠ RECETTES §1 : le registre NE S'ALIMENTE PAS TOUT SEUL. Lire une
        # limite sans jamais l'inscrire revient a ne poser aucune limite
        # (lecon `gb020` You Are My God).
        effect.world.stat.RecordEffectWithPlayer(effect, joueur)

        # ⚠ CORRECTIF DU 09/09/2026 — LA REDUCTION NE PARTAIT JAMAIS.
        # Le premier parametre de `WhenUnitWouldTakeDamage` est un
        # `CardType|Literal["You"]` que `Condition.GetYouRule` interprete
        # (damage.py:23) ; un `CardFinder(check_face_fn=...)` n'y survit pas, et
        # l'ability, pourtant enregistree, ne se declenchait sur aucune attaque.
        # Mesure du 09/09/2026 : Sandman frappe deux fois pour 3, l'identite
        # encaisse 6 alors que `sm010` est en jeu et que son effet est BIEN
        # inscrit au registre `once_per_phase_player_effects`. Le modele qui
        # marche est celui de `su003` Agility et de `50159` : `"You"` nu.
        # ⚠ Aucune gate ne pouvait le voir : la carte n'avait pas de cas sur sa
        # reduction, faute de savoir empecher la defense (voir le cas
        # « la reduction MORD »).
        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                "You",
                lambda e2, dmg_message: dmg_message.ReduceDamage(1, e2),
                is_from_attack=True,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        *AbilityFactory.GiveKeywordToAttached(
            # ⚠ `Hero` et non `"You"` : le texte dit « YOUR HERO gets ». Sur
            # cette carte-ci la nuance est invisible (ni ATQ ni DEF n'existent
            # en alter-ego), mais `sm012` Web Cape a montre le 08/09/2026 que
            # `"You"` fait bien fuir le bonus sur l'autre face — on s'aligne.
            Hero,
            defense=1,
        ),

        AbilityFactory.WhenResolveSpecialAbility(
            CardFinder(card_ids=[ID_HEROS]),
            esquiver,
            conditions=[sans_evenement],
        ).SetName(NOM_ACCEL_FINI)
        .LimitOncePerPhase(),
    ]
