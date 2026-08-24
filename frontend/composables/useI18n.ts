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
    'footer.disclaimer': 'Screening aid only — not a diagnosis. Always refer to a qualified clinician.',

    'welcome.headline': 'A neurologist may be far away. A smartphone isn\u2019t.',
    'welcome.subhead': 'Neuromoyo turns a short voice recording into a structured screening signal for Parkinsonian speech patterns.',
    'welcome.tagline': 'Screening and monitoring — not a diagnosis.',
    'welcome.cta': 'Get started',
    'welcome.footnote': 'Accounts are created by a facility admin. Already have one? Sign in on the next screen.',

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
    'report.tier.priority_referral': 'Priority — refer to neurologist',
    'report.tier.monitor': 'Continue monitoring',
    'report.tier.routine': 'Routine — no action indicated',
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
  },
  fr: {
    'nav.dashboard': 'Tableau de bord',
    'nav.newPatient': 'Nouveau patient',
    'nav.signOut': 'Déconnexion',
    'footer.disclaimer': "Outil de dépistage uniquement — pas un diagnostic. Toujours consulter un clinicien qualifié.",

    'welcome.headline': 'Un neurologue peut être loin. Un smartphone ne l\u2019est pas.',
    'welcome.subhead': "Neuromoyo transforme un court enregistrement vocal en un signal structuré de dépistage des troubles de la parole parkinsoniens.",
    'welcome.tagline': 'Dépistage et suivi — pas un diagnostic.',
    'welcome.cta': 'Commencer',
    'welcome.footnote': "Les comptes sont créés par un administrateur d'établissement. Vous en avez déjà un ? Connectez-vous à l'écran suivant.",

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
    'report.tier.priority_referral': 'Priorité — orienter vers un neurologue',
    'report.tier.monitor': 'Poursuivre le suivi',
    'report.tier.routine': 'Routine — aucune action indiquée',
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
