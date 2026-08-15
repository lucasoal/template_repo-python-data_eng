import logging
import os
from time import sleep

from dotenv import load_dotenv
from quati.navigation.automation import launch_navigator, save_session_cookies
from selenium.webdriver.common.by import By

from include.src.core.base_extractor import BaseExtractor
from include.src.utils.paths import ASSETS, TMP

load_dotenv()

logger = logging.getLogger(__name__)


class ExemplePipeline(BaseExtractor):
    """Classe responsável por autenticar no Instagram via Selenium e salvar os cookies de sessão."""

    def __init__(self, something: str = "blal-bla-bla"):
        super().__init__()
        self.something = something

    def _prtsc(self, browser, saveat: str = TMP) -> None:
        browser.save_screenshot(f"{saveat}/view.png")

    def execute(self) -> bool:
        """Executa a rotina de login e exportação do arquivo .pkl"""
        if not self.usr or not self.psswd:
            raise ValueError(
                "Credenciais do Instagram (INSTAGRAM_USR / INSTAGRAM_PSSWD) não foram encontradas."
            )

        BUTTON_USERNAME = "//input[@name='email']"
        BUTTON_PASSWORD = "//input[@name='pass']"
        BUTTON_LOGIN = "//*[text()='Log in']"
        BUTTON_SAVE_INFO = "//*[text()='Save info']"
        BUTTON_IGNORE_SUSPECT = "//*[text()='Ignore']"

        try:
            logger.info(f"Opening browser • {self.url}")
            browser = launch_navigator(self.url, True, True, None)
            self._prtsc(browser)
            sleep(15)

            logger.info(f"Input username and password for user {self.usr}")
            browser.find_element(By.XPATH, BUTTON_USERNAME).send_keys(self.usr)
            browser.find_element(By.XPATH, BUTTON_PASSWORD).send_keys(self.psswd)

            logger.info("Click login button")
            browser.find_element(By.XPATH, BUTTON_LOGIN).click()
            sleep(15)

            for btn_xpath in [BUTTON_SAVE_INFO, BUTTON_IGNORE_SUSPECT]:
                try:
                    browser.find_element(By.XPATH, btn_xpath).click()
                    sleep(15)
                except Exception:
                    pass

            logger.info("Saving cookies")
            os.makedirs(os.path.dirname(self.cookie_path), exist_ok=True)

            saved = save_session_cookies(self.cookie_path, browser)
            browser.quit()

            if (
                not os.path.exists(self.cookie_path)
                or os.path.getsize(self.cookie_path) == 0
            ):
                raise RuntimeError(
                    f"Falha ao salvar o arquivo de cookies em '{self.cookie_path}'."
                )

            return True

        except Exception as e:
            logger.error(f"Erro crítico no pipeline de cookies: {e}")
            raise e
