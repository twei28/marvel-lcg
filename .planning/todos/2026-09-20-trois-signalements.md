# Trois signalements du 20/09/2026

Lus en production le 20/09 au soir (`rapports` 18, 19, 20). Aucun n'est traité.
Les deux d'Aghenatak sont **le même défaut**, pas deux.

---

## A. Deux cartes restent coincées « en résolution » (n°19 et n°20)

**Ce que le joueur voit.** « Squirrel Girl a été jouée comme un support.
Impossible de l'activer d'aucune manière, ni de la défausser. » Puis :
« Piecing all together a été joué comme un support. Impossible de le contrer. »

**Ce que dit le journal, et c'est net.** Les deux rapports viennent de la MÊME
partie (Jessica Jones contre Dark Beast's Bogus Journey, round 13,
`render_id` 1845), et portent tous deux le même état de table :

```
c16 Piecing It All Together (61007, PlayerSideScheme, en résolution)
c41 Squirrel Girl           (61017, Ally,             en résolution)
```

« En résolution » est la **zone de traitement** du moteur
(`world.area_processing`), celle où une carte transite pendant qu'elle se
résout. Les deux y sont restées. C'est pour ça que rien ne marche sur elles :
elles ne sont ni en jeu, ni en défausse, elles sont en transit. Le joueur les
voit posées sur la table et les prend pour des soutiens, ce qui est une lecture
raisonnable de ce qu'il a sous les yeux.

**Ce n'est donc pas deux bugs de carte, c'est un bug de séquence de jeu**, et
les deux cartes appartiennent au paquet Jessica Jones (61xxx), le héros joué.

**Piste, à vérifier.** `PlayAnAlly` et `PlayACard`
(`src/game/player/action/player_action.py:811` et `:847`) font, dans le cas
« mise en jeu GRATUITE » :

```python
Faces.MoveAllToProcessingArea([ally], effect)
return ally.Play(player, effect, message, Resources("0"), from_area, False)
```

Si `Play` n'aboutit pas, **rien ne ramène la carte**. Elle reste où le premier
appel l'a mise. Ce chemin est celui d'une carte mise en jeu par l'effet d'une
autre, pas d'une carte jouée depuis la main en payant son coût.

**Ce qui manque pour conclure.** Le journal du rapport ne remonte pas jusqu'au
round où les deux cartes sont entrées : la fenêtre retenue commence au round 4
et le seul événement conservé est `R6 {c41} Squirrel Girl défaussé / P1`, qui
est probablement une tentative de défausse restée sans effet, pas sa mise en
jeu. Il faut reproduire : Jessica Jones, et une mise en jeu gratuite de chacune
des deux cartes.

**Aucune exception côté serveur** (`journalctl` du 20/09 à partir de 15 h :
zéro `Traceback`). Le moteur n'a pas planté, la séquence s'est arrêtée
proprement au mauvais endroit.

⚠ Le paquet `jj` n'a **aucun fichier de test** dans `tools/`.

---

## B. SP//dr : payer avec la capacité avant la main fait PERDRE la carte (n°18)

**Yarro, et sa description est exemplaire** : elle contient le défaut ET le
contournement.

> « Quand tu veux payer le coût pour jouer une carte, tu peux incliner une
> interface pour générer une ressource. Cela fonctionne mais il faut respecter
> un ordre précis si tu as un mix entre payer de ta main et payer avec la capa
> d'SP//dr. En gros si tu fais un mix et que tu choisis d'abord de payer par la
> capa, et que par exemple pour une carte qui coûte 2 tu n'inclines qu'une
> interface, il va te l'incliner et mettre la carte que tu veux en défausse.
> Pour jouer la carte il faut d'abord payer une carte de ta main et ensuite
> déclencher la capa. »

**Ce que ça veut dire.** Un paiement incomplet n'est pas annulé : la ressource
est consommée (l'interface reste inclinée) ET la carte part à la défausse sans
avoir été jouée. Le joueur perd la carte et la ressource.

**Pourquoi c'est sérieux.** Ce n'est pas un défaut d'affichage ni une gêne :
c'est une **perte sèche de matériel** au milieu d'un tour, sur un ordre de
clics que rien n'interdit à l'écran. Et le contournement n'est devinable par
personne.

Journal du rapport : 308 lignes, héros SP//dr Suit, les lignes 54 à 61 montrent
bien l'alternance `gains resource` / `exhausted` pendant un paiement.

---

## C. Ce qu'il reste à faire

1. Reproduire A avec Jessica Jones, sur les deux cartes, et trouver pourquoi
   `Play` n'aboutit pas. Écrire le cas qui manque.
2. Reproduire B : jouer une carte à coût 2 en inclinant l'interface AVANT de
   défausser une carte de la main. Vérifier qu'un paiement incomplet rend la
   ressource et ne défausse rien.
3. Répondre aux deux joueurs. Yarro attend depuis le 19/09 au soir sur un
   autre sujet (Echo), et depuis le 20/09 à 13 h 34 sur celui-ci.
