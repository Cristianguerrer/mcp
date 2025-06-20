from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pokemon")

POKEAPI_BASE = "https://pokeapi.co/api/v2/"

# Función genérica de consulta
async def fetch_pokemon_data(endpoint: str) -> dict[str, Any] | None:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{POKEAPI_BASE}{endpoint}", timeout=20.0)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return None

# Herramienta: Información básica de un Pokémon
@mcp.tool()
async def get_pokemon(name: str) -> str:
    """Obtiene información básica de un Pokémon por nombre"""
    data = await fetch_pokemon_data(f"pokemon/{name.lower()}")

    if not data:
        return f"No se encontró información para el Pokémon: {name}"

    types = ', '.join(t["type"]["name"] for t in data["types"])
    abilities = ', '.join(a["ability"]["name"] for a in data["abilities"])
    weight = data["weight"] / 10  # convertir a kg

    return f"""
Nombre: {data['name'].title()}
Tipos: {types.title()}
Habilidades: {abilities.title()}
Peso: {weight} kg
"""

# Herramienta: Listar Pokémon
@mcp.tool()
async def get_pokemon_list(limit: int = 10) -> str:
    """Devuelve una lista de nombres de Pokémon"""
    data = await fetch_pokemon_data(f"pokemon?limit={limit}&offset=0")

    if not data or "results" not in data:
        return "No se pudo obtener la lista de Pokémon."

    names = [p["name"].title() for p in data["results"]]
    return "\n".join(names)

# Herramienta: Detalles de una habilidad
@mcp.tool()
async def get_ability(name: str) -> str:
    """Obtiene información sobre una habilidad Pokémon"""
    data = await fetch_pokemon_data(f"ability/{name.lower()}")

    if not data:
        return f"No se encontró información para la habilidad: {name}"

    effect_entries = data.get("effect_entries", [])
    effect = next((entry["effect"] for entry in effect_entries if entry["language"]["name"] == "en"), "Sin descripción en inglés.")

    return f"""
Habilidad: {data["name"].title()}
Efecto: {effect}
"""

# Herramienta: Detalles de un tipo Pokémon
@mcp.tool()
async def get_type(type_id_or_name: str) -> str:
    """Obtiene información sobre un tipo Pokémon por nombre o ID"""
    data = await fetch_pokemon_data(f"type/{type_id_or_name.lower()}")

    if not data:
        return f"No se encontró información para el tipo: {type_id_or_name}"

    damage_relations = data.get("damage_relations", {})
    double_from = ', '.join([t['name'] for t in damage_relations.get('double_damage_from', [])])
    double_to = ', '.join([t['name'] for t in damage_relations.get('double_damage_to', [])])
    half_from = ', '.join([t['name'] for t in damage_relations.get('half_damage_from', [])])
    half_to = ', '.join([t['name'] for t in damage_relations.get('half_damage_to', [])])

    return f"""
Tipo: {data["name"].title()}
Doble daño de: {double_from or "Ninguno"}
Doble daño a: {double_to or "Ninguno"}
Mitad de daño de: {half_from or "Ninguno"}
Mitad de daño a: {half_to or "Ninguno"}
"""

# Herramienta: Especie de un Pokémon
@mcp.tool()
async def get_species(name: str) -> str:
    """Devuelve información de especie del Pokémon dado"""
    data = await fetch_pokemon_data(f"pokemon-species/{name.lower()}")

    if not data:
        return f"No se encontró información de especie para {name}."

    habitat = data["habitat"]["name"] if data.get("habitat") else "Desconocido"
    color = data["color"]["name"]
    shape = data["shape"]["name"]
    is_legendary = data["is_legendary"]
    is_mythical = data["is_mythical"]

    return f"""
Especie de {data['name'].title()}:
Color: {color}
Forma: {shape}
Hábitat: {habitat}
Legendario: {"Sí" if is_legendary else "No"}
Mítico: {"Sí" if is_mythical else "No"}
"""

# Herramienta: Cadena evolutiva
@mcp.tool()
async def get_evolution_chain(name: str) -> str:
    """Devuelve la cadena evolutiva de un Pokémon"""
    species = await fetch_pokemon_data(f"pokemon-species/{name.lower()}")
    if not species or "evolution_chain" not in species["urls"]:
        return f"No se encontró la cadena evolutiva para {name}."

    evo_url = species["evolution_chain"]["url"]
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(evo_url, timeout=20.0)
            resp.raise_for_status()
            evo_data = resp.json()
    except Exception:
        return "No se pudo obtener la cadena evolutiva."

    def extract_chain(chain: dict) -> list[str]:
        names = [chain["species"]["name"].title()]
        while chain.get("evolves_to"):
            chain = chain["evolves_to"][0]
            names.append(chain["species"]["name"].title())
        return names

    names = extract_chain(evo_data["chain"])
    return " → ".join(names)

# Ejecutar el servidor
if __name__ == "__main__":
    mcp.run(transport="stdio")
