INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpay'
WHERE pm.code = 'clickpay'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpaycard'
WHERE pm.code = 'clickpaycard'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpaymada'
WHERE pm.code = 'clickpaymada'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpayamex'
WHERE pm.code = 'clickpayamex'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpayapplepay'
WHERE pm.code = 'clickpayapplepay'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
INSERT INTO payment_method_payment_provider_rel (payment_method_id, payment_provider_id)
SELECT pm.id, pp.id
FROM payment_method pm
JOIN payment_provider pp ON pp.code = 'clickpayapplepayhosted'
WHERE pm.code = 'clickpayapplepayhosted'
AND NOT EXISTS (
    SELECT 1
    FROM payment_method_payment_provider_rel pmpr
    WHERE pmpr.payment_method_id = pm.id
    AND pmpr.payment_provider_id = pp.id
);;
