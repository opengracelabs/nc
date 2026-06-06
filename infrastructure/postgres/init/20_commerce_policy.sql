-- v0.5.0 Phase 1 / Migration 20.
-- Commerce Intelligence policy authority.
--
-- No scoring worker activation.
-- No product generation.
-- No Shopify integration.

CREATE TABLE IF NOT EXISTS commerce_policy (
    id                           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version                      TEXT NOT NULL UNIQUE,
    status                       TEXT NOT NULL REFERENCES commerce_policy_status_vocabulary(value),
    effective_from               TIMESTAMPTZ,
    effective_until              TIMESTAMPTZ,
    authored_by                  TEXT NOT NULL,
    approved_by                  TEXT,
    approved_at                  TIMESTAMPTZ,
    changelog                    TEXT NOT NULL,
    previous_version_id          UUID REFERENCES commerce_policy(id),
    max_score_age_days           INT NOT NULL DEFAULT 90 CHECK (max_score_age_days > 0),

    formula_spec                 JSONB NOT NULL,
    composite_weights            JSONB NOT NULL,
    tier_thresholds              JSONB NOT NULL,
    hard_gate_values             JSONB NOT NULL,
    model_activation_thresholds  JSONB NOT NULL,
    product_surface_requirements JSONB NOT NULL,

    provenance                   JSONB NOT NULL DEFAULT '{}',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_commerce_policy_approval_identity CHECK (
        approved_by IS NULL OR approved_by IS DISTINCT FROM authored_by
    ),
    CONSTRAINT chk_commerce_policy_approved_status CHECK (
        status NOT IN ('active','paused','superseded')
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)
    ),
    CONSTRAINT chk_commerce_policy_effective_window CHECK (
        effective_until IS NULL OR effective_from IS NULL OR effective_until > effective_from
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_commerce_policy_one_active
    ON commerce_policy((status))
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_commerce_policy_status
    ON commerce_policy(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_commerce_policy_previous_version
    ON commerce_policy(previous_version_id)
    WHERE previous_version_id IS NOT NULL;

DROP TRIGGER IF EXISTS trg_commerce_policy_updated_at ON commerce_policy;
CREATE TRIGGER trg_commerce_policy_updated_at
    BEFORE UPDATE ON commerce_policy
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE OR REPLACE FUNCTION enforce_commerce_policy_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.status IN ('active','paused','superseded') THEN
        IF NEW.version IS DISTINCT FROM OLD.version
           OR NEW.authored_by IS DISTINCT FROM OLD.authored_by
           OR NEW.formula_spec IS DISTINCT FROM OLD.formula_spec
           OR NEW.composite_weights IS DISTINCT FROM OLD.composite_weights
           OR NEW.tier_thresholds IS DISTINCT FROM OLD.tier_thresholds
           OR NEW.hard_gate_values IS DISTINCT FROM OLD.hard_gate_values
           OR NEW.model_activation_thresholds IS DISTINCT FROM OLD.model_activation_thresholds
           OR NEW.product_surface_requirements IS DISTINCT FROM OLD.product_surface_requirements
           OR NEW.max_score_age_days IS DISTINCT FROM OLD.max_score_age_days
        THEN
            RAISE EXCEPTION 'commerce_policy % is immutable after active, paused, or superseded status',
                OLD.id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_commerce_policy_immutability ON commerce_policy;
CREATE TRIGGER trg_commerce_policy_immutability
    BEFORE UPDATE ON commerce_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_commerce_policy_immutability();

CREATE OR REPLACE FUNCTION enforce_commerce_policy_activation()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.status = 'active' THEN
        IF NEW.approved_by IS NULL OR NEW.approved_at IS NULL THEN
            RAISE EXCEPTION 'active commerce_policy requires approved_by and approved_at';
        END IF;
        IF NEW.approved_by IS NOT DISTINCT FROM NEW.authored_by THEN
            RAISE EXCEPTION 'active commerce_policy requires second-human approval';
        END IF;
        IF NEW.effective_from IS NULL THEN
            RAISE EXCEPTION 'active commerce_policy requires effective_from';
        END IF;
        IF EXISTS (
            SELECT 1
            FROM commerce_policy p
            WHERE p.status = 'active'
              AND p.id IS DISTINCT FROM NEW.id
        ) THEN
            RAISE EXCEPTION 'only one commerce_policy may be active';
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_commerce_policy_activation ON commerce_policy;
CREATE TRIGGER trg_commerce_policy_activation
    BEFORE INSERT OR UPDATE ON commerce_policy
    FOR EACH ROW EXECUTE FUNCTION enforce_commerce_policy_activation();

INSERT INTO commerce_policy (
    version,
    status,
    authored_by,
    changelog,
    max_score_age_days,
    formula_spec,
    composite_weights,
    tier_thresholds,
    hard_gate_values,
    model_activation_thresholds,
    product_surface_requirements,
    provenance
)
VALUES (
    '1.0.0',
    'draft',
    'commerce_migration_20',
    'Initial Commerce Intelligence policy.',
    90,
    '{
      "version": "1.0.0",
      "input_hash": {
            "algorithm": "sha256",
            "encoding": "lowercase_hex",
            "canonical_json": {
                  "key_order": "alpha_sorted_keys",
                  "null_policy": "retain_json_nulls",
                  "float_serialization": "6_decimal_places"
            }
      },
      "scorer_version": "weighted_sum_v1",
      "subscores": {
            "museum_score": {
                  "inputs": [
                        {
                              "signal": "illustrator_prestige",
                              "weight": 0.35
                        },
                        {
                              "signal": "rights_confidence",
                              "weight": 0.25
                        },
                        {
                              "signal": "golden_age_factor",
                              "weight": 0.2
                        },
                        {
                              "signal": "institutional_credit",
                              "weight": 0.1
                        },
                        {
                              "signal": "provenance_completeness",
                              "weight": 0.1
                        }
                  ]
            },
            "retail_score": {
                  "inputs": [
                        {
                              "signal": "image_quality_score",
                              "weight": 0.3
                        },
                        {
                              "signal": "taxon_commercial_tier_score",
                              "weight": 0.25
                        },
                        {
                              "signal": "resolution_tier_score",
                              "weight": 0.2
                        },
                        {
                              "signal": "composition_fit",
                              "weight": 0.15
                        },
                        {
                              "signal": "color_score",
                              "weight": 0.1
                        }
                  ]
            },
            "publishing_score": {
                  "inputs": [
                        {
                              "signal": "identification_confidence",
                              "weight": 0.3
                        },
                        {
                              "signal": "image_quality_score",
                              "weight": 0.25
                        },
                        {
                              "signal": "golden_age_factor",
                              "weight": 0.2
                        },
                        {
                              "signal": "taxon_commercial_tier_score",
                              "weight": 0.15
                        },
                        {
                              "signal": "rights_confidence",
                              "weight": 0.1
                        }
                  ]
            },
            "tourism_score": {
                  "inputs": [
                        {
                              "signal": "place_relevance_score",
                              "weight": 0.35
                        },
                        {
                              "signal": "taxon_place_iconic",
                              "weight": 0.25
                        },
                        {
                              "signal": "place_tier_score",
                              "weight": 0.2
                        },
                        {
                              "signal": "image_quality_score",
                              "weight": 0.2
                        }
                  ]
            },
            "reference_score": {
                  "inputs": [
                        {
                              "signal": "identification_confidence",
                              "weight": 0.35
                        },
                        {
                              "signal": "taxon_commercial_tier_score",
                              "weight": 0.2
                        },
                        {
                              "signal": "golden_age_factor",
                              "weight": 0.2
                        },
                        {
                              "signal": "image_quality_score",
                              "weight": 0.15
                        },
                        {
                              "signal": "provenance_completeness",
                              "weight": 0.1
                        }
                  ]
            }
      },
      "composite": {
            "inputs": [
                  {
                        "signal": "retail_score",
                        "weight": 0.3
                  },
                  {
                        "signal": "tourism_score",
                        "weight": 0.25
                  },
                  {
                        "signal": "museum_score",
                        "weight": 0.2
                  },
                  {
                        "signal": "publishing_score",
                        "weight": 0.15
                  },
                  {
                        "signal": "reference_score",
                        "weight": 0.1
                  }
            ]
      },
      "signal_defaults": {
            "image_quality_score": null,
            "composition_fit": null,
            "identification_confidence": 0.0,
            "taxon_place_iconic": 0.0,
            "color_profile": "unknown",
            "color_score": 0.3
      },
      "null_signal_policy": "null_blocks_tier_12_advancement",
      "resolution_tier_map": {
            "premium": {
                  "min_width_px": 4000,
                  "score": 1.0
            },
            "standard": {
                  "min_width_px": 2000,
                  "score": 0.75
            },
            "marginal": {
                  "min_width_px": 1200,
                  "score": 0.4
            },
            "blocked": {
                  "min_width_px": 0,
                  "score": 0.0
            }
      },
      "csm_dimension_map": {
            "scorer_version": "csm_pass2_v1",
            "dimensions": {
                  "VAS": {
                        "label": "Visual Authority Score",
                        "csm_weight": 0.3,
                        "inputs": [
                              {
                                    "signal": "image_quality_score",
                                    "weight": 0.5
                              },
                              {
                                    "signal": "composition_fit",
                                    "weight": 0.3
                              },
                              {
                                    "signal": "color_score",
                                    "weight": 0.2
                              }
                        ]
                  },
                  "PIS": {
                        "label": "Place Identity Score",
                        "csm_weight": 0.2,
                        "inputs": [
                              {
                                    "signal": "place_relevance_score",
                                    "weight": 0.6
                              },
                              {
                                    "signal": "taxon_place_iconic",
                                    "weight": 0.4
                              }
                        ]
                  },
                  "SSS": {
                        "label": "Story Strength Score",
                        "csm_weight": 0.15,
                        "inputs": [
                              {
                                    "signal": "provenance_completeness",
                                    "weight": 0.4
                              },
                              {
                                    "signal": "golden_age_factor",
                                    "weight": 0.35
                              },
                              {
                                    "signal": "illustrator_prestige",
                                    "weight": 0.25
                              }
                        ]
                  },
                  "TAS": {
                        "label": "Tourism Appeal Score",
                        "csm_weight": 0.15,
                        "inputs": [
                              {
                                    "signal": "taxon_place_iconic",
                                    "weight": 0.4
                              },
                              {
                                    "signal": "place_tier_score",
                                    "weight": 0.35
                              },
                              {
                                    "signal": "place_relevance_score",
                                    "weight": 0.25
                              }
                        ]
                  },
                  "IPS": {
                        "label": "Institutional Prestige Score",
                        "csm_weight": 0.1,
                        "inputs": [
                              {
                                    "signal": "institutional_credit",
                                    "weight": 0.7
                              },
                              {
                                    "signal": "provenance_completeness",
                                    "weight": 0.3
                              }
                        ]
                  },
                  "PVS": {
                        "label": "Product Versatility Score",
                        "csm_weight": 0.1,
                        "inputs": [
                              {
                                    "signal": "resolution_tier_score",
                                    "weight": 0.7
                              },
                              {
                                    "signal": "identification_confidence",
                                    "weight": 0.3
                              }
                        ]
                  }
            },
            "composite": {
                  "inputs": [
                        {
                              "signal": "VAS",
                              "weight": 0.3
                        },
                        {
                              "signal": "PIS",
                              "weight": 0.2
                        },
                        {
                              "signal": "SSS",
                              "weight": 0.15
                        },
                        {
                              "signal": "TAS",
                              "weight": 0.15
                        },
                        {
                              "signal": "IPS",
                              "weight": 0.1
                        },
                        {
                              "signal": "PVS",
                              "weight": 0.1
                        }
                  ]
            },
            "tier_thresholds": {
                  "MASTERWORK": 0.9,
                  "FLAGSHIP": 0.75,
                  "STANDARD": 0.6,
                  "REFERENCE": 0.4,
                  "BLOCKED": 0.0
            },
            "null_signal_policy": "null_blocks_MASTERWORK_FLAGSHIP",
            "rcs_gate": {
                  "signal": "rights_confidence",
                  "min_value": 0.70,
                  "blocked_tier": "BLOCKED"
            }
      },
      "staleness_config": {
            "poll_interval_hours": 24
      }
}',
    '{
      "retail_score": 0.3,
      "tourism_score": 0.25,
      "museum_score": 0.2,
      "publishing_score": 0.15,
      "reference_score": 0.1
}',
    '{
      "tier_1": 0.8,
      "tier_2": 0.65,
      "tier_3": 0.5,
      "blocked": 0.0
}',
    '{
      "gate_0_rights_record_exists": {
            "required": true,
            "blocked_status": "blocked_rights"
      },
      "gate_1_min_rights_confidence": {
            "min_rights_confidence": 0.7,
            "blocked_status": "blocked_rights"
      },
      "gate_2_min_image_width_px": {
            "min_image_width_px": 2000,
            "blocked_status": "blocked_resolution"
      },
      "gate_3_legal_hold": {
            "rights_confidence_equals": 0.0,
            "blocked_status": "blocked_legal",
            "curator_overridable": false
      },
      "gate_4_min_quality_score": {
            "min_quality_score": 0.4,
            "null_blocks": true,
            "blocked_status": "blocked_quality"
      },
      "gate_5_curator_approval": {
            "publication_stage_only": true
      }
}',
    '{
      "museum_unlock": 0.8,
      "retail_unlock": 0.65,
      "publishing_unlock": 0.7,
      "tourism_unlock": 0.65,
      "reference_unlock": 0.65
}',
    '{
      "wall_art_premium": {
            "min_cos": 0.8,
            "min_image_width_px": 4000,
            "min_quality_score": 0.75
      },
      "wall_art_standard": {
            "min_cos": 0.65,
            "min_image_width_px": 2000,
            "min_quality_score": 0.55
      },
      "calendar": {
            "min_cos": 0.65,
            "min_composition_fit": 0.6
      },
      "puzzle": {
            "min_cos": 0.6,
            "min_composition_fit": 0.65
      },
      "card": {
            "min_cos": 0.55,
            "min_image_width_px": 1200,
            "min_quality_score": 0.5
      },
      "book_illustration": {
            "min_publishing_score": 0.7,
            "min_identification_confidence": 0.85
      },
      "educational": {
            "min_reference_score": 0.65
      },
      "museum_print": {
            "min_museum_score": 0.8,
            "illustrator_prestige": 1.0,
            "min_rights_confidence": 1.0
      },
      "institutional_license": {
            "min_museum_score": 0.8,
            "min_rights_confidence": 1.0
      }
}',
    '{"seeded_for": "commerce_benchmark_fixture_v1"}'
)
ON CONFLICT (version) DO UPDATE SET
    changelog = EXCLUDED.changelog,
    formula_spec = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.formula_spec
        ELSE commerce_policy.formula_spec
    END,
    composite_weights = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.composite_weights
        ELSE commerce_policy.composite_weights
    END,
    tier_thresholds = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.tier_thresholds
        ELSE commerce_policy.tier_thresholds
    END,
    hard_gate_values = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.hard_gate_values
        ELSE commerce_policy.hard_gate_values
    END,
    model_activation_thresholds = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.model_activation_thresholds
        ELSE commerce_policy.model_activation_thresholds
    END,
    product_surface_requirements = CASE
        WHEN commerce_policy.status = 'draft' THEN EXCLUDED.product_surface_requirements
        ELSE commerce_policy.product_surface_requirements
    END,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
