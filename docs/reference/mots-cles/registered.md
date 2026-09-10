# REGISTERED

**Texte imprimé / définition** : pack `iron_patriot` (Neptune, set 142).
Norman Osborn joue avec un SECOND DECK de 20 sbires, le **deck REGISTERED**. Sa
manigance permanente en révèle le dessus ; le sbire entre en jeu **engagé avec
lui**, résout ses effets de révélation, puis le joueur peut dépenser un nombre
de ressources égal à ses **icônes de [boost]** pour en prendre le contrôle et le
traiter comme un **allié REGISTERED**. Insert, mot pour mot :

> « When you reveal a minion from the REGISTERED deck, it enters play as a
> minion first and resolves any revealed effects. After this, you may spend
> resources equal to the number of boost icons on that minion's card to take
> control of it as a REGISTERED ally. If you do not, it remains in play as a
> minion engaged with you. »

⚠ **Ce n'est pas un mot-clé au sens du jeu, c'est un TRAIT** — comme `ELITE`.
Il se déclare dans `traits`, jamais dans `desc`, et le moteur ne lui associe
aucune mécanique native. La fiche existe parce que le pack construit tout un
système autour de lui, et que trois pièges moteur ont coûté une journée.

**Mécanisme moteur** : rien de neuf, tout existait.

| Besoin du pack | Ce qui existe déjà |
|---|---|
| un second deck et sa défausse | `player.additional_deck` / `additional_discard_pile` (`player.py:97`) |
| le remplir au montage | `AbilityFactory.BeginGameWithSetAside` + `WhenPlayerSelectHero` (modèle `09001b` Stephen Strange) |
| révéler le dessus | `Deck.RevealTopCard` → `face.Reveal` (`face_on_event.py:245`) |
| sbire → allié, CTR = MNG imprimée | `Faces.TreatAsAlly` (`faces.py:340`), qui recopie déjà `printed_scheme` dans `printed_thwart` |
| la capacité « Special » | `AbilityFactory.WhenResolveSpecialAbility` pour la déclarer, `face.ResolveSpecialAbility` pour la résoudre |

**Carte exemple** : `ip002a` : * Registration Act, et le helper partagé
`src/cards/pack/iron_patriot/iron_patriot/__init__.py`.

**Pièges connus** — les quatre ont été MESURÉS le 09-10/09/2026 :

1. **`Faces.TreatAsAlly` ÉCHANGE LA FACE, et n'emporte rien avec elle.** Le
   gabarit `registered_ally` n'a aucune capacité et un seul trait. Sans
   correctif, le « Special » qu'on vient de PAYER disparaissait à la seconde
   où on l'obtenait, et Bullseye cessait d'être ASSASSIN. Il faut donc :
   - **recharger le module du sbire** pour obtenir des `Ability` NEUVES —
     celles déjà en place sont liées à leur papier (`face_ability.py:18`) et le
     moteur refuse de les reposer ailleurs (`card.py:316`) ;
   - **recopier les traits imprimés** ;
   - **rallumer les bonus continus** : la famille `WhileValid`
     (`ThisGainKeyword`...) se suspend à `WhenCardEnterPlay` (`on_while.py:177`)
     et n'est jamais calculée si on l'inscrit APRÈS l'entrée en jeu.
   Les mots-clés lus dans `desc` (Garde, Patrouille, Riposte, Vulnérable…), eux,
   tombent avec la face — et c'est voulu : un allié ne garde pas la garde.
2. **Convertir PENDANT le « When Revealed » casse la révélation.** Le sbire
   n'est alors plus engagé, et `minion.py:41` l'exige
   (`assert self.card.world.is_game_over, f"{self.engaged_player=}"`). On se
   pose une fenêtre plus tard, sur `AfterCardRevealedEnd`.
3. **Le prix est en ICÔNES DE BOOST, pas en coût de ressource.** Aucune carte
   qui réduit un coût ne touche le deck REGISTERED ; une carte qui change les
   icônes, si (`ip008` Director of Security). Lire par
   `CountBoostIconsInternal`, jamais `printed_boost`.
4. **La défausse se sépare en deux, contre l'intuition.** Insert : un ALLIÉ
   REGISTERED vaincu part dans la défausse du deck REGISTERED, un SBIRE du deck
   REGISTERED resté sbire part dans la défausse de RENCONTRE. Le test est
   `HasTrait("REGISTERED")` au moment de la défaite.

**Variantes maison** : aucune à ce jour. À ne pas confondre avec le trait
`CONTROLLED` (packs `rogue`, `phoenix`), qui prend aussi le contrôle d'un sbire
mais lui **interdit** d'utiliser ses capacités — l'insert d'Iron Patriot oppose
explicitement les deux.
