from flask import Flask, request, jsonify
from g4f.client import Client
import re
import asyncio

# Initialize Flask app
app = Flask(__name__)


# Function to clean up response
def filter_strings(strings):
    clean_text = re.sub(r"```json|```", "", strings)
    return clean_text


# Function to process truck data and get the response from GPT model
async def process_truck_data(truck_data):
    client = Client()

    # Prepare the message for the API call
    message = f"""
                You are an intelligent assistant specialized in analyzing truck specifications to determine the estimated capacity for loading household items.
    Based on the given input, calculate the estimated load capacity, recommend suitable household items to load, and respond strictly in JSON format.
    Follow the rules carefully.

    ### Ruleset:

     1. Input Rules:
    - Input will be a single JSON object containing details about the truck, including:
        - manufacturer (string): The manufacturer of the truck.
        - model (string): The truck's model name.
        - type (string): The type of truck (e.g., flatbed, box truck, etc.).
        - year (number): The manufacturing year of the truck.
        - startingRate (number): The starting rental rate in dollars.
        - estimatedItems (number): The estimated number of items that need to be loaded.
        - units (number): The unit count available for loading (e.g., number of pallets, boxes, etc.).
        - dimensions (string): Dimensions of the truck (formatted as length x width x height in meters).

    2. Response Rules:
    - Respond strictly in JSON format.
    - Replace the annotated ```json into " " (space)
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
        - `kitchenware` (array): Recommended kitchenware items (e.g., pots, pans, utensils).
        - `bathroomEssentials` (array): Bathroom essentials (e.g., towels, toiletries).
        - `bedroomEssentials` (array): Bedroom essentials (e.g., bed linens, pillows).
        - `wallDecor` (array): Wall décor (e.g., pictures, mirrors).
        - `floorDecor` (array): Floor décor (e.g., rugs, mats).
        - `closetStorage` (array): Closet storage items (e.g., hangers, storage bins).
        - `generalStorage` (array): General storage items (e.g., boxes, containers).
        - `electronics` (array): Electronics (e.g., TVs, laptops, lamps).
        - `officeSupplies` (array): Office supplies (e.g., desks, chairs, filing cabinets).
        - `hobbiesAndRecreation` (array): Hobbies and recreation items (e.g., books, sports equipment).
        - `outdoorItems` (array): Outdoor items (e.g., garden tools, chairs).
        - `safety` (array): Safety items (e.g., fire extinguisher, first aid kit).
        - `utilities` (array): Utility items (e.g., extension cords, light bulbs).
        - `miscellaneous` (array): Miscellaneous items (e.g., decorations, knick-knacks).

    3. Constraints:
    - If `dimensions` is missing or improperly formatted, include a warning in `warnings`.
    - If `estimatedItems` exceeds `maxItems`, include a warning.
    - Use truck `totalVolume` and average sizes of household items to determine recommendations:
        - Large truck (20+ m³): Suitable for multiple large appliances and furniture.
        - Medium truck (10–20 m³): Suitable for some appliances and furniture with boxes.
        - Small truck (<10 m³): Best for small furniture and boxes.

    Input:
    {truck_data}
    
     Output:
    {{
    "truckDetails": {{
    "manufacturer": "{truck_data["manufacturer"]}",
    "model": "{truck_data["model"]}",
    "type": "{truck_data["truck_type"]}",
    "year": {truck_data["year"]},
    "startingRate": {truck_data["starting_rate"]},
    "estimatedItems": {truck_data["estimated_items"]},
    "units": {truck_data["units"]},
    "dimensions": "{truck_data["dimensions"]}"
    }},
    "capacityEstimation": {{
    "totalVolume": "The calculated total volume of the truck in cubic meters",
    "maxItems": "The maximum number of items the truck can hold based on its dimensions",
    "utilizationRate": "A descriptive string about the truck's capacity utilization",
    "warnings": ["A list of warnings if any issues are identified, or an empty array if none"]
    }},
    "recommendedItems": {{
    "appliances": ["A list of recommended appliances based on the truck's capacity"],
    "furniture": ["A list of recommended furniture based on the truck's capacity"],
    "others": ["A list of other suitable items for loading"],
    "kitchenware": ["A list of recommended kitchenware items"],
    "bathroomEssentials": ["A list of bathroom essentials"],
    "bedroomEssentials": ["A list of bedroom essentials"],
    "wallDecor": ["A list of wall décor items"],
    "floorDecor": ["A list of floor décor items"],
    "closetStorage": ["A list of closet storage items"],
    "generalStorage": ["A list of general storage items"],
    "electronics": ["A list of electronics"],
    "officeSupplies": ["A list of office supplies"],
    "hobbiesAndRecreation": ["A list of hobbies and recreation items"],
    "outdoorItems": ["A list of outdoor items"],
    "safety": ["A list of safety items"],
    "utilities": ["A list of utility items"],
    "miscellaneous": ["A list of miscellaneous items"]
    }}
    }}
    """

    # Call GPT model with prepared message
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": message}]
    )

    output = response.choices[0].message.content
    return filter_strings(output)


# Flask route to handle POST request
@app.route("/estimate-capacity", methods=["POST"])
async def estimate_capacity():
    # Get JSON data from the request body
    truck_data = request.json

    # Validate required fields
    required_fields = [
        "manufacturer",
        "model",
        "type",
        "year",
        "startingRate",
        "estimatedItems",
        "units",
        "dimensions",
    ]
    for field in required_fields:
        if field not in truck_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Process truck data asynchronously and return the response
    response_data = await process_truck_data(truck_data)
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
