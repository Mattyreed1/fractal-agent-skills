---
name: google-maps
description: Google Maps operations via MCP tools. Use when finding places by query (restaurants, hotels, businesses), getting place details (hours, rating, phone, address), calculating directions or distance matrix, estimating travel time, geocoding addresses to coordinates, reverse geocoding coordinates to addresses, or doing elevation lookups. Triggers on "google maps", "find places near", "directions to", "how long does it take to get to", "geocode", "place details".
---

# Google Maps Skill

Use Google Maps MCP tools for place search, geocoding, directions, and travel time calculations.

## Available Tools

All tool names below are prefixed `mcp__google-maps__` (e.g. `mcp__google-maps__maps_search_places`).

| Tool | Use For |
|------|---------|
| `maps_search_places` | Find places by query (restaurants, hotels, etc.) |
| `maps_place_details` | Get hours, rating, phone, address for a place_id |
| `maps_geocode` | Address → coordinates |
| `maps_reverse_geocode` | Coordinates → address |
| `maps_directions` | Turn-by-turn directions between two points |
| `maps_distance_matrix` | Travel time/distance for multiple origin-destination pairs |
| `maps_elevation` | Elevation data for coordinates |

## Common Patterns

### Search → Details
```
1. maps_search_places(query="coffee shops near Union Square, San Francisco")
2. maps_place_details(place_id="ChIJ...") // from search results
```

### Address → Directions
```
1. maps_geocode(address="123 Main St, City") // if needed
2. maps_directions(origin="123 Main St", destination="456 Oak Ave", mode="driving")
```

### Travel Time Matrix
```
maps_distance_matrix(
  origins=["Home address", "Office address"],
  destinations=["Airport", "Downtown"],
  mode="driving"
)
```

## Modes
- `driving` (default)
- `walking`
- `bicycling`
- `transit`

## Calendar Integration

Combine with the `google-calendar` skill (gws CLI) for location-aware scheduling:
- Search place → add event with location
- Get travel time between consecutive meetings
- Find restaurants near meeting location

## Limitations
- Cannot manage personal Google Maps saved places/lists (no API exists)
- Place search returns limited results per query
