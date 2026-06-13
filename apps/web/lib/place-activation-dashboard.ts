export type ActivationReadiness = "Ready" | "Review" | "Hold";

export type ActivationDashboardRow = {
  placeSlug: string;
  place: string;
  country: string;
  region: string;
  designationFamily: string;
  collectionFamily: string;
  authorityReadiness: ActivationReadiness;
  collectionReadiness: ActivationReadiness;
  productReadiness: ActivationReadiness;
  graphReadiness: ActivationReadiness;
  publishingReadiness: ActivationReadiness;
  activationScore: number;
};

export const activationDashboardSummary = {
  totalCandidates: 218,
  topPlaceCount: 25,
  canonicalIdentityWritten: false
};

export type ActivationReadinessCounts = Partial<Record<ActivationReadiness, number>>;

export const activationReadinessCounts: {
  authority: ActivationReadinessCounts;
  collection: ActivationReadinessCounts;
  product: ActivationReadinessCounts;
  graph: ActivationReadinessCounts;
  publishing: ActivationReadinessCounts;
} = {
  authority: {
  "Review": 218
},
  collection: {
  "Ready": 85,
  "Review": 133
},
  product: {
  "Hold": 43,
  "Review": 175
},
  graph: {
  "Ready": 43,
  "Review": 175
},
  publishing: {
  "Hold": 43,
  "Review": 175
}
};

export const activationDashboardRows: ActivationDashboardRow[] = [
  {
    "placeSlug": "pont-saint-benezet",
    "place": "pont Saint-B\u00e9n\u00e9zet",
    "country": "France",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "isimangaliso-wetland-park",
    "place": "iSimangaliso Wetland Park",
    "country": "South Africa",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "yungang-grottoes",
    "place": "Yungang Grottoes",
    "country": "People's Republic of China",
    "region": "Asia",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "vredefort-crater",
    "place": "Vredefort crater",
    "country": "South Africa",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "thracian-tomb-of-kazanlak",
    "place": "Thracian Tomb of Kazanlak",
    "country": "Bulgaria",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "tai-national-park",
    "place": "Ta\u00ef National Park",
    "country": "Ivory Coast",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "tadrart-acacus",
    "place": "Tadrart Acacus",
    "country": "Libya",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "stone-spheres-of-costa-rica",
    "place": "Stone spheres of Costa Rica",
    "country": "Costa Rica",
    "region": "Central America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "salonga-national-park",
    "place": "Salonga National Park",
    "country": "Democratic Republic of the Congo",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "sacred-island-of-okinoshima-and-associated-sites-in-the-munakata-region",
    "place": "Sacred Island of Okinoshima and Associated Sites in the Munakata Region",
    "country": "Japan",
    "region": "Asia",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "roman-monuments-cathedral-of-st-peter-and-church-of-our-lady-in-trier-unesco-world-heritage-site",
    "place": "Roman Monuments, Cathedral of St. Peter and Church of Our Lady in Trier UNESCO World Heritage Site",
    "country": "Germany",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "quirigua",
    "place": "Quirigu\u00e1",
    "country": "Guatemala",
    "region": "Central America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "q367395",
    "place": "Q367395",
    "country": "Hungary",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "q305044",
    "place": "Q305044",
    "country": "Bangladesh",
    "region": "Asia",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "putorana-plateau",
    "place": "Putorana Plateau",
    "country": "Russia",
    "region": "Eurasia",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "olympic-national-park",
    "place": "Olympic National Park",
    "country": "United States",
    "region": "North America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "margravial-opera-house",
    "place": "Margravial Opera House",
    "country": "Germany",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "madriu-perafita-claror-valley",
    "place": "Madriu-Perafita-Claror Valley",
    "country": "Andorra",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "madara-rider",
    "place": "Madara Rider",
    "country": "Bulgaria",
    "region": "Europe",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "los-katios-national-park",
    "place": "Los Kat\u00edos National Park",
    "country": "Colombia",
    "region": "South America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "liberty-island",
    "place": "Liberty Island",
    "country": "United States",
    "region": "North America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "lena-pillars",
    "place": "Lena Pillars",
    "country": "Russia",
    "region": "Eurasia",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "kasubi-tombs",
    "place": "Kasubi Tombs",
    "country": "Uganda",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "jau-national-park",
    "place": "Ja\u00fa National Park",
    "country": "Brazil",
    "region": "South America",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  },
  {
    "placeSlug": "island-of-mozambique",
    "place": "Island of Mozambique",
    "country": "Mozambique",
    "region": "Africa",
    "designationFamily": "UNESCO",
    "collectionFamily": "world_heritage_collection",
    "authorityReadiness": "Review",
    "collectionReadiness": "Ready",
    "productReadiness": "Review",
    "graphReadiness": "Ready",
    "publishingReadiness": "Review",
    "activationScore": 92
  }
];
