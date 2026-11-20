# Starjammers Aspects : doutes réels restants (26/10/2026)

Règle suivie : règles (Rules Reference v1.8) puis carte. Il ne reste que les cas où le texte imprimé est contradictoire ou où le moteur ne peut pas rendre le texte tel quel.
L'option A est celle qui est CODÉE ; la carte reste « Carte terminée : NON (provisoire) ».

1. **sy002 Corsair (allié), `images : assets/pics/sy002.jpg`** : « **Interrupt**: **After** you play Corsair from your hand, tuck each card you used to pay for him under here. »
   Une Interruption part AVANT l'événement, « After » veut dire après. Le modèle officiel 53018 Spectrum imprime « Response » pour ce même texte.
   - A (codé, recommandé) : Réponse, après que Corsair est joué.
   - B : Interruption, quand il est joué (les cartes payées sont glissées avant son entrée en jeu).
2. **sy027 Freedom Fighters** (`sy027.jpg`) : « **Response** (thwart): **When** the villain activates against a player, exhaust ... → **cancel** that activation. »
   Une Réponse part après l'activation : on ne peut plus l'annuler.
   - A (codé, recommandé) : Interruption (annule l'activation, puis retire X menaces).
   - B : vraie Réponse après l'activation : seule la partie « retirez X menaces » s'applique, rien n'est annulé.
3. **sy037 Far-Flung Family** (`sy037.jpg`) : « **as a group**, the players search their decks for a total of 1 STARJAMMER ally and 1 X-MEN ally ».
   Le moteur n'a pas de fouille collective ; en solo c'est sans effet.
   - A (codé, recommandé) : les joueurs, dans l'ordre, cherchent chacun dans son deck ce qui manque encore (un allié STARJAMMER et X-MEN comble les deux lignes).
   - B : seul le joueur qui a joué la carte cherche, dans son deck.
4. **sy043 Thorn Crew / sy042 Kalyx** (`sy043.jpg`) : « Each facedown THORN ally has a base THW 1, ATK 1, hit points 1 ». Le moteur n'a pas de PV/CTR de base pour un allié face cachée.
   - A (codé) : le gabarit d'allié face cachée `sy_thorn_ally` porte déjà ATQ 1, CTR 1, PV 1 (l'effet vaut donc même si Thorn Crew quitte le jeu).
   - B : exiger Thorn Crew en jeu (extension moteur à écrire).
5. **Textes imprimés avec coquille, recopiés tels quels** : sy010 « Centre Section Garden » dans le texte contre « Center » dans le titre ; sy026 Polaris « give **a** her a tough status card » (lu « give her ») ; sy045 Tolo Hawk « **Thowing** it away » (citation).
6. **Cartes Linked dans le deck-builder** : sy018 Blade of the Phoenix (classe Agressivité) et sy043 Thorn Crew (classe Protection) sont `Linked` (mises de côté par leur carte), mais le deck-builder ne cache pas les cartes liées de classe d'aspect (précédent officiel : classe Basic). Un joueur pourrait donc les glisser dans son deck. Faut-il les masquer ?

## Décisions (26/10/2026)

- **1. sy002 Corsair** : décision de l'utilisateur, carte montrée : A (Réponse, après que Corsair est joué). Déjà codé.
- **2. sy027 Freedom Fighters** : décision de l'utilisateur, carte montrée : A (Interruption, annule l'activation puis retire X menaces). Déjà codé.
- **3. sy037 Far-Flung Family** : tranché par les règles, A (les joueurs cherchent chacun ce qui manque encore ; en solo, le même résultat).
- **4. sy043 / sy042 Thorn Crew et Kalyx** : tranché, A (gabarit d'allié face cachée `sy_thorn_ally` ATQ 1 / CTR 1 / PV 1). Le moteur n'a pas de valeurs de base conditionnelles.
- **5. Coquilles imprimées** : recopiées telles quelles, pas de question.
- **6. Cartes Linked (sy018 Blade of the Phoenix, sy043 Thorn Crew)** : tranché par la règle Linked (la carte est mise de côté par sa carte liée, elle ne fait pas partie du deck) : à MASQUER dans le deckbuilder. À FAIRE (voir `docs/rapports/2026-10-26-problemes-a-corriger.md`).
