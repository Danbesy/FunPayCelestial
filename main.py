import Utils.config_loader as cfg_loader
from first_setup import first_setup
from colorama import Fore, Style
import Utils.logger
from Utils.logger import LOGGER_CONFIG
import logging.config
import colorama
import sys
import os
from celestial import Celestial
import Utils.exceptions as excs
from locales.localizer import Localizer

logo = f"""
{Fore.WHITE}{Style.BRIGHT}███████╗██╗   ██╗███╗   ██╗██████╗  █████╗ ██╗   ██╗
██╔════╝██║   ██║████╗  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
█████╗  ██║   ██║██╔██╗ ██║██████╔╝███████║ ╚████╔╝ 
██╔══╝  ██║   ██║██║╚██╗██║██╔═══╝ ██╔══██║  ╚██╔╝  
██║     ╚██████╔╝██║ ╚████║██║     ██║  ██║   ██║   
╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝   ╚═╝{Style.RESET_ALL}                                                                                                  
      
                  {Fore.MAGENTA}{Style.BRIGHT}
 ██████╗███████╗██╗     ███████╗███████╗████████╗██╗ █████╗ ██╗     
██╔════╝██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔══██╗██║     
██║     █████╗  ██║     █████╗  ███████╗   ██║   ██║███████║██║     
██║     ██╔══╝  ██║     ██╔══╝  ╚════██║   ██║   ██║██╔══██║██║     
╚██████╗███████╗███████╗███████╗███████║   ██║   ██║██║  ██║███████╗
 ╚═════╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═╝╚══════╝
                                                                    
{Style.RESET_ALL}
"""

VERSION = "0.1.0"


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

folders = ["configs", "logs", "storage", "storage/cache", "storage/plugins", "storage/products"]
for i in folders:
    if not os.path.exists(i):
        os.makedirs(i)

files = ["configs/auto_delivery.cfg", "configs/auto_response.cfg"]
for i in files:
    if not os.path.exists(i):
        with open(i, "w", encoding="utf-8") as f:
            ...


if os.path.exists("storage/cache/block_list.json"):
    os.rename("storage/cache/block_list.json", "storage/cache/blacklist.json")


colorama.init()


logging.config.dictConfig(LOGGER_CONFIG)
logging.raiseExceptions = False
logger = logging.getLogger("main")
logger.debug("------------------------------------------------------------------")


print(logo)
print(f"{Fore.WHITE}{Style.BRIGHT}v{VERSION}{Style.RESET_ALL}\n")
print(f"{Fore.MAGENTA}{Style.BRIGHT}By {Fore.WHITE}{Style.BRIGHT}Danbesy{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Telegram: {Fore.WHITE}{Style.BRIGHT}https://t.me/Danbesy{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * FunPay: {Fore.WHITE}{Style.BRIGHT}https://funpay.com/users/1143244/{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * GitHub: {Fore.WHITE}{Style.BRIGHT}https://github.com/Danbesy/FunPayCelestial\n\n\n")


if not os.path.exists("configs/_main.cfg"):
    first_setup()
    sys.exit()


try:
    logger.info("$MAGENTAЗагружаю конфиг _main.cfg...")
    MAIN_CFG = cfg_loader.load_main_config("configs/_main.cfg")
    localizer = Localizer(MAIN_CFG["Other"]["language"])
    _ = localizer.translate

    logger.info("$MAGENTAЗагружаю конфиг auto_response.cfg...")
    AR_CFG = cfg_loader.load_auto_response_config("configs/auto_response.cfg")
    RAW_AR_CFG = cfg_loader.load_raw_auto_response_config("configs/auto_response.cfg")

    logger.info("$MAGENTAЗагружаю конфиг auto_delivery.cfg...")
    AD_CFG = cfg_loader.load_auto_delivery_config("configs/auto_delivery.cfg")
except excs.ConfigParseError as e:
    logger.error(e)
    logger.error("Завершаю программу...")
    sys.exit()
except UnicodeDecodeError:
    logger.error("Произошла ошибка при расшифровке UTF-8. Убедитесь, что кодировка файла = UTF-8, "
                 "а формат конца строк = LF.")
    logger.error("Завершаю программу...")
    sys.exit()
except:
    logger.critical("Произошла непредвиденная ошибка.")
    logger.debug("TRACEBACK", exc_info=True)
    logger.error("Завершаю программу...")
    sys.exit()

localizer = Localizer(MAIN_CFG["Other"]["language"])

try:
    Celestial(MAIN_CFG, AD_CFG, AR_CFG, RAW_AR_CFG, VERSION).init().run()
except KeyboardInterrupt:
    logger.info("Завершаю программу...")
    sys.exit()
except:
    logger.critical("При работе FPC произошла необработанная ошибка.")
    logger.debug("TRACEBACK", exc_info=True)
    logger.critical("Завершаю программу...")
    sys.exit()
