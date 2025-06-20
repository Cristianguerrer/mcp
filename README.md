# 🧠✨ MCP Pokémon Server

¡Conecta a Claude con el mundo Pokémon!  
Este proyecto es un **servidor MCP en Python** que expone herramientas para consultar la PokéAPI y brindarle a Claude (u otros clientes MCP) acceso en tiempo real a datos de Pokémon.

> 🐍 Desarrollado con Python + FastMCP + HTTPX  
> ⚡ Compatible con Claude Desktop vía configuración `mcpServers`

---

## 🎮 ¿Qué puede hacer?

Actualmente este servidor permite:

- 🔎 Buscar datos de un Pokémon por nombre (`get_pokemon`)
- 📋 Listar Pokémon por cantidad (`get_pokemon_list`)
- 💡 Consultar habilidades (`get_ability`)
- ⚔️ Analizar tipos y sus fortalezas/debilidades (`get_type`)
- 🧬 Ver la especie de un Pokémon (`get_species`)
- 🔁 Mostrar la cadena evolutiva (`get_evolution_chain`)

---

## 🚀 Cómo usarlo

### 1. Requisitos

- Python 3.10 o superior
- [`uv`](https://astral.sh/uv) (instalador de paquetes y entorno virtual)
- Claude Desktop instalado (opcional, para integración)

### 2. Instalación

```bash
uv init mcp-pokemon
cd mcp-pokemon
uv venv
.\.venv\Scripts\activate
uv add mcp[cli] httpx
```

### 3. Agrega el archivo `pokemon.py`

Puedes usar el código del servidor que se encuentra en este repositorio.

### 4. Ejecutar el servidor

```bash
uv run pokemon.py
```

---

## 🧩 Integración con Claude Desktop

Edita el archivo de configuración en:

```bash
%APPDATA%\Claude\claude_desktop_config.json
```

Y agrega:

```json
{
  "mcpServers": {
    "pokemon": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\RUTA\\AL\\PROYECTO\\mcp-pokemon",
        "run",
        "pokemon.py"
      ]
    }
  }
}
```

> 🔁 Reinicia Claude Desktop para aplicar los cambios.

---

## 📸 Ejemplo de uso

**Consulta:**
> “Dame los datos del Pokémon Pikachu”

**Respuesta (via MCP):**
```
Nombre: Pikachu
Tipos: electric
Habilidades: static, lightning-rod
Peso: 60 hectogramos
```

---

## 🛠️ ¿Qué es MCP?

> MCP (Model Context Protocol) permite a modelos como Claude ejecutar herramientas externas de forma controlada y segura.

Más info en: [MCP Spec](https://github.com/anthropics/mcp)

---

## 🤝 Contribuciones

¡Bienvenido a colaborar! Puedes ayudar a mejorar el formato, añadir más herramientas como:

- Stats base
- Sprites/imágenes
- Movimientos
- Comparativas entre Pokémon

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

## ⭐ Créditos

- [PokéAPI](https://pokeapi.co/) – fuente oficial de datos
- [Anthropic Claude](https://www.anthropic.com) – cliente LLM
- [uv by Astral](https://astral.sh/uv) – entorno y gestor de paquetes Python ultrarrápido

