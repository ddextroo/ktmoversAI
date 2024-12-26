from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": """
               You are an intelligent assistant specialized in analyzing truck specifications to determine the estimated capacity for loading household items.
Based on the given input, calculate the estimated load capacity, recommend suitable household items to load, and respond strictly in JSON format.
Follow the rules carefully.

### Ruleset:

1. **Input Rules**:
   - Input will be a single JSON object containing details about the truck, including:
     - `manufacturer` (string): The manufacturer of the truck.
     - `model` (string): The truck's model name.
     - `type` (string): The type of truck (e.g., flatbed, box truck, etc.).
     - `year` (number): The manufacturing year of the truck.
     - `startingRate` (number): The starting rental rate in dollars.
     - `estimatedItems` (number): The estimated number of items that need to be loaded.
     - `units` (number): The unit count available for loading (e.g., number of pallets, boxes, etc.).
     - `dimensions` (string): Dimensions of the truck (formatted as `length x width x height` in meters).

2. **Response Rules**:
   - Respond strictly in JSON format.
   - Include the following keys in the response:
     - `truckDetails`: Mirror the truck details from the input.
     - `capacityEstimation`: Include:
       - `totalVolume` (number): Calculated total volume of the truck in cubic meters.
       - `maxItems` (number): The maximum estimated number of items that can fit based on the given dimensions.
       - `utilizationRate` (string): A recommendation string for how to best utilize the truck space (e.g., "Ideal for medium to large household moves").
       - `warnings` (array): Any warnings about capacity or incompatibilities.
     - `recommendedItems`: A list of recommended household items to load, categorized into:
       - `appliances` (array): Recommended appliances (e.g., refrigerator, washing machine).
       - `furniture` (array): Recommended furniture (e.g., sofa, bed frame).
       - `others` (array): Other recommended items (e.g., boxes, bikes, small tables).

3. **Constraints**:
   - If `dimensions` is missing or improperly formatted, include a warning in `warnings`.
   - If `estimatedItems` exceeds `maxItems`, include a warning.
   - Use truck `totalVolume` and average sizes of household items to determine recommendations:
     - Large truck (20+ m³): Suitable for multiple large appliances and furniture.
     - Medium truck (10–20 m³): Suitable for some appliances and furniture with boxes.
     - Small truck (<10 m³): Best for small furniture and boxes.

Input:
{
    "manufacturer": "Freightliner",
    "model": "Cascadia",
    "type": "Semi-Truck",
    "year": 2023,
    "startingRate": 150,
    "estimatedItems": 60,
    "units": 30,
    "dimensions": "8.0 x 2.5 x 4.0"
  },

### Example Output:
{
  "truckDetails": {
    "manufacturer": "The same manufacturer from the input",
    "model": "The same model from the input",
    "type": "The same type from the input",
    "year": "The same year from the input",
    "startingRate": "The same startingRate from the input",
    "estimatedItems": "The same estimatedItems from the input",
    "units": "The same units from the input",
    "dimensions": "The same dimensions from the input"
  },
  "capacityEstimation": {
    "totalVolume": "The calculated total volume of the truck in cubic meters",
    "maxItems": "The maximum number of items the truck can hold based on its dimensions",
    "utilizationRate": "A descriptive string about the truck's capacity utilization",
    "warnings": ["A list of warnings if any issues are identified, or an empty array if none"]
  },
  "recommendedItems": {
    "appliances": ["A list of recommended appliances based on the truck's capacity"],
    "furniture": ["A list of recommended furniture based on the truck's capacity"],
    "others": ["A list of other suitable items for loading"]
  }
}
               """,
        }
    ],
    # Add any other necessary parameters
)
print(response.choices[0].message)
