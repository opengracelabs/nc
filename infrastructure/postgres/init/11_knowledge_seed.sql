-- Seed the knowledge concept vocabulary.
-- OUV criteria i–x with canonical UNESCO descriptions.
-- Heritage types and institutional actors.
-- These URIs are the authority — all facts and relationships reference them.

INSERT INTO concepts (uri, label, description, type, status) VALUES

    -- OUV Criteria (Cultural: i–vi, Natural: vii–x)
    ('whc:criterion/i',
     '{"en": "Masterpiece of Human Creative Genius"}',
     '{"en": "Represents a masterpiece of human creative genius."}',
     'criterion', 'active'),

    ('whc:criterion/ii',
     '{"en": "Important Interchange of Human Values"}',
     '{"en": "Exhibits an important interchange of human values, over a span of time or within a cultural area of the world, on developments in architecture or technology, monumental arts, town-planning or landscape design."}',
     'criterion', 'active'),

    ('whc:criterion/iii',
     '{"en": "Unique or Exceptional Testimony to Cultural Tradition"}',
     '{"en": "Bears a unique or at least exceptional testimony to a cultural tradition or to a civilization which is living or which has disappeared."}',
     'criterion', 'active'),

    ('whc:criterion/iv',
     '{"en": "Outstanding Example of a Type of Building or Landscape"}',
     '{"en": "Is an outstanding example of a type of building, architectural or technological ensemble or landscape which illustrates significant stages in human history."}',
     'criterion', 'active'),

    ('whc:criterion/v',
     '{"en": "Outstanding Example of Traditional Human Settlement"}',
     '{"en": "Is an outstanding example of a traditional human settlement, land-use, or sea-use which is representative of a culture, or human interaction with the environment, especially when it has become vulnerable under the impact of irreversible change."}',
     'criterion', 'active'),

    ('whc:criterion/vi',
     '{"en": "Directly Associated with Events or Living Traditions"}',
     '{"en": "Is directly or tangibly associated with events or living traditions, with ideas, or with beliefs, with artistic and literary works of outstanding universal significance."}',
     'criterion', 'active'),

    ('whc:criterion/vii',
     '{"en": "Superlative Natural Phenomena or Exceptional Natural Beauty"}',
     '{"en": "Contains superlative natural phenomena or areas of exceptional natural beauty and aesthetic importance."}',
     'criterion', 'active'),

    ('whc:criterion/viii',
     '{"en": "Outstanding Examples of Earth History"}',
     '{"en": "Is an outstanding example representing major stages of earth''s history, including the record of life, significant on-going geological processes in the development of landforms, or significant geomorphic or physiographic features."}',
     'criterion', 'active'),

    ('whc:criterion/ix',
     '{"en": "Outstanding Examples of Ecological and Biological Processes"}',
     '{"en": "Is an outstanding example representing significant on-going ecological and biological processes in the evolution and development of terrestrial, fresh water, coastal and marine ecosystems and communities of plants and animals."}',
     'criterion', 'active'),

    ('whc:criterion/x',
     '{"en": "Most Important Natural Habitats for Biodiversity Conservation"}',
     '{"en": "Contains the most important and significant natural habitats for in-situ conservation of biological diversity, including those containing threatened species of outstanding universal value from the point of view of science or conservation."}',
     'criterion', 'active'),

    -- Heritage types
    ('whc:type/natural',
     '{"en": "Natural Heritage"}',
     '{"en": "Sites inscribed for their outstanding natural values under criteria vii–x."}',
     'heritage_type', 'active'),

    ('whc:type/cultural',
     '{"en": "Cultural Heritage"}',
     '{"en": "Sites inscribed for their outstanding cultural values under criteria i–vi."}',
     'heritage_type', 'active'),

    ('whc:type/mixed',
     '{"en": "Mixed Heritage"}',
     '{"en": "Sites inscribed for outstanding natural and cultural values under both sets of criteria."}',
     'heritage_type', 'active'),

    -- Institutional actors
    ('whc:org/unesco',
     '{"en": "UNESCO World Heritage Committee"}',
     '{"en": "The United Nations Educational, Scientific and Cultural Organization body responsible for implementing the World Heritage Convention."}',
     'actor', 'active'),

    ('iucn:org/iucn',
     '{"en": "International Union for Conservation of Nature"}',
     '{"en": "The world''s leading conservation organization; advisory body to the WHC for natural and mixed sites."}',
     'actor', 'active'),

    ('icomos:org/icomos',
     '{"en": "International Council on Monuments and Sites"}',
     '{"en": "Advisory body to the WHC for cultural and mixed sites."}',
     'actor', 'active')

ON CONFLICT (uri) DO NOTHING;
