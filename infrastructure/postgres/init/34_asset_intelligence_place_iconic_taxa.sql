-- v0.5.4 Phase 1 / Migration 34.
-- Place iconic taxa registry and flagship place seeds.
--
-- PostgreSQL is authoritative.
-- Replay-safe by registry_version and pinned signal snapshots.
-- Versioned registries.
-- No Commerce Intelligence formula redesign.
-- No Product Routing redesign.
-- No Catalog redesign.
-- No Publication redesign.

CREATE TABLE IF NOT EXISTS place_iconic_taxa_registry (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registry_version      TEXT NOT NULL,
    place_key             TEXT NOT NULL,
    place_label           TEXT NOT NULL,
    place_id              UUID REFERENCES places(id),
    concept_id            UUID REFERENCES concepts(id),
    taxon_key             TEXT NOT NULL,
    scientific_name       TEXT NOT NULL,
    common_name           TEXT,
    anchor_type           TEXT NOT NULL REFERENCES commerce_anchor_type_vocabulary(value) DEFAULT 'biological',
    iconic_score          NUMERIC(4,3) NOT NULL CHECK (iconic_score BETWEEN 0 AND 1),
    authority_confidence  NUMERIC(4,3) NOT NULL CHECK (authority_confidence BETWEEN 0 AND 1),
    iconic_rationale      TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','active','retired')),
    authored_by           TEXT NOT NULL,
    approved_by           TEXT,
    approved_at           TIMESTAMPTZ,
    provenance            JSONB NOT NULL DEFAULT '{}',
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (registry_version, place_key, taxon_key),
    CONSTRAINT chk_place_iconic_taxa_registry_approval CHECK (
        status != 'active'
        OR (approved_by IS NOT NULL AND approved_at IS NOT NULL AND approved_by IS DISTINCT FROM authored_by)
    )
);

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_registry_active
    ON place_iconic_taxa_registry(registry_version, place_key, iconic_score DESC)
    WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_place_iconic_taxa_registry_taxon
    ON place_iconic_taxa_registry(registry_version, taxon_key)
    WHERE status = 'active';

DROP TRIGGER IF EXISTS trg_place_iconic_taxa_registry_updated_at ON place_iconic_taxa_registry;
CREATE TRIGGER trg_place_iconic_taxa_registry_updated_at
    BEFORE UPDATE ON place_iconic_taxa_registry
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

WITH seeds(place_key, place_label, taxon_key, scientific_name, common_name, iconic_score, authority_confidence, iconic_rationale) AS (
    VALUES
        ('yellowstone', 'Yellowstone National Park', 'bison-bison', 'Bison bison', 'American bison', 1.000::numeric, 0.950::numeric, 'Flagship Yellowstone wildlife subject.'),
        ('yellowstone', 'Yellowstone National Park', 'canis-lupus', 'Canis lupus', 'Gray wolf', 0.970::numeric, 0.930::numeric, 'Iconic reintroduction and trophic cascade subject.'),
        ('yellowstone', 'Yellowstone National Park', 'ursus-arctos-horribilis', 'Ursus arctos horribilis', 'Grizzly bear', 0.960::numeric, 0.930::numeric, 'High-recognition Yellowstone apex species.'),
        ('yellowstone', 'Yellowstone National Park', 'cervus-canadensis', 'Cervus canadensis', 'Elk', 0.900::numeric, 0.900::numeric, 'Common and visually recognizable Yellowstone subject.'),
        ('yellowstone', 'Yellowstone National Park', 'haliaeetus-leucocephalus', 'Haliaeetus leucocephalus', 'Bald eagle', 0.850::numeric, 0.880::numeric, 'Recognizable protected bird associated with the region.'),
        ('yosemite', 'Yosemite National Park', 'ursus-americanus', 'Ursus americanus', 'American black bear', 0.930::numeric, 0.900::numeric, 'Iconic Yosemite wildlife subject.'),
        ('yosemite', 'Yosemite National Park', 'ovis-canadensis-sierrae', 'Ovis canadensis sierrae', 'Sierra Nevada bighorn sheep', 0.920::numeric, 0.880::numeric, 'High-value Sierra conservation subject.'),
        ('yosemite', 'Yosemite National Park', 'sequoiadendron-giganteum', 'Sequoiadendron giganteum', 'Giant sequoia', 0.960::numeric, 0.940::numeric, 'Flagship Yosemite botanical subject.'),
        ('yosemite', 'Yosemite National Park', 'falco-peregrinus', 'Falco peregrinus', 'Peregrine falcon', 0.840::numeric, 0.850::numeric, 'Recognizable cliff and conservation subject.'),
        ('yosemite', 'Yosemite National Park', 'lynx-rufus', 'Lynx rufus', 'Bobcat', 0.780::numeric, 0.820::numeric, 'Recognizable Yosemite wildlife subject.'),
        ('grand-canyon', 'Grand Canyon National Park', 'gymnogyps-californianus', 'Gymnogyps californianus', 'California condor', 1.000::numeric, 0.950::numeric, 'Flagship Grand Canyon conservation subject.'),
        ('grand-canyon', 'Grand Canyon National Park', 'ovis-canadensis-nelsoni', 'Ovis canadensis nelsoni', 'Desert bighorn sheep', 0.930::numeric, 0.900::numeric, 'Iconic canyon wildlife subject.'),
        ('grand-canyon', 'Grand Canyon National Park', 'aquila-chrysaetos', 'Aquila chrysaetos', 'Golden eagle', 0.850::numeric, 0.840::numeric, 'Recognizable canyon raptor.'),
        ('grand-canyon', 'Grand Canyon National Park', 'crotalus-oreganus-abyssus', 'Crotalus oreganus abyssus', 'Grand Canyon rattlesnake', 0.820::numeric, 0.830::numeric, 'Place-specific reptile subject.'),
        ('grand-canyon', 'Grand Canyon National Park', 'cervus-canadensis', 'Cervus canadensis', 'Elk', 0.760::numeric, 0.800::numeric, 'Visible and recognizable park wildlife.'),
        ('everglades', 'Everglades National Park', 'alligator-mississippiensis', 'Alligator mississippiensis', 'American alligator', 1.000::numeric, 0.960::numeric, 'Flagship Everglades wildlife subject.'),
        ('everglades', 'Everglades National Park', 'crocodylus-acutus', 'Crocodylus acutus', 'American crocodile', 0.940::numeric, 0.900::numeric, 'Distinctive Everglades reptile subject.'),
        ('everglades', 'Everglades National Park', 'platalea-ajaja', 'Platalea ajaja', 'Roseate spoonbill', 0.920::numeric, 0.900::numeric, 'High-recognition Everglades bird subject.'),
        ('everglades', 'Everglades National Park', 'ardea-herodias', 'Ardea herodias', 'Great blue heron', 0.840::numeric, 0.850::numeric, 'Common visual wetland subject.'),
        ('everglades', 'Everglades National Park', 'trichechus-manatus', 'Trichechus manatus', 'West Indian manatee', 0.900::numeric, 0.880::numeric, 'Iconic Florida aquatic mammal.'),
        ('galapagos', 'Galapagos Islands', 'chelonoidis-niger', 'Chelonoidis niger', 'Galapagos giant tortoise', 1.000::numeric, 0.970::numeric, 'Flagship Galapagos species.'),
        ('galapagos', 'Galapagos Islands', 'amblyrhynchus-cristatus', 'Amblyrhynchus cristatus', 'Marine iguana', 0.980::numeric, 0.950::numeric, 'Distinctive endemic Galapagos subject.'),
        ('galapagos', 'Galapagos Islands', 'spheniscus-mendiculus', 'Spheniscus mendiculus', 'Galapagos penguin', 0.940::numeric, 0.920::numeric, 'Endemic and high-recognition bird subject.'),
        ('galapagos', 'Galapagos Islands', 'fregata-magnificens', 'Fregata magnificens', 'Magnificent frigatebird', 0.880::numeric, 0.860::numeric, 'Visually distinctive Galapagos bird subject.'),
        ('galapagos', 'Galapagos Islands', 'sula-nebouxii', 'Sula nebouxii', 'Blue-footed booby', 0.960::numeric, 0.930::numeric, 'High-recognition Galapagos bird subject.')
)
INSERT INTO place_iconic_taxa_registry (
    registry_version, place_key, place_label, place_id, concept_id, taxon_key,
    scientific_name, common_name, anchor_type, iconic_score, authority_confidence,
    iconic_rationale, status, authored_by, approved_by, approved_at, provenance
)
SELECT
    '1.0.0',
    s.place_key,
    s.place_label,
    p.id,
    c.id,
    s.taxon_key,
    s.scientific_name,
    s.common_name,
    'biological',
    s.iconic_score,
    s.authority_confidence,
    s.iconic_rationale,
    'active',
    'migration_34_asset_intelligence_place_iconic_taxa',
    'migration_34_second_human',
    NOW(),
    '{"migration": "34_asset_intelligence_place_iconic_taxa"}'::jsonb
FROM seeds s
LEFT JOIN places p
  ON lower(p.name::text) LIKE '%' || replace(s.place_key, '-', '%') || '%'
LEFT JOIN concepts c
  ON lower(c.label::text) LIKE '%' || lower(s.scientific_name) || '%'
ON CONFLICT (registry_version, place_key, taxon_key) DO UPDATE SET
    place_label = EXCLUDED.place_label,
    place_id = EXCLUDED.place_id,
    concept_id = EXCLUDED.concept_id,
    scientific_name = EXCLUDED.scientific_name,
    common_name = EXCLUDED.common_name,
    anchor_type = EXCLUDED.anchor_type,
    iconic_score = EXCLUDED.iconic_score,
    authority_confidence = EXCLUDED.authority_confidence,
    iconic_rationale = EXCLUDED.iconic_rationale,
    status = EXCLUDED.status,
    approved_by = EXCLUDED.approved_by,
    approved_at = EXCLUDED.approved_at,
    provenance = EXCLUDED.provenance,
    updated_at = NOW();
