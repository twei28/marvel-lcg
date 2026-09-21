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
// La regle juste ne regarde plus « une partie tourne » mais « le heros de MON
// siege, dans la partie en cours, est-il celui que je viens de choisir ? ».
//
// Meme moule que sondage-salon.spec.ts : des fonctions PURES, appelees dans la
// page sur le vrai module, sans moteur derriere.
//   npm run bascule-salon
import { test, expect, type Page } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/prepare.html');
});

type Etat = {
  monChoix: string;
  enJeu: boolean;
  heros: string;
  desaccordDepuis?: number | null;
  maintenant?: number;
};

/** Appelle la fonction PURE du vrai module, dans la page. */
async function decision(page: Page, etat: Etat) {
  return page.evaluate(async (e) => {
    const mod: any = await import('/js/salon/bascule.js');
    return mod.decisionSalon({ desaccordDepuis: null, maintenant: 0, ...e });
  }, etat);
}

// Deux identifiants de carte heros, comme le salon les manipule : c'est
// `heroCardId` qu'il envoie a `/set_choix_siege`, et c'est lui que la partie en
// cours rend pour le siege.
const SPIDER_MAN = '01001a';
const SHE_HULK = '05001a';

// ⚠ LE CAS DU 20/09, CELUI QUI A BLOQUE LA SOIREE. Une partie de la manche
// precedente est encore chargee (l'hote a clique « Retour au menu » sur l'ecran
// de fin, ce qui ne ferme rien) et l'invite vient d'arriver : il n'a RIEN
// choisi. L'ancienne regle basculait ici.
test('ancienne partie chargee, rien de choisi : on ne bascule pas', async ({ page }) => {
  expect(await decision(page, { monChoix: '', enJeu: true, heros: SPIDER_MAN })).toBe('attendre');
});

// Meme table, mais l'invite a choisi : son heros n'est pas celui que son siege
// tient dans la partie encore chargee, donc cette partie n'est pas la sienne.
test('ancienne partie chargee, choix fait : on ne bascule toujours pas', async ({ page }) => {
  expect(await decision(page, { monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN })).toBe('attendre');
});

test('l hote lance : le siege tient MON heros, on bascule', async ({ page }) => {
  expect(await decision(page, { monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK })).toBe('basculer');
});

// L'attente ordinaire : la table est eteinte, ou aucune partie n'y tourne.
test('aucune partie en cours : on attend', async ({ page }) => {
  expect(await decision(page, { monChoix: SHE_HULK, enJeu: false, heros: '' })).toBe('attendre');
});

// ⚠ LE CAS QUI A FAIT ECARTER LE COMPTEUR DE GENERATION. Un invite qui recharge
// sa page perdrait un repere releve « en arrivant ». Ici il n'y a pas de
// repere : la question ne depend que de SON choix et du siege, donc elle
// survit au rechargement — a condition que le salon se souvienne de son choix,
// ce que prouvent les cas de memoire plus bas.
test('rechargement APRES le lancement : on bascule quand meme', async ({ page }) => {
  // Le serveur a vide les choix de siege au lancement : le choix relu vient de
  // la memoire du navigateur.
  expect(await decision(page, { monChoix: SPIDER_MAN, enJeu: true, heros: SPIDER_MAN })).toBe('basculer');
});

// ⚠ DEUX PARTIES D'AFFILEE SUR LE MEME SCENARIO. `get_play_scene_name` rend le
// meme texte dans les deux, et un nom de scene ne distinguerait donc rien.
// Le heros du siege, lui, distingue.
test('deux parties du meme scenario : le heros tranche, pas le scenario', async ({ page }) => {
  // Manche 1, encore chargee : le siege tenait Spider-Man.
  expect(await decision(page, { monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN })).toBe('attendre');
  // Manche 2, lancee : le meme siege tient maintenant She-Hulk.
  expect(await decision(page, { monChoix: SHE_HULK, enJeu: true, heros: SHE_HULK })).toBe('basculer');
});

// ⚠ LE CAS QUI N'ETAIT PAS DANS LA LISTE. L'hote a envoye trois liens et lance
// a deux : ce siege n'a PAS de heros dans la partie qui commence. Sans ce cas,
// l'invite attendrait indefiniment devant un ecran qui ne dit rien.
//
// On ne peut pas l'affirmer tout de suite : « mon siege ne tient pas mon
// heros » est EXACTEMENT ce que dit aussi une ancienne partie encore chargee.
// On laisse donc passer un delai franc avant d'expliquer.
test('lance sans ce siege : rien n est affirme avant le delai', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: '', desaccordDepuis: debut, maintenant: debut + 20_000,
  })).toBe('attendre');
});

test('lance sans ce siege : passe le delai, on explique', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: '', desaccordDepuis: debut, maintenant: debut + 60_000,
  })).toBe('expliquer');
  // Meme explication quand le siege tient QUELQU'UN D'AUTRE : l'hote a pu
  // changer le heros de ce siege dans son assistant.
  expect(await decision(page, {
    monChoix: SHE_HULK, enJeu: true, heros: SPIDER_MAN, desaccordDepuis: debut, maintenant: debut + 60_000,
  })).toBe('expliquer');
});

// ⚠ ET JAMAIS AVANT D'AVOIR CHOISI. Tant que l'invite n'a rien choisi, il a du
// travail devant lui : lui annoncer qu'une partie tourne sans lui serait un
// mensonge une fois sur deux (c'est peut-etre l'ancienne) et le detournerait
// de la grille des heros.
test('rien de choisi : on n explique rien, meme longtemps apres', async ({ page }) => {
  const debut = 1_000_000;
  expect(await decision(page, {
    monChoix: '', enJeu: true, heros: SPIDER_MAN, desaccordDepuis: debut, maintenant: debut + 600_000,
  })).toBe('attendre');
});

/* ---------------- La memoire du choix ---------------- */
//
// ⚠ POURQUOI ELLE EXISTE. `/new` VIDE `choix_sieges` cote serveur, pour que la
// partie suivante ne reparte pas avec les choix de la precedente. Un invite qui
// recharge sa page APRES le lancement ne peut donc plus apprendre du serveur ce
// qu'il avait choisi : sans memoire locale, il ne saurait pas se reconnaitre et
// resterait sur le salon pendant que sa partie tourne.

/** Ecrit puis relit un choix dans un faux stockage, avec un ecart de temps. */
async function allerRetour(page: Page, params: { siege: number; choix: string; ecartMs: number }) {
  return page.evaluate(async (p) => {
    const mod: any = await import('/js/salon/bascule.js');
    const boite: Record<string, string> = {};
    const stockage = {
      getItem: (k: string) => (k in boite ? boite[k] : null),
      setItem: (k: string, v: string) => { boite[k] = v; },
      removeItem: (k: string) => { delete boite[k]; },
    };
    const pose = 1_000_000;
    mod.memoriserChoix(stockage, p.siege, p.choix, pose);
    return mod.relireChoix(stockage, p.siege, pose + p.ecartMs);
  }, params);
}

test('rechargement pendant l attente : le choix est retrouve', async ({ page }) => {
  expect(await allerRetour(page, { siege: 2, choix: SHE_HULK, ecartMs: 90_000 })).toBe(SHE_HULK);
});

// Un siege ne lit jamais le choix d'un autre : deux invites sur le meme poste
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
    mod.memoriserChoix(stockage, 1, '01001a', 1_000_000);
    return mod.relireChoix(stockage, 2, 1_000_000);
  });
  expect(autre).toBe('');
});

// ⚠ LE GARDE-FOU CONTRE LA SOIREE D'HIER. Un choix oublie dans un navigateur,
// plus la partie d'hier encore chargee sur la table, ramenerait exactement le
// defaut du 20/09 — en plus etroit, mais le meme. Un choix perime ne vaut plus
// rien.
test('un choix trop vieux ne vaut plus rien', async ({ page }) => {
  const duree = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    return mod.DUREE_MEMOIRE as number;
  });
  expect(duree).toBeGreaterThan(60 * 60 * 1000); // une attente d'une heure reste couverte
  expect(await allerRetour(page, { siege: 0, choix: SHE_HULK, ecartMs: duree - 1000 })).toBe(SHE_HULK);
  expect(await allerRetour(page, { siege: 0, choix: SHE_HULK, ecartMs: duree + 1000 })).toBe('');
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
    mod.memoriserChoix(casse, 1, '01001a', 1_000_000);
    return mod.relireChoix(casse, 1, 1_000_000);
  });
  expect(resultat).toBe('');
});

// Le choix a servi : on l'efface en partant, pour qu'il ne traine pas jusqu'a
// la prochaine soiree.
test('oublierChoix efface bien la ligne du siege', async ({ page }) => {
  const restant = await page.evaluate(async () => {
    const mod: any = await import('/js/salon/bascule.js');
    const boite: Record<string, string> = {};
    const stockage = {
      getItem: (k: string) => (k in boite ? boite[k] : null),
      setItem: (k: string, v: string) => { boite[k] = v; },
      removeItem: (k: string) => { delete boite[k]; },
    };
    mod.memoriserChoix(stockage, 3, '01001a', 1_000_000);
    mod.oublierChoix(stockage, 3);
    return mod.relireChoix(stockage, 3, 1_000_000);
  });
  expect(restant).toBe('');
});
