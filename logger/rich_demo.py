import logging

from rich.logging import RichHandler

if __name__ == "__main__":  # pragma: no cover
    from time import sleep

    FORMAT = "%(message)s"
    # FORMAT = "%(asctime)-15s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level="NOTSET",
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )
    log = logging.getLogger("rich")

    log.info("Server starting...")
    log.info("Listening on http://127.0.0.1:8080")
    sleep(1)

    log.info("GET /index.html 200 1298")
    log.info("GET /imgs/backgrounds/back1.jpg 200 54386")
    log.info("GET /css/styles.css 200 54386")
    log.warning("GET /favicon.ico 404 242")
    sleep(1)

    log.debug(
        "JSONRPC request\n--> %r\n<-- %r",
        {
            "version": "1.1",
            "method": "confirmFruitPurchase",
            "params": [["apple", "orange", "mangoes", "pomelo"], 1.123],
            "id": "194521489",
        },
        {"version": "1.1", "result": True, "error": None, "id": "194521489"},
    )
    log.debug(
        "Loading configuration file /adasd/asdasd/qeqwe/qwrqwrqwr/sdgsdgsdg/werwerwer/dfgerert/ertertert/ertetert/werwerwer"
    )
    log.error("Unable to find 'pomelo' in database!")
    log.info("POST /jsonrpc/ 200 65532")
    log.info("POST /admin/ 401 42234")
    log.warning("password was rejected for admin site.")

    def divide() -> None:
        number = 1
        divisor = 0
        foos = ["foo"] * 100
        log.debug("in divide")
        try:
            number / divisor
        except:
            log.exception("An error of some kind occurred!")

    divide()
    sleep(1)
    log.critical("Out of memory!")
    log.info("Server exited with code=-1")
    log.info("[bold]EXITING...[/bold]", extra=dict(markup=True))