-- v0.5.1 Phase 1 / Migration 25.
-- Product routing worker audit event registration.
--
-- PostgreSQL is authoritative.
-- No catalog generation.
-- No provider integration.

INSERT INTO commerce_audit_event_type_vocabulary (value, description, sort_order)
VALUES
    ('product_route_recommended', 'Product routing worker recommended one product family.', 120)
ON CONFLICT (value) DO UPDATE SET
    description = EXCLUDED.description,
    sort_order = EXCLUDED.sort_order;
