from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pokemon")

POKEAPI_BASE = "https://pokeapi.co/api/v2/"

async def fetch_pokemon_data(endpoint: str) -> dict[str, Any] | None:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{POKEAPI_BASE}{endpoint}", timeout=20.0)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return None

@mcp.tool()
async def get_pokemon(name: str) -> str:
    """Obtiene información básica de un Pokémon por nombre"""
    data = await fetch_pokemon_data(f"pokemon/{name.lower()}")

    if not data:
        return f"No se encontró información para el Pokémon: {name}"

    types = ', '.join(t["type"]["name"] for t in data["types"])
    abilities = ', '.join(a["ability"]["name"] for a in data["abilities"])
    weight = data["weight"]

    return f"""
Nombre: {data['name'].title()}
Tipos: {types}
Habilidades: {abilities}
Peso: {weight} hectogramos
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
