SELECT 
    CAST(person_age AS INTEGER) AS age,
    CAST(person_income AS DOUBLE) AS income,
    CAST(person_home_ownership AS VARCHAR) AS home_ownership,
    CAST(loan_amnt AS DOUBLE) AS loan_amount,
    CAST(loan_intent AS VARCHAR) AS loan_intent,
    CAST(loan_int_rate AS DOUBLE) AS interest_rate,
    CAST(loan_status AS INTEGER) AS default_status
FROM {{ source('raw_credit_data', 'credit_applications') }}
WHERE person_age BETWEEN 18 AND 100
  AND person_income > 0