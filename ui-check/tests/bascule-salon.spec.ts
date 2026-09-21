// LA PARTIE QUI COMMENCE EST-ELLE LA MIENNE ? La question du salon, eprouvee
// sur le vrai module.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Le 20/09/2026, deux fois dans la meme soiree,
// des invites ont ete expedies dans la partie PRECEDENTE avant d'avoir choisi
// leur heros, et y sont restes bloques sur « Connexion a la partie... ».
// `surveillerLeLancement` basculait des que `/get_play_scene_name` rendait
// autre chose qu'une chaine vide, sur l'hypothese — ecrite en commentaire —
// que la table est VIDE avant le lancement. Elle ne l'est pas : le moteur rend
// le nom de scene des qu'un monde existe, et il en existe un jusqu'au
// redemarrage.
//
// ⚠⚠ ET LE HEROS SEUL NE SUFFIT PAS (ronde de correction du 21/09/2026) : voir
// le cas « meme heros a la manche suivante » plus bas, qui rouvrait le defaut
// en grand. Il faut DEUX signaux : le heros (« ce siege est a moi ») et la
// fraicheur (« cette partie a commence apres que je me suis pose »).
//
// Meme moule que sondage-salon.spec.ts : des fonctions PURES, appelees dans la
// page sur le vrai module, sans moteur derriere.
//   npm run bascule-salon
import { test, expect, type Page } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
});

type Etat = {
  monChoix?: string;
  sansChoix?: boolean;
  debutAuChoix?: string | null;
  enJeu: boolean;
  heros?: string;
  debut?: string;
  attenteDepuis?: number | null;
  maintenant?: number;
};

/** Appelle la fonction PURE du vrai module, dans la page. */
async function decision(page: Page, etat: Etat) {
  return page.evaluate(async (e) => {
    const mod: any = await import('/js/salon/bascule.js');
    return mod.decisionSalon({
      monChoix: '', sansChoix: false, debutAuChoix: null, heros: '', debut: '',
      attenteDepuis: null, maintenant: 0, ...e,
    });
  }, etat);
}

// Deux identifiants de carte heros, comme le salon les manipule : c'est
// `heroCardId` qu'il envoie a `/set_choix_siege`, et c'est lui que la partie en
// cours rend pour le siege.
const SPIDER_MAN = '01001a';
const SHE_HULK = '05001a';

// Les reperes de partie, tels que le moteur les rend : `game_uid:game_id`, la
// meme cle que le plateau utilise deja pour savoir si son journal appartient
// encore a la partie affichee (`clePartie`, ui-app/src/board/moteur.ts).
const MANCHE_1 = '19a3f2c41b0:7';
const MANCHE_2 = '19a3f30d9e8:8';

/* ================= 1. L'ancienne partie encore chargee ================= */

// ⚠ LE CAS DU 20/09, CELUI QUI A BLOQUE LA SOIREE. Une partie de la manche
// precedente est encore chargee (l'hote a clique « Retour au menu » sur l'ecran
// de fin, ce qui ne ferme rien) et l'invite vient d'arriver : il n'a RIEN
// choisi. L'ancienne regle basculait ici.
test('ancienne partie chargee, rien de choisi : on ne bascule pas', async ({ page }) => {
  expect(await decision(page, {
    enJeu: true, heros: SPIDER_MAN, debut: MANCHE_1,
  })).toBe('attendre');
});

test('ancienne partie chargee, choix fait, autre heros : on ne bascule pas', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

// ⚠⚠ LE SEPTIEME CAS, ET C'EST EXACTEMENT LE CHEMIN QUE CE CORRECTIF VISE.
// Le heros SEUL ne suffit pas, et c'est ce cas qui le prouve.
//
// Deroule : on joue la manche 1, ecran de fin, « Retour au menu » (qui ne ferme
// rien), l'hote relance. Entre les deux, le moteur porte encore le monde de la
// manche 1, avec le heros de l'invite a son siege. `/new` a vide `choix_sieges`,
// donc l'invite re-choisit — et il reprend LE MEME HEROS, ce que fait la
// majorite des joueurs. Son siege tient donc « son » heros dans l'ANCIENNE
// partie, et la regle du heros seul l'y expediait. Le 20/09 a l'identique.
//
// Aucune memoire n'est en cause : le choix est refait en direct. C'est la
// FRAICHEUR, et elle seule, qui tranche.
test('meme heros a la manche suivante : on ne repart pas sur l ancienne', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

// ... et le temoin qui prouve qu'on n'a pas simplement tout bloque : des que
// l'hote lance vraiment, le repere change et la bascule se fait.
test('meme heros, manche vraiment lancee : on bascule', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('basculer');
});

/* ================= 2. Le lancement ================= */

test('l hote lance : le siege tient MON heros, on bascule', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('basculer');
});

test('aucune partie en cours : on attend', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: false, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

/* ================= 3. Le rechargement ================= */

// ⚠ LE CAS QUI AVAIT FAIT ECARTER LE COMPTEUR DE GENERATION SEUL. Un invite qui
// recharge sa page perdrait un repere releve « en arrivant ». Ici le repere est
// releve AU MOMENT DU CHOIX et voyage AVEC lui dans la memoire du navigateur :
// il survit donc au rechargement. Les cas de memoire plus bas le prouvent.
test('rechargement pendant l attente : on continue d attendre', async ({ page }) => {
  // La table porte toujours la manche 1, comme au moment du choix.
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

test('rechargement APRES le lancement : on bascule, on ne reste pas coince', async ({ page }) => {
  // Le serveur a vide les choix de siege au lancement : le choix ET le repere
  // relus viennent de la memoire du navigateur.
  expect(await decision(page, {
    monChoix: SPIDER_MAN, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('basculer');
});

/* ================= 4. Deux parties du meme scenario ================= */

// `get_play_scene_name` rend le meme texte dans les deux : un nom de scene ne
// distinguerait rien. Le repere, lui, distingue — meme quand le heros ne
// distingue pas non plus (cas 7 ci-dessus).
test('deux parties du meme scenario : le repere tranche, pas le scenario', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('basculer');
});

/* ================= 5. Lance sans ce siege ================= */

// ⚠ LE CAS QUI N'ETAIT PAS DANS LA LISTE. L'hote a envoye trois liens et lance
// a deux : ce siege n'a PAS de heros dans la partie qui commence. Sans ce cas,
// l'invite attendrait indefiniment devant un ecran qui ne dit rien.
//
// Grace au repere, ce n'est plus une devinette a 45 s : la partie est NEUVE et
// mon siege n'y est pas, donc on peut l'affirmer tout de suite.
test('lance sans ce siege : on l affirme, et tout de suite', async ({ page }) => {
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: '',
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('sans-toi');
});

test('lance avec un AUTRE heros a mon siege : meme affirmation', async ({ page }) => {
  // L'hote a change le heros de ce siege dans son assistant. L'invite doit
  // pouvoir le voir, et le salon lui offrira de rejoindre avec ce heros-la.
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('sans-toi');
});

// ⚠ ET JAMAIS AVANT D'AVOIR CHOISI. Tant que l'invite n'a rien choisi, il a du
// travail devant lui : lui annoncer qu'une partie tourne sans lui le
// detournerait de la grille des heros, et serait faux une fois sur deux.
test('rien de choisi : on n affirme rien, meme longtemps apres', async ({ page }) => {
  expect(await decision(page, {
    enJeu: true, heros: SPIDER_MAN, debut: MANCHE_2,
    attenteDepuis: 1_000_000, maintenant: 1_600_000,
  })).toBe('attendre');
});

/* ================= 6. La campagne ================= */

// ⚠ EN CAMPAGNE LE HEROS NE PEUT PAS SERVIR DE SIGNAL, et c'est structurel :
// l'equipe est fixee par le livret et ne change PAS d'une manche a l'autre. Le
// siege N tient donc toujours le meme heros. Comparer les heros ne laisserait
// pas le defaut ouvert, il le GARANTIRAIT — bascule immediate a chaque
// chargement du salon, sur la partie precedente.
//
// La fraicheur, elle, suffit seule : l'invite n'a rien choisi, la seule
// question est « une partie a-t-elle demarre depuis que je suis arrive ? ».
test('campagne : la manche precedente encore chargee n emmene nulle part', async ({ page }) => {
  expect(await decision(page, {
    sansChoix: true, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

test('campagne : la manche suivante fait basculer, meme equipe', async ({ page }) => {
  expect(await decision(page, {
    sansChoix: true, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_2, debutAuChoix: MANCHE_1,
  })).toBe('basculer');
});

test('campagne : aucune partie, on attend', async ({ page }) => {
  expect(await decision(page, {
    sansChoix: true, enJeu: false, debutAuChoix: MANCHE_1,
  })).toBe('attendre');
});

/* ================= 7. Le residu : aucun repere ================= */

// ⚠ LE SEUL CAS QU'AUCUN SIGNAL NE TRANCHE. Un invite dont le navigateur n'a
// aucun repere (donnees effacees, autre appareil) et qui arrive APRES le
// lancement : la partie qui tourne est peut-etre la sienne, peut-etre celle
// d'avant. On ne l'envoie nulle part de force et on ne le laisse pas non plus
// devant un ecran muet : passe un delai franc, on PROPOSE et c'est lui qui
// tranche.
test('aucun repere : rien n est propose avant le delai', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK, debut: MANCHE_1,
    debutAuChoix: null, attenteDepuis: debut, maintenant: debut + 20_000,
  })).toBe('attendre');
});

test('aucun repere : passe le delai, on propose', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK, debut: MANCHE_1,
    debutAuChoix: null, attenteDepuis: debut, maintenant: debut + 60_000,
  })).toBe('proposer');
});

// ⚠⚠ ET LE TEMPS NE DOIT RIEN Y CHANGER (ronde 2 du 21/09/2026). La premiere
// version gardait ici une « clause de reserve » : passe 45 s, elle PROPOSAIT de
// rejoindre, au motif qu'on avait peut-etre perdu son repere. Elle rouvrait le
// cas 7 sous forme de bouton — « Rejoindre cette partie » vers la manche
// PRECEDENTE, a chaque soiree ou l'hote met plus de 45 s a lancer.
//
// Le raisonnement etait faux : si le repere avait ete perdu, `debutAuChoix`
// serait `null`. `debut === debutAuChoix` est au contraire la preuve POSITIVE
// que la partie qui tourne precede mon choix.
//
// ⚠ AUCUN CAS PLUS HAUT NE FAIT PASSER LE TEMPS, et c'est ainsi que le defaut
// avait pu passer : `attenteDepuis: null` n'est la valeur d'aucune session
// reelle.
test('cas 7, une minute plus tard : toujours rien a proposer', async ({ page }) => {
  const t0 = 1_000_000;
  for (const ecart of [44_000, 60_000, 600_000]) {
    expect(await decision(page, {
      monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK,
      debut: MANCHE_1, debutAuChoix: MANCHE_1,
      attenteDepuis: t0, maintenant: t0 + ecart,
    })).toBe('attendre');
  }
});

// ⚠ MEME CHOSE EN CAMPAGNE, et c'etait pire : `sansChoix` satisfaisait seul la
// clause, sans aucun controle de heros. TOUT invite de campagne arrive pendant
// que la manche precedente est chargee se voyait offrir « Rejoindre cette
// partie » vers la manche d'hier, des que l'hote tardait de 45 s.
test('campagne, une minute plus tard : toujours rien a proposer', async ({ page }) => {
  const t0 = 1_000_000;
  for (const ecart of [44_000, 60_000, 600_000]) {
    expect(await decision(page, {
      sansChoix: true, enJeu: true, heros: SPIDER_MAN,
      debut: MANCHE_1, debutAuChoix: MANCHE_1,
      attenteDepuis: t0, maintenant: t0 + ecart,
    })).toBe('attendre');
  }
});

// ... mais si le siege tient QUELQU'UN D'AUTRE, il n'y a aucune ambiguite :
// cette partie n'est pas la mienne, on n'a rien a proposer.
test('repere inchange et autre heros : on attend, sans rien proposer', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN,
    debut: MANCHE_1, debutAuChoix: MANCHE_1,
    attenteDepuis: debut, maintenant: debut + 600_000,
  })).toBe('attendre');
});

/* ================= 8. La memoire du repere ================= */
//
// ⚠ POURQUOI ELLE EXISTE. `/new` VIDE `choix_sieges` cote serveur, pour que la
// partie suivante ne reparte pas avec les choix de la precedente. Un invite qui
// recharge sa page APRES le lancement ne peut donc plus rien apprendre du
// serveur : ni son heros, ni ce qui tournait quand il a choisi.

/** Ecrit puis relit un repere dans un faux stockage, avec un ecart de temps. */
async function allerRetour(page: Page, params: {
  siege: number; choix: string; debut: string; ecartMs: number;
}) {
  return page.evaluate(async (p) => {
    const mod: any = await import('/js/salon/bascule.js');
    const boite: Record<string, string> = {};
    const stockage = {
      getItem: (k: string) => (k in boite ? boite[k] : null),
      setItem: (k: string, v: string) => { boite[k] = v; },
      removeItem: (k: string) => { delete boite[k]; },
    };
    const pose = 1_000_000;
    mod.memoriserRepere(stockage, p.siege, p.choix, p.debut, pose);
    return mod.relireRepere(stockage, p.siege, pose + p.ecartMs);
  }, params);
}

test('rechargement pendant l attente : le choix ET le repere sont retrouves', async ({ page }) => {
  expect(await allerRetour(page, {
    siege: 2, choix: SHE_HULK, debut: MANCHE_1, ecartMs: 90_000,
  })).toEqual({ heros: SHE_HULK, debut: MANCHE_1 });
});

// En campagne il n'y a pas de heros a retenir : seul le repere compte, et il
// doit se relire tel quel.
test('campagne : un repere sans heros se relit quand meme', async ({ page }) => {
  expect(await allerRetour(page, {
    siege: 1, choix: '', debut: MANCHE_1, ecartMs: 5_000,
  })).toEqual({ heros: '', debut: MANCHE_1 });
});

// Un siege ne lit jamais le repere d'un autre : deux invites sur le meme poste
// (un parent et son enfant, deux onglets) ne doivent pas se marcher dessus.
test('chaque siege a sa propre memoire', async ({ page }) => {
  const autre = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    const boite: Record<string, string> = {};
    const stockage = {
      getItem: (k: string) => (k in boite ? boite[k] : null),
      setItem: (k: string, v: string) => { boite[k] = v; },
      removeItem: (k: string) => { delete boite[k]; },
    };
    mod.memoriserRepere(stockage, 1, '01001a', 'aa:1', 1_000_000);
    return mod.relireRepere(stockage, 2, 1_000_000);
  });
  expect(autre).toBe(null);
});

// ⚠ LE GARDE-FOU CONTRE LA SOIREE D'HIER. Un repere oublie dans un navigateur
// ferait prendre la partie de la veille pour une partie neuve. Un repere perime
// ne vaut plus rien : on retombe sur « aucun repere », qui ne bascule jamais.
test('un repere trop vieux ne vaut plus rien', async ({ page }) => {
  const duree = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    return mod.DUREE_MEMOIRE as number;
  });
  expect(duree).toBeGreaterThan(60 * 60 * 1000); // une attente d'une heure reste couverte
  expect(await allerRetour(page, {
    siege: 0, choix: SHE_HULK, debut: MANCHE_1, ecartMs: duree - 1000,
  })).toEqual({ heros: SHE_HULK, debut: MANCHE_1 });
  expect(await allerRetour(page, {
    siege: 0, choix: SHE_HULK, debut: MANCHE_1, ecartMs: duree + 1000,
  })).toBe(null);
});

// Un stockage indisponible (navigation privee stricte, stockage desactive) ne
// doit pas casser le salon : on perd la memoire, pas la page.
test('stockage en panne : on perd la memoire, pas le salon', async ({ page }) => {
  const resultat = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    const casse = {
      getItem: () => { throw new Error('refuse'); },
      setItem: () => { throw new Error('refuse'); },
      removeItem: () => { throw new Error('refuse'); },
    };
    mod.memoriserRepere(casse, 1, '01001a', 'aa:1', 1_000_000);
    return mod.relireRepere(casse, 1, 1_000_000);
  });
  expect(resultat).toBe(null);
});

// Le repere a servi : on l'efface en partant, pour qu'il ne traine pas jusqu'a
// la prochaine soiree.
test('oublierRepere efface bien la ligne du siege', async ({ page }) => {
  const restant = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    const boite: Record<string, string> = {};
    const stockage = {
      getItem: (k: string) => (k in boite ? boite[k] : null),
      setItem: (k: string, v: string) => { boite[k] = v; },
      removeItem: (k: string) => { delete boite[k]; },
    };
    mod.memoriserRepere(stockage, 3, '01001a', 'aa:1', 1_000_000);
    mod.oublierRepere(stockage, 3);
    return mod.relireRepere(stockage, 3, 1_000_000);
  });
  expect(restant).toBe(null);
});
