-- models/marts/fct_credit_features.sql

{{ config(materialized='table') }}

SELECT 
    age,
    income,
    home_ownership,
    loan_amount,
    loan_intent,
    interest_rate,
    default_status,
    
    -- Création de features (caractéristiques) utiles pour le Machine Learning :
    -- 1. Ratio du montant du prêt par rapport au revenu annuel
    CASE 
        WHEN income > 0 THEN loan_amount / income 
        ELSE 0 
    END AS loan_to_income_ratio,
    
    -- 2. Tranche d'âge (pour aider certains modèles ou analyses)
    CASE 
        WHEN age < 25 THEN 'Young'
        WHEN age BETWEEN 25 AND 40 THEN 'Adult'
        ELSE 'Senior'
    END AS age_category

FROM {{ ref('stg_credit_applications') }}