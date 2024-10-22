# PSStoreJSON

## Usage
`python main.py <dlc file> <country> <language> <Service ID Prefix> <Title ID>`

### Example
`python main.py "downloadables.dlc" gb en EP9000 BCES00141`

## Description
PSStoreJSON is a utility for collecting LittleBigPlanet™ downloadable content metadata from Playstation®Store content using the **ContentID** section from the native downloadable content locking format, a.k.a. `*.dlc`. The script uses undocumented API endpoints to collect the data.

## To-Do List
- [ ] Add "InGameCommerceID" support (partially complete)
- [ ] Test with LittleBigPlanet™ PS Vita™ releases DLC file
- [ ] Add SerialStation CSV support
