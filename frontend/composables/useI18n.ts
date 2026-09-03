// Lightweight UI-language toggle (English/French) for the console chrome --
// separate from a patient's own `language` field (which selects which language
// the READING PASSAGE is shown in, on the assessment page). This toggle only
// affects the interface text a clinician reads, not clinical content.
//
// Deliberately a plain dictionary rather than a full i18n library: the console
// has a small, stable set of chrome strings, and a dependency-free approach
// keeps this easy to extend to more languages later (Cameroon's own digital
// health strategy prioritizes English + French first, per the project brief).
export type Locale = 'en' | 'fr'

const dict: Record<Locale, Record<string, string>> = {
  en: {
    'nav.dashboard': 'Dashboard',
    'nav.newPatient': 'New patient',
    'nav.signOut': 'Sign out',
    'footer.disclaimer': 'Screening aid only, not a diagnosis. Always refer to a qualified clinician.',

    'welcome.headline': 'A neurologist may be far away. A smartphone isn\u2019t.',
    'welcome.subhead': 'Neuromoyo turns a short voice recording into a structured screening signal for Parkinsonian speech patterns.',
    'welcome.tagline': 'Screening and monitoring, not a diagnosis.',
    'welcome.cta': 'Get started',
    'welcome.footnote': 'Accounts are created by a facility admin. Already have one? Sign in on the next screen.',
    'welcome.eyebrow': 'AI-assisted neurological screening',
    'welcome.secondaryCta': 'See the science behind it',

    'welcome.how.eyebrow': 'How it works',
    'welcome.how.heading': 'Three short recordings, one structured signal',
    'welcome.how.step1.title': 'Read a passage',
    'welcome.how.step1.desc': 'About 30 seconds of natural speech, analyzed for pitch, rhythm, and clarity.',
    'welcome.how.step2.title': 'Hold a vowel',
    'welcome.how.step2.desc': 'A sustained "aaah" reveals voice steadiness that\u2019s hard to notice by ear alone.',
    'welcome.how.step3.title': 'Repeat "pa-ta-ka"',
    'welcome.how.step3.desc': 'Rapid syllable repetition measures motor-speech speed and rhythm.',

    'welcome.science.eyebrow': 'The science',
    'welcome.science.heading': 'Why a voice recording can reveal Parkinson\u2019s early',
    'welcome.science.p1': 'Parkinson\u2019s disease is already the world\u2019s fastest-growing neurological disorder. A 2025 global modelling study published in The BMJ projects 25.2 million people will be living with it by 2050, more than double the 2021 total, with the sharpest regional rise anywhere, 292%, expected in western Sub-Saharan Africa.',
    'welcome.science.p2': 'Parkinson\u2019s affects the brain circuits that control movement, including the fine muscle coordination behind speech. Around 9 in 10 people with Parkinson\u2019s develop measurable speech changes, reduced loudness, a narrower pitch range, imprecise articulation, and research shows these changes often appear before the hand tremor or stiffness most people associate with the disease. Voice is one of the earliest windows into the condition, not just a symptom of it.',
    'welcome.science.illustrationCaption': 'A tremor is easy to see. The speech changes that came before it are easier to measure than to hear.',
    'welcome.science.p3': 'Published acoustic-biomarker studies over the past two years have reported strong accuracy, commonly in the 80\u201395%+ range on curated research datasets, at distinguishing Parkinsonian speech from healthy speech using measurements like jitter, shimmer, and pitch variability, the same category of features NeuroVoice extracts from every recording.',
    'welcome.science.p4': 'Voice-based screening has particular value where specialist neurological care is scarce and brain imaging is expensive, exactly the primary-care setting most of Africa\u2019s health system runs on. NeuroVoice\u2019s own model is validated conservatively, across recordings from different sources rather than one lab\u2019s clean dataset, because a tool meant for real clinics needs to be tested like one. It\u2019s built to flag who needs a closer look, not to diagnose, every result says so, every time.',
    'welcome.science.sources': 'Sources: Global Burden of Disease Study 2021 modelling, published in The BMJ (2025); peer-reviewed acoustic-biomarker research, 2024\u20132025.',

    'welcome.africa.eyebrow': 'Built for where care is thin on the ground',
    'welcome.africa.heading': 'Designed around real constraints, not ideal ones',
    'welcome.africa.item1.title': 'Just a smartphone',
    'welcome.africa.item1.desc': 'No wearables, no lab equipment, the same phone a health worker already carries.',
    'welcome.africa.item2.title': 'Works where specialists don\u2019t reach',
    'welcome.africa.item2.desc': 'A structured screening result travels with the patient to whichever clinician sees them next.',
    'welcome.africa.item3.title': 'Honest about its limits',
    'welcome.africa.item3.desc': 'Every screen says clearly: further evaluation recommended, never a diagnosis.',

    'welcome.finalCta.heading': 'Start where the patient already is',

    'dashboard.title': 'Patients',
    'dashboard.subtitle': 'Screening and monitoring across your facility.',
    'dashboard.search': 'Search by patient ID',
    'dashboard.addPatient': 'New patient',
    'dashboard.filter.all': 'All',
    'dashboard.filter.flagged': 'Needs review',
    'dashboard.empty': 'No patients yet. Register one to begin screening.',
    'dashboard.empty.filtered': 'No patients match this filter.',
    'dashboard.col.patient': 'Patient',
    'dashboard.col.lastAssessed': 'Last assessed',
    'dashboard.col.latestRisk': 'Latest risk',
    'dashboard.col.trend': 'Trend',
    'dashboard.noAssessments': 'Not yet screened',
    'dashboard.stat.total': 'Patients',
    'dashboard.stat.flagged': 'Flagged for review',
    'dashboard.stat.assessments': 'Assessments this month',

    'login.title': 'Sign in',
    'login.subtitle': 'Neuromoyo clinician console. Accounts are created by an admin.',
    'login.email': 'Email',
    'login.password': 'Password',
    'login.submit': 'Sign in',
    'login.submitting': 'Signing in…',

    'intake.step': 'Step 1 of 2',
    'intake.title': 'New assessment',
    'intake.subtitle': "Enter the patient's clinic ID to begin a NeuroVoice screening.",
    'intake.patientId': 'Patient ID (clinic-assigned)',
    'intake.age': 'Age',
    'intake.sex': 'Sex',
    'intake.sex.unspecified': 'Prefer not to say',
    'intake.sex.female': 'Female',
    'intake.sex.male': 'Male',
    'intake.language': 'Language',
    'intake.facility': 'Facility',
    'intake.existingDx': "Existing Parkinson's diagnosis",
    'intake.submit': 'Start screening',
    'intake.submitting': 'Creating…',

    'assess.step': 'Step 2 of 2',
    'assess.tab.reading': 'Reading',
    'assess.tab.vowel': 'Sustained vowel',
    'assess.tab.ddk': '/pa-ta-ka/',
    'assess.tab.history': 'History',
    'assess.tab.trends': 'Trends',
    'assess.tab.details': 'Details',
    'assess.backToDashboard': 'Back to patients',

    'assess.nav.overview': 'Overview',
    'assess.nav.record': 'Record assessment',
    'assess.nav.history': 'History & trends',
    'assess.nav.details': 'Patient details',
    'assess.nav.report': 'Generate report',

    'overview.status': 'Latest status',
    'overview.notScreened': 'Not yet screened',
    'overview.lastAssessed': 'Last assessed',
    'overview.totalAssessments': 'Total assessments',
    'overview.recordCta': 'Record a new assessment',
    'overview.recordCtaDesc': 'Reading passage, sustained vowel, or /pa-ta-ka/.',
    'overview.historyCta': 'View history & trends',
    'overview.historyCtaDesc': 'Every past assessment and how measurements have moved over time.',
    'overview.reportCta': 'Generate report',
    'overview.reportCtaDesc': 'A synthesized summary across all tasks, ready to share or print.',
    'overview.detailsCta': 'Patient details',
    'overview.detailsCtaDesc': 'View or edit demographic and clinical info.',

    'report.title': 'Screening Report',
    'report.generatedOn': 'Generated',
    'report.coverage': 'Assessments covered',
    'report.download': 'Download as PDF',
    'report.recommendation': 'Recommendation',
    'report.tier.priority_referral': 'Priority, refer to neurologist',
    'report.tier.monitor': 'Continue monitoring',
    'report.tier.routine': 'Routine, no action indicated',
    'report.tier.insufficient_data': 'Insufficient data',
    'report.taskSummary': 'Task completion',
    'report.readingTrend': 'Reading risk trend',
    'report.biomarkerTrends': 'Biomarker trends across tasks',
    'report.supportingFindings': 'Supporting findings',
    'report.noFindings': 'No additional findings from the sustained-vowel or /pa-ta-ka/ tasks.',
    'report.task.reading': 'Reading passage',
    'report.task.vowel': 'Sustained vowel',
    'report.task.ddk': '/pa-ta-ka/',
    'report.notCompleted': 'Not completed',
    'report.assessmentsCount': 'assessments',

    'nav.team': 'Team',
    'team.title': 'Team & facilities',
    'team.subtitle.admin': 'Register facilities and invite their administrators.',
    'team.subtitle.facilityAdmin': 'Invite and manage clinicians at your facility.',
    'team.facilities': 'Facilities',
    'team.newFacility': 'New facility',
    'team.facilityName': 'Facility name',
    'team.createFacility': 'Register facility',
    'team.roster': 'Roster',
    'team.inviteClinician': 'Invite clinician',
    'team.inviteFacilityAdmin': 'Invite facility admin',
    'team.email': 'Email',
    'team.facility': 'Facility',
    'team.role': 'Role',
    'team.role.clinician': 'Clinician',
    'team.role.facility_admin': 'Facility admin',
    'team.invite': 'Send invite',
    'team.inviting': 'Sending…',
    'team.inviteSent': 'Invite sent, they\'ll receive an email to set a password.',
    'team.noFacilities': 'No facilities registered yet.',
    'team.noClinicians': 'No clinicians yet.',
  },
  fr: {
    'nav.dashboard': 'Tableau de bord',
    'nav.newPatient': 'Nouveau patient',
    'nav.signOut': 'Déconnexion',
    'footer.disclaimer': "Outil de dépistage uniquement, pas un diagnostic. Toujours consulter un clinicien qualifié.",

    'welcome.headline': 'Un neurologue peut être loin. Un smartphone ne l\u2019est pas.',
    'welcome.subhead': "Neuromoyo transforme un court enregistrement vocal en un signal structuré de dépistage des troubles de la parole parkinsoniens.",
    'welcome.tagline': 'Dépistage et suivi, pas un diagnostic.',
    'welcome.cta': 'Commencer',
    'welcome.footnote': "Les comptes sont créés par un administrateur d'établissement. Vous en avez déjà un ? Connectez-vous à l'écran suivant.",
    'welcome.eyebrow': 'Dépistage neurologique assisté par IA',
    'welcome.secondaryCta': 'Voir la science derrière l\u2019outil',

    'welcome.how.eyebrow': 'Comment ça marche',
    'welcome.how.heading': 'Trois courts enregistrements, un signal structuré',
    'welcome.how.step1.title': 'Lire un texte',
    'welcome.how.step1.desc': 'Environ 30 secondes de parole naturelle, analysées pour le ton, le rythme et la clarté.',
    'welcome.how.step2.title': 'Tenir une voyelle',
    'welcome.how.step2.desc': 'Un "aaah" soutenu révèle une stabilité vocale difficile à percevoir à l\u2019oreille seule.',
    'welcome.how.step3.title': 'Répéter "pa-ta-ka"',
    'welcome.how.step3.desc': 'La répétition rapide de syllabes mesure la vitesse et le rythme moteur de la parole.',

    'welcome.science.eyebrow': 'La science',
    'welcome.science.heading': 'Pourquoi un enregistrement vocal peut révéler Parkinson tôt',
    'welcome.science.p1': 'La maladie de Parkinson est déjà le trouble neurologique dont la croissance est la plus rapide au monde. Une étude de modélisation mondiale de 2025, publiée dans The BMJ, projette 25,2 millions de personnes vivant avec la maladie d\u2019ici 2050, plus du double du total de 2021, avec la hausse régionale la plus marquée, 292 %, attendue en Afrique subsaharienne occidentale.',
    'welcome.science.p2': 'La maladie de Parkinson affecte les circuits cérébraux qui contrôlent le mouvement, y compris la coordination musculaire fine à l\u2019origine de la parole. Environ 9 personnes atteintes sur 10 développent des changements vocaux mesurables, volume réduit, gamme de tons plus étroite, articulation imprécise, et la recherche montre que ces changements apparaissent souvent avant le tremblement de la main ou la raideur généralement associés à la maladie. La voix est l\u2019une des premières fenêtres sur la maladie, pas seulement un de ses symptômes.',
    'welcome.science.illustrationCaption': 'Un tremblement se voit facilement. Les changements vocaux qui l\u2019ont précédé se mesurent plus facilement qu\u2019ils ne s\u2019entendent.',
    'welcome.science.p3': 'Des études publiées sur les biomarqueurs acoustiques ces deux dernières années rapportent une bonne précision, souvent entre 80 et 95 %+ sur des jeux de données de recherche organisés, pour distinguer la parole parkinsonienne de la parole saine à l\u2019aide de mesures comme le jitter, le shimmer et la variabilité du ton, la même catégorie de caractéristiques que NeuroVoice extrait de chaque enregistrement.',
    'welcome.science.p4': 'Le dépistage vocal a une valeur particulière là où les soins neurologiques spécialisés sont rares et l\u2019imagerie cérébrale coûteuse, exactement le contexte de soins primaires sur lequel repose la majeure partie du système de santé africain. Le modèle de NeuroVoice est validé de façon prudente, sur des enregistrements provenant de sources différentes plutôt que le jeu de données propre d\u2019un seul laboratoire, car un outil destiné aux vraies cliniques doit être testé comme tel. Il est conçu pour signaler qui mérite un examen plus approfondi, pas pour diagnostiquer, chaque résultat le rappelle, à chaque fois.',
    'welcome.science.sources': 'Sources : modélisation de l\u2019étude Global Burden of Disease 2021, publiée dans The BMJ (2025) ; recherches évaluées par les pairs sur les biomarqueurs acoustiques, 2024\u20132025.',

    'welcome.africa.eyebrow': 'Conçu pour là où les soins se font rares',
    'welcome.africa.heading': 'Pensé pour des contraintes réelles, pas idéales',
    'welcome.africa.item1.title': 'Juste un smartphone',
    'welcome.africa.item1.desc': 'Pas de dispositif portable, pas d\u2019équipement de laboratoire, le même téléphone qu\u2019un agent de santé porte déjà.',
    'welcome.africa.item2.title': 'Fonctionne là où les spécialistes n\u2019arrivent pas',
    'welcome.africa.item2.desc': 'Un résultat de dépistage structuré accompagne le patient jusqu\u2019au prochain clinicien qui le reçoit.',
    'welcome.africa.item3.title': 'Honnête sur ses limites',
    'welcome.africa.item3.desc': 'Chaque dépistage l\u2019indique clairement : évaluation complémentaire recommandée, jamais un diagnostic.',

    'welcome.finalCta.heading': 'Commencez là où se trouve déjà le patient',

    'dashboard.title': 'Patients',
    'dashboard.subtitle': 'Dépistage et suivi au sein de votre établissement.',
    'dashboard.search': "Rechercher par ID patient",
    'dashboard.addPatient': 'Nouveau patient',
    'dashboard.filter.all': 'Tous',
    'dashboard.filter.flagged': 'À examiner',
    'dashboard.empty': "Aucun patient pour l'instant. Enregistrez-en un pour commencer.",
    'dashboard.empty.filtered': 'Aucun patient ne correspond à ce filtre.',
    'dashboard.col.patient': 'Patient',
    'dashboard.col.lastAssessed': 'Dernière évaluation',
    'dashboard.col.latestRisk': 'Risque le plus récent',
    'dashboard.col.trend': 'Tendance',
    'dashboard.noAssessments': 'Pas encore évalué',
    'dashboard.stat.total': 'Patients',
    'dashboard.stat.flagged': 'Signalés pour examen',
    'dashboard.stat.assessments': 'Évaluations ce mois-ci',

    'login.title': 'Connexion',
    'login.subtitle': 'Console clinicien Neuromoyo. Les comptes sont créés par un administrateur.',
    'login.email': 'E-mail',
    'login.password': 'Mot de passe',
    'login.submit': 'Se connecter',
    'login.submitting': 'Connexion…',

    'intake.step': 'Étape 1 sur 2',
    'intake.title': 'Nouvelle évaluation',
    'intake.subtitle': "Saisissez l'identifiant clinique du patient pour commencer un dépistage NeuroVoice.",
    'intake.patientId': 'ID patient (attribué par la clinique)',
    'intake.age': 'Âge',
    'intake.sex': 'Sexe',
    'intake.sex.unspecified': 'Préfère ne pas préciser',
    'intake.sex.female': 'Féminin',
    'intake.sex.male': 'Masculin',
    'intake.language': 'Langue',
    'intake.facility': 'Établissement',
    'intake.existingDx': 'Diagnostic de Parkinson existant',
    'intake.submit': 'Commencer le dépistage',
    'intake.submitting': 'Création…',

    'assess.step': 'Étape 2 sur 2',
    'assess.tab.reading': 'Lecture',
    'assess.tab.vowel': 'Voyelle soutenue',
    'assess.tab.ddk': '/pa-ta-ka/',
    'assess.tab.history': 'Historique',
    'assess.tab.trends': 'Tendances',
    'assess.tab.details': 'Détails',
    'assess.backToDashboard': 'Retour aux patients',

    'assess.nav.overview': 'Aperçu',
    'assess.nav.record': 'Enregistrer une évaluation',
    'assess.nav.history': 'Historique et tendances',
    'assess.nav.details': 'Détails du patient',
    'assess.nav.report': 'Générer un rapport',

    'overview.status': 'Dernier statut',
    'overview.notScreened': 'Pas encore évalué',
    'overview.lastAssessed': 'Dernière évaluation',
    'overview.totalAssessments': 'Total des évaluations',
    'overview.recordCta': 'Enregistrer une nouvelle évaluation',
    'overview.recordCtaDesc': 'Lecture, voyelle soutenue, ou /pa-ta-ka/.',
    'overview.historyCta': 'Voir l\u2019historique et les tendances',
    'overview.historyCtaDesc': 'Chaque évaluation passée et l\u2019évolution des mesures dans le temps.',
    'overview.reportCta': 'Générer un rapport',
    'overview.reportCtaDesc': 'Un résumé synthétisé de toutes les tâches, prêt à partager ou imprimer.',
    'overview.detailsCta': 'Détails du patient',
    'overview.detailsCtaDesc': 'Voir ou modifier les informations démographiques et cliniques.',

    'report.title': 'Rapport de dépistage',
    'report.generatedOn': 'Généré le',
    'report.coverage': 'Évaluations couvertes',
    'report.download': 'Télécharger en PDF',
    'report.recommendation': 'Recommandation',
    'report.tier.priority_referral': 'Priorité, orienter vers un neurologue',
    'report.tier.monitor': 'Poursuivre le suivi',
    'report.tier.routine': 'Routine, aucune action indiquée',
    'report.tier.insufficient_data': 'Données insuffisantes',
    'report.taskSummary': 'Achèvement des tâches',
    'report.readingTrend': 'Tendance du risque (lecture)',
    'report.biomarkerTrends': 'Tendances des biomarqueurs entre les tâches',
    'report.supportingFindings': 'Constatations à l\u2019appui',
    'report.noFindings': 'Aucune constatation supplémentaire des tâches voyelle soutenue ou /pa-ta-ka/.',
    'report.task.reading': 'Lecture',
    'report.task.vowel': 'Voyelle soutenue',
    'report.task.ddk': '/pa-ta-ka/',
    'report.notCompleted': 'Non complété',
    'report.assessmentsCount': 'évaluations',

    'nav.team': 'Équipe',
    'team.title': 'Équipe et établissements',
    'team.subtitle.admin': 'Enregistrez des établissements et invitez leurs administrateurs.',
    'team.subtitle.facilityAdmin': 'Invitez et gérez les cliniciens de votre établissement.',
    'team.facilities': 'Établissements',
    'team.newFacility': 'Nouvel établissement',
    'team.facilityName': 'Nom de l\u2019établissement',
    'team.createFacility': 'Enregistrer l\u2019établissement',
    'team.roster': 'Équipe',
    'team.inviteClinician': 'Inviter un clinicien',
    'team.inviteFacilityAdmin': 'Inviter un administrateur d\u2019établissement',
    'team.email': 'E-mail',
    'team.facility': 'Établissement',
    'team.role': 'Rôle',
    'team.role.clinician': 'Clinicien',
    'team.role.facility_admin': 'Administrateur d\u2019établissement',
    'team.invite': 'Envoyer l\u2019invitation',
    'team.inviting': 'Envoi…',
    'team.inviteSent': 'Invitation envoyée, la personne recevra un e-mail pour définir un mot de passe.',
    'team.noFacilities': 'Aucun établissement enregistré pour l\u2019instant.',
    'team.noClinicians': 'Aucun clinicien pour l\u2019instant.',
  },
}

export function useI18n() {
  const locale = useState<Locale>('i18n:locale', () => 'en')

  function t(key: string): string {
    return dict[locale.value]?.[key] ?? dict.en[key] ?? key
  }

  function setLocale(l: Locale) {
    locale.value = l
    if (import.meta.client) {
      try { window.localStorage.setItem('neuromoyo:locale', l) } catch { /* ignore */ }
    }
  }

  function toggleLocale() {
    setLocale(locale.value === 'en' ? 'fr' : 'en')
  }

  function initLocale() {
    if (import.meta.client) {
      try {
        const saved = window.localStorage.getItem('neuromoyo:locale')
        if (saved === 'en' || saved === 'fr') locale.value = saved
      } catch { /* ignore */ }
    }
  }

  return { locale, t, setLocale, toggleLocale, initLocale }
}
