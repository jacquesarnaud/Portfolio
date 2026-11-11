def main() -> None:
    """Point d'entrée de développement."""
    import uvicorn

    uvicorn.run("python_ia.main:app", host="127.0.0.1", port=8000, reload=True)
