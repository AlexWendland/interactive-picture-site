import uvicorn


def run():
    uvicorn.run(
        "interactive_picture_site.main:app",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    run()
