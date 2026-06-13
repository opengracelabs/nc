export type PlaceFactoryDashboardRow = {
  place: string;
  authority: string;
  collectionFamily: string;
  discoveryFamily: string;
  commerceReadiness: "Ready" | "Review" | "Hold";
  designationFamily: string;
  graphReadiness: "Ready" | "Review" | "Hold";
};

export const placeFactoryDashboardRows: PlaceFactoryDashboardRow[] = [
  {
    place: "Yellowstone",
    authority: "Source observed",
    collectionFamily: "World Heritage Collection",
    discoveryFamily: "Heritage Discovery",
    commerceReadiness: "Review",
    designationFamily: "UNESCO",
    graphReadiness: "Ready"
  },
  {
    place: "Sian Ka'an Biosphere Reserve",
    authority: "Source observed",
    collectionFamily: "Biosphere Collection",
    discoveryFamily: "Ecology Discovery",
    commerceReadiness: "Review",
    designationFamily: "Biosphere",
    graphReadiness: "Ready"
  },
  {
    place: "Arouca Geopark",
    authority: "Source observed",
    collectionFamily: "Geopark Collection",
    discoveryFamily: "Geology Discovery",
    commerceReadiness: "Hold",
    designationFamily: "Geopark",
    graphReadiness: "Ready"
  },
  {
    place: "Okavango Delta",
    authority: "Source observed",
    collectionFamily: "Wetland Collection",
    discoveryFamily: "Water Discovery",
    commerceReadiness: "Hold",
    designationFamily: "Ramsar",
    graphReadiness: "Ready"
  },
  {
    place: "Pacific Wayfinding",
    authority: "Source observed",
    collectionFamily: "ICH Collection",
    discoveryFamily: "Culture Discovery",
    commerceReadiness: "Review",
    designationFamily: "ICH",
    graphReadiness: "Review"
  }
];

export const placeFactoryDashboardSummary = {
  scaleTarget: "10,000 places",
  supportedFamilies: [
    "UNESCO",
    "Biosphere",
    "Geopark",
    "Ramsar",
    "ICH",
  ],
  rows: placeFactoryDashboardRows.length
};
