export type CoverageMapPoint = {
  placeSlug: string;
  displayName: string;
  designationFamily: string;
  latitude: number;
  longitude: number;
};

export const coverageSummary = {
  totalCandidates: 218,
  mappedCandidates: 175,
  missingCoordinateCandidates: 43,
  sourceObservedOnly: 218,
  unverified: 0,
  needsReview: 0,
  canonicalIdentityWritten: false
};

export const coverageRegions = [
  {
    "region": "Africa",
    "count": 15
  },
  {
    "region": "Asia",
    "count": 48
  },
  {
    "region": "Central America",
    "count": 2
  },
  {
    "region": "Eurasia",
    "count": 6
  },
  {
    "region": "Europe",
    "count": 96
  },
  {
    "region": "North America",
    "count": 8
  },
  {
    "region": "Oceania",
    "count": 6
  },
  {
    "region": "South America",
    "count": 7
  },
  {
    "region": "Transregional",
    "count": 30
  }
];

export const coverageDesignationCounts = [
  {
    "designation": "Biosphere",
    "count": 42
  },
  {
    "designation": "Geopark",
    "count": 45
  },
  {
    "designation": "ICH",
    "count": 43
  },
  {
    "designation": "Ramsar",
    "count": 45
  },
  {
    "designation": "UNESCO",
    "count": 43
  }
];

export const coverageCollectionFamilies = [
  {
    "family": "biosphere_collection",
    "count": 42
  },
  {
    "family": "geopark_collection",
    "count": 45
  },
  {
    "family": "ich_collection",
    "count": 43
  },
  {
    "family": "wetland_collection",
    "count": 45
  },
  {
    "family": "world_heritage_collection",
    "count": 43
  }
];

export const coverageCollectionReviewGaps = [
  {
    "family": "geopark_collection",
    "count": 45
  },
  {
    "family": "ich_collection",
    "count": 43
  },
  {
    "family": "wetland_collection",
    "count": 45
  }
];

export const coverageMissingCollectionFamilies = [
  "dark_sky_collection",
  "marine_collection"
];

export const coverageMapPoints: CoverageMapPoint[] = [
  {
    "placeSlug": "ak-zhayik",
    "displayName": "Ak-Zhayik",
    "designationFamily": "Biosphere",
    "latitude": 46.9167,
    "longitude": 51.75
  },
  {
    "placeSlug": "al-ahsa-oasis",
    "displayName": "Al-Ahsa Oasis",
    "designationFamily": "UNESCO",
    "latitude": 25.429444,
    "longitude": 49.621944
  },
  {
    "placeSlug": "alakol",
    "displayName": "Alakol",
    "designationFamily": "Biosphere",
    "latitude": 46.1833,
    "longitude": 81.7667
  },
  {
    "placeSlug": "aland-elbe-niederung-und-elbaue-jerichow",
    "displayName": "Aland-Elbe-Niederung und Elbaue Jerichow",
    "designationFamily": "Ramsar",
    "latitude": 52.75,
    "longitude": 11.816666666667
  },
  {
    "placeSlug": "artists-colony-in-darmstadt",
    "displayName": "Artists' Colony in Darmstadt",
    "designationFamily": "UNESCO",
    "latitude": 49.87543334529,
    "longitude": 8.6665039701752
  },
  {
    "placeSlug": "arxan",
    "displayName": "Arxan",
    "designationFamily": "Geopark",
    "latitude": 47.174166666667,
    "longitude": 119.93888888889
  },
  {
    "placeSlug": "aya",
    "displayName": "Aya",
    "designationFamily": "Biosphere",
    "latitude": 32.0567,
    "longitude": 131.1906
  },
  {
    "placeSlug": "ait-benhaddou",
    "displayName": "A\u00eft Benhaddou",
    "designationFamily": "UNESCO",
    "latitude": 31.05,
    "longitude": -7.1333333333333
  },
  {
    "placeSlug": "babelsberg-park",
    "displayName": "Babelsberg Park",
    "designationFamily": "UNESCO",
    "latitude": 52.405386,
    "longitude": 13.092721
  },
  {
    "placeSlug": "bashkirskiyi-ural",
    "displayName": "Bashkirskiyi Ural",
    "designationFamily": "Biosphere",
    "latitude": 53.0022,
    "longitude": 56.75
  },
  {
    "placeSlug": "bhimbetka-rock-shelters",
    "displayName": "Bhimbetka rock shelters",
    "designationFamily": "UNESCO",
    "latitude": 22.93863333,
    "longitude": 77.61438056
  },
  {
    "placeSlug": "bohemian-paradise",
    "displayName": "Bohemian Paradise",
    "designationFamily": "Geopark",
    "latitude": 50.519722,
    "longitude": 15.170556
  },
  {
    "placeSlug": "boyana-church",
    "displayName": "Boyana Church",
    "designationFamily": "UNESCO",
    "latitude": 42.644672222222,
    "longitude": 23.266172222222
  },
  {
    "placeSlug": "bru-na-boinne",
    "displayName": "Br\u00fa na B\u00f3inne",
    "designationFamily": "UNESCO",
    "latitude": 53.69284,
    "longitude": -6.44932
  },
  {
    "placeSlug": "bura-a",
    "displayName": "Bura'a",
    "designationFamily": "Biosphere",
    "latitude": 15.11,
    "longitude": 43.31
  },
  {
    "placeSlug": "cabo-de-gata-nijar-natural-park",
    "displayName": "Cabo de Gata-N\u00edjar Natural Park",
    "designationFamily": "Geopark",
    "latitude": 36.9,
    "longitude": -2.03
  },
  {
    "placeSlug": "cahokia",
    "displayName": "Cahokia",
    "designationFamily": "UNESCO",
    "latitude": 38.653888888889,
    "longitude": -90.064444444444
  },
  {
    "placeSlug": "cairngorm-lochs",
    "displayName": "Cairngorm Lochs",
    "designationFamily": "Ramsar",
    "latitude": 57.066666666667,
    "longitude": -3.7
  },
  {
    "placeSlug": "caithness-lochs",
    "displayName": "Caithness Lochs",
    "designationFamily": "Ramsar",
    "latitude": 58.516666666667,
    "longitude": -3.4333333333333
  },
  {
    "placeSlug": "caldeirao-do-corvo",
    "displayName": "Caldeir\u00e3o do Corvo",
    "designationFamily": "Ramsar",
    "latitude": 39.7,
    "longitude": -31.1
  },
  {
    "placeSlug": "cangshan",
    "displayName": "Cangshan",
    "designationFamily": "Geopark",
    "latitude": 25.648888888889,
    "longitude": 100.09805555556
  },
  {
    "placeSlug": "causses-du-quercy",
    "displayName": "Causses du Quercy",
    "designationFamily": "Geopark",
    "latitude": 44.593,
    "longitude": 1.683
  },
  {
    "placeSlug": "cerrado",
    "displayName": "Cerrado",
    "designationFamily": "UNESCO",
    "latitude": -14.005693888889,
    "longitude": -47.684611111111
  },
  {
    "placeSlug": "chan-chan",
    "displayName": "Chan Chan",
    "designationFamily": "UNESCO",
    "latitude": -8.1105555555556,
    "longitude": -79.075
  },
  {
    "placeSlug": "chauvet-cave",
    "displayName": "Chauvet Cave",
    "designationFamily": "UNESCO",
    "latitude": 44.3881219,
    "longitude": 4.4161408
  },
  {
    "placeSlug": "cheongsong",
    "displayName": "Cheongsong",
    "designationFamily": "Geopark",
    "latitude": 36.436111111111,
    "longitude": 129.05694444444
  },
  {
    "placeSlug": "ciletuh-palabuhanratu-geopark",
    "displayName": "Ciletuh-Palabuhanratu Geopark",
    "designationFamily": "Geopark",
    "latitude": -6.7686111111111,
    "longitude": 106.52611111111
  },
  {
    "placeSlug": "city-of-vicenza-and-the-palladian-villas-of-the-veneto",
    "displayName": "City of Vicenza and the Palladian Villas of the Veneto",
    "designationFamily": "UNESCO",
    "latitude": 45.55,
    "longitude": 11.55
  },
  {
    "placeSlug": "complexo-vulcanico-das-furnas",
    "displayName": "Complexo Vulc\u00e2nico das Furnas",
    "designationFamily": "Ramsar",
    "latitude": 37.75,
    "longitude": -25.316666666667
  },
  {
    "placeSlug": "dinosaur-provincial-park",
    "displayName": "Dinosaur Provincial Park",
    "designationFamily": "UNESCO",
    "latitude": 50.7617,
    "longitude": -111.485
  },
  {
    "placeSlug": "donauauen-donaumoos",
    "displayName": "Donauauen & Donaumoos",
    "designationFamily": "Ramsar",
    "latitude": 48.466666666667,
    "longitude": 10.216666666667
  },
  {
    "placeSlug": "dong-van-karst-plateau-unesco-global-geopark",
    "displayName": "Dong Van Karst Plateau UNESCO Global Geopark",
    "designationFamily": "Geopark",
    "latitude": 23.192222222222,
    "longitude": 105.19694444444
  },
  {
    "placeSlug": "dunhuang-yardang-national-geopark",
    "displayName": "Dunhuang Yardang National Geopark",
    "designationFamily": "Geopark",
    "latitude": 40.5305,
    "longitude": 93.0643
  },
  {
    "placeSlug": "east-coast-cape-barren-island-lagoons",
    "displayName": "East Coast Cape Barren Island Lagoons",
    "designationFamily": "Ramsar",
    "latitude": -40.366666666667,
    "longitude": 148.4
  },
  {
    "placeSlug": "east-sanday-coast",
    "displayName": "East Sanday Coast",
    "designationFamily": "Ramsar",
    "latitude": 59.26667,
    "longitude": -2.51667
  },
  {
    "placeSlug": "elbauen-schnackenburg-lauenburg",
    "displayName": "Elbauen, Schnackenburg-Lauenburg",
    "designationFamily": "Ramsar",
    "latitude": 53.116666666667,
    "longitude": 11.066666666667
  },
  {
    "placeSlug": "fuerteventura-biosphere-reserve",
    "displayName": "Fuerteventura Biosphere reserve",
    "designationFamily": "Biosphere",
    "latitude": 28.45,
    "longitude": -13.85
  },
  {
    "placeSlug": "garamba-national-park",
    "displayName": "Garamba National Park",
    "designationFamily": "UNESCO",
    "latitude": 4.19559,
    "longitude": 29.48093
  },
  {
    "placeSlug": "geoparque-mundial-de-la-unesco-comarca-minera-hidalgo",
    "displayName": "Geoparque Mundial de la UNESCO Comarca Minera, Hidalgo",
    "designationFamily": "Geopark",
    "latitude": 20.214722222222,
    "longitude": -98.730555555556
  },
  {
    "placeSlug": "geres-xures-transboundary-biosphere-reserve",
    "displayName": "Ger\u00eas-Xur\u00e9s Transboundary Biosphere Reserve",
    "designationFamily": "Biosphere",
    "latitude": 41.95,
    "longitude": -8.25
  },
  {
    "placeSlug": "glarus-thrust",
    "displayName": "Glarus thrust",
    "designationFamily": "UNESCO",
    "latitude": 46.91667,
    "longitude": 9.25
  },
  {
    "placeSlug": "glenelg-estuary-and-discovery-bay-wetlands",
    "displayName": "Glenelg Estuary and Discovery Bay Wetlands",
    "designationFamily": "Ramsar",
    "latitude": -38.083333333333,
    "longitude": 141.11666666667
  },
  {
    "placeSlug": "glienicke-palace",
    "displayName": "Glienicke Palace",
    "designationFamily": "UNESCO",
    "latitude": 52.4142,
    "longitude": 13.0953
  },
  {
    "placeSlug": "gobustan-state-historical-and-cultural-reserve",
    "displayName": "Gobustan State Historical and Cultural Reserve",
    "designationFamily": "UNESCO",
    "latitude": 40.10555556,
    "longitude": 49.38888889
  },
  {
    "placeSlug": "gochang",
    "displayName": "Gochang",
    "designationFamily": "Biosphere",
    "latitude": 35.483333333333,
    "longitude": 126.7
  },
  {
    "placeSlug": "goguryeo-tombs",
    "displayName": "Goguryeo tombs",
    "designationFamily": "UNESCO",
    "latitude": 38.863055555556,
    "longitude": 125.415
  },
  {
    "placeSlug": "gouritz-cluster",
    "displayName": "Gouritz Cluster",
    "designationFamily": "Biosphere",
    "latitude": -33.8681,
    "longitude": 21.6753
  },
  {
    "placeSlug": "gran-canaria-biosphere-reserve",
    "displayName": "Gran Canaria Biosphere Reserve",
    "designationFamily": "Biosphere",
    "latitude": 27.95,
    "longitude": -15.63
  },
  {
    "placeSlug": "guangwushan-nuoshuihe",
    "displayName": "Guangwushan-Nuoshuihe",
    "designationFamily": "Geopark",
    "latitude": 32.311666666667,
    "longitude": 106.63638888889
  },
  {
    "placeSlug": "gunbower-forest",
    "displayName": "Gunbower Forest",
    "designationFamily": "Ramsar",
    "latitude": -35.816666666667,
    "longitude": 144.31666666667
  },
  {
    "placeSlug": "hanma",
    "displayName": "Hanma",
    "designationFamily": "Biosphere",
    "latitude": 51.59,
    "longitude": 122.6792
  },
  {
    "placeSlug": "huanggang-dabieshan",
    "displayName": "Huanggang Dabieshan",
    "designationFamily": "Geopark",
    "latitude": 30.729444444444,
    "longitude": 115.05361111111
  },
  {
    "placeSlug": "inlay-lake",
    "displayName": "Inlay Lake",
    "designationFamily": "Biosphere",
    "latitude": 20.45,
    "longitude": 96.8333
  },
  {
    "placeSlug": "island-of-mozambique",
    "displayName": "Island of Mozambique",
    "designationFamily": "UNESCO",
    "latitude": -15.036666666667,
    "longitude": 40.732777777778
  },
  {
    "placeSlug": "island-of-principe-biosphere-reserve",
    "displayName": "Island of Pr\u00edncipe Biosphere Reserve",
    "designationFamily": "Biosphere",
    "latitude": 1.583333,
    "longitude": 7.383333
  },
  {
    "placeSlug": "ismaninger-speichersee-fischteichen",
    "displayName": "Ismaninger Speichersee & Fischteichen",
    "designationFamily": "Ramsar",
    "latitude": 48.216666666667,
    "longitude": 11.666666666667
  },
  {
    "placeSlug": "izu-peninsula-geopark",
    "displayName": "Izu Peninsula Geopark",
    "designationFamily": "Geopark",
    "latitude": 34.97269444,
    "longitude": 138.93330556
  },
  {
    "placeSlug": "jau-national-park",
    "displayName": "Ja\u00fa National Park",
    "designationFamily": "UNESCO",
    "latitude": -2.1702777777778,
    "longitude": -62.617222222222
  },
  {
    "placeSlug": "jeju-island-unesco-global-geopark",
    "displayName": "Jeju Island UNESCO Global Geopark",
    "designationFamily": "Geopark",
    "latitude": 33.5,
    "longitude": 126.57
  },
  {
    "placeSlug": "kasubi-tombs",
    "displayName": "Kasubi Tombs",
    "designationFamily": "UNESCO",
    "latitude": 0.32916666666667,
    "longitude": 32.553333333333
  }
];
