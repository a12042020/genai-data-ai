enum RiskCategory {
  Financial @description("Risques liés aux aspects financiers du contrat")
  IntellectualProperty @description("Risques concernant la propriété intellectuelle")
  Liability @description("Risques de responsabilité et limitation de responsabilité")
  Confidentiality @description("Risques liés à la confidentialité et protection des données")
  Regulatory @description("Risques de conformité réglementaire")
  Performance @description("Risques liés à la performance et niveaux de service")
  Termination @description("Risques de résiliation et fin de contrat")
  Sanctions @description("Risques liés aux sanctions internationales et PEPs")
  ForceMajeure @description("Risques de force majeure")
  Subcontracting @description("Risques liés à la sous-traitance et cession")
}

enum Severity {
  Low @description("Impact limité, facilement gérable")
  Medium @description("Impact modéré, nécessite une attention")
  High @description("Impact significatif, nécessite une action immédiate")
  Critical @description("Impact sévère, pourrait mettre en péril le contrat")
}

enum ComplianceType {
  GDPR @description("Règlement général sur la protection des données")
  AntiCorruption @description("Lois anti-corruption")
  InternationalSanctions @description("Sanctions internationales")
  IndustrySpecific @description("Réglementations spécifiques à l'industrie")
  DataProtection @description("Protection des données personnelles")
}

class ContractRisk {
  id string @description("Identifiant unique du risque")
  category RiskCategory @description("Catégorie du risque")
  severity Severity @description("Niveau de sévérité du risque")
  description string @description("Description détaillée du risque")
  contractReference string @description("Référence au contrat concerné")
  clauseReference string? @description("Référence à la clause spécifique du contrat")
  mitigation string? @description("Mesures d'atténuation proposées")
  owner string? @description("Responsable de la gestion du risque")
}

class FinancialRisk {
  paymentTerms string @description("Conditions de paiement")
  penaltyClauses string @description("Clauses de pénalité")
  priceEscalation string? @description("Mécanismes d'escalade des prix")
  currencyRisk string? @description("Risques liés aux fluctuations de change")
  latePaymentPenalties string? @description("Pénalités pour retard de paiement")
  paymentSchedule string? @description("Calendrier des paiements")
}

class IntellectualPropertyRisk {
  ownership string @description("Propriété de la propriété intellectuelle")
  licenseTerms string @description("Conditions de licence")
  infringementLiability string @description("Responsabilité en cas de contrefaçon")
  thirdPartyIP string @description("Utilisation de propriété intellectuelle tiers")
  modificationsAllowed string @description("Autorisations de modification")
  sourceCodeAccess string? @description("Accès au code source")
}

class LiabilityRisk {
  limitationClauses string @description("Clauses de limitation de responsabilité")
  indemnification string @description("Indemnisation")
  warrantyPeriod string @description("Période de garantie")
  exclusions string @description("Exclusions de responsabilité")
  insuranceRequirements string @description("Exigences d'assurance")
  capLimit string @description("Plafond de responsabilité")
}

class ConfidentialityRisk {
  confidentialInformation string @description("Définition des informations confidentielles")
  dataProcessing string @description("Traitement des données")
  dataBreachNotification string @description("Notification de violation de données")
  dataRetention string @description("Période de rétention des données")
  securityMeasures string @description("Mesures de sécurité")
  thirdPartyAccess string @description("Accès par des tiers")
}

class RegulatoryRisk {
  applicableLaws string @description("Lois applicables")
  complianceRequirements string @description("Exigences de conformité")
  auditRights string @description("Droits d'audit")
  reportingObligations string @description("Obligations de déclaration")
  complianceType ComplianceType @description("Type de conformité requis")
  penalties string @description("Pénalités en cas de non-conformité")
}

class PerformanceRisk {
  serviceLevels string @description("Niveaux de service")
  performanceMetrics string @description("Métriques de performance")
  monitoring string @description("Mécanismes de surveillance")
  acceptanceCriteria string @description("Critères d'acceptation")
  serviceCredits string @description("Crédits de service")
  maintenanceObligations string @description("Obligations de maintenance")
}

class TerminationRisk {
  terminationConditions string @description("Conditions de résiliation")
  noticePeriod string @description("Préavis de résiliation")
  terminationForConvenience string @description("Résiliation pour convenance")
  terminationForCause string @description("Résiliation pour cause")
  postTerminationObligations string @description("Obligations post-résiliation")
  exitPlan string @description("Plan de sortie")
}

class SanctionsRisk {
  sanctionedPersons string @description("Personnes sanctionnées")
  sanctionedTerritories string @description("Territoires sous sanctions")
  complianceObligations string @description("Obligations de conformité")
  verificationRequirements string @description("Exigences de vérification")
  reportingObligations string @description("Obligations de déclaration")
  penalties string @description("Pénalités en cas de violation")
}

class ForceMajeureRisk {
  definition string @description("Définition de force majeure")
  notificationRequirements string @description("Exigences de notification")
  impactOnObligations string @description("Impact sur les obligations")
  suspensionPeriod string @description("Période de suspension")
  terminationRights string @description("Droits de résiliation")
}

class SubcontractingRisk {
  subcontractorApproval string @description("Approbation des sous-traitants")
  liabilityForSubcontractors string @description("Responsabilité pour les sous-traitants")
  changeOfSubcontractor string @description("Changement de sous-traitant")
  assignmentRestrictions string @description("Restrictions de cession")
  flowDownClauses string @description("Clauses de répercussion")
}

 class ExtractedContractInformation { 
    id string @description("Identifiant unique de l'analyse") 
    documentTitle string @description("Titre du document analysé") 
    documentType string @description("Type de document (contrat, CGU, etc.)") 
    documentDate string @description("Date du document") 
    parties string @description("Parties impliquées dans le document") 
    summary string @description("Résumé synthétique du document") 
    keyTerms string @description("Termes clés du document") 
    risks ContractRisk [] @description("Liste des risques identifiés dans le document") 
    financialRisk FinancialRisk? @description("Détails des risques financiers identifiés") 
    intellectualPropertyRisk IntellectualPropertyRisk? @description("Détails des risques de propriété intellectuelle") 
    liabilityRisk LiabilityRisk? @description("Détails des risques de responsabilité") 
    confidentialityRisk ConfidentialityRisk? @description("Détails des risques de confidentialité") 
    regulatoryRisk RegulatoryRisk? @description("Détails des risques réglementaires") 
    performanceRisk PerformanceRisk? @description("Détails des risques de performance") 
    terminationRisk TerminationRisk? @description("Détails des risques de résiliation") 
    sanctionsRisk SanctionsRisk? @description("Détails des risques de sanctions") 
    forceMajeureRisk ForceMajeureRisk? @description("Détails des risques de force majeure") 
    subcontractingRisk SubcontractingRisk? @description("Détails des risques de sous-traitance") 
 }


function ExtractLegalContract (document: string) -> ExtractedContractInformation {
  client "GptOss120" 
  prompt #"
    Analyse the following contract and extract information related to legal risks.
    Document:
    {{ document }}

    Follow that format:
    {{ ctx.output_format }}
    JSON:
  "#
}

function CreateFakeRiskAnalysys(instruction: string) -> ExtractedContractInformation {
  client "GptOss120" 
  prompt #"
    Generage a fake Risk Analysis for a contrat, with these instructiond:
    {{ instruction }}

    Follow that format:
    {{ ctx.output_format }}
    JSON:
  "#
}

test fake {
  functions [CreateFakeRiskAnalysys]
  args {
    instruction "Fourniture de prestation de conseil"
  }
}

test test_analyse {
  functions [ExtractLegalContract]
  args { 
    document #"
Service Agreement
Parties: TechPro Solutions (Provider) and GlobalCorp Inc (Client)

Effective Date: January 1, 2024

Term: 24 months

Services: Cloud infrastructure management and 24/7 technical support

Payment: $50,000 annually, payable in quarterly installments. Late payments incur 1.5% monthly interest.

Intellectual Property: All deliverables remain property of TechPro. Client granted non-exclusive license for internal use.

Liability: Provider's liability capped at 25% of annual contract value. No liability for consequential damages.

Confidentiality: Both parties agree to protect confidential information for 5 years post-termination.

Termination: Either party may terminate with 60 days written notice. Immediate termination for material breach.

Force Majeure: Neither party liable for delays due to events beyond reasonable control.

Governing Law: California law applies to this agreement.


    "#
  }
}