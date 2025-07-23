import logging
from datetime import datetime
from enum import Enum

class ErrorCodes:
    """Tüm error kodları ve açıklamalarını içeren class"""
    
    ERROR_FETCHING_JSON_FROM = {
        "name": "ERR_FETCHING_JSON_FROM",
        "desc": "Json Fetching Hatası!",
        "code": "209"
    }
    
    ERROR_SEARCH_DATA = {
        "name": "ERR_SEARCH_DATA",
        "desc": "Anime arama verisi alınamadı!",
        "code": "210"
    }
    
    ERROR_STREAM_URL = {
        "name": "ERR_STREAM_URL",
        "desc": "Stream URL alınamadı!",
        "code": "211"
    }
    
    ERROR_NETWORK = {
        "name": "ERR_NETWORK",
        "desc": "Ağ bağlantı hatası!",
        "code": "212"
    }
    
    ERROR_INVALID_RESPONSE = {
        "name": "ERR_INVALID_RESPONSE",
        "desc": "Geçersiz API yanıtı!",
        "code": "213"
    }
    
    ERROR_SEASON_DATA = {
        "name": "ERR_SEASON_DATA",
        "desc": "Sezon verisi alınamadı!",
        "code": "214"
    }
    
    ERROR_EPISODE_DATA = {
        "name": "ERR_EPISODE_DATA",
        "desc": "Bölüm verisi alınamadı!",
        "code": "215"
    }
    
    ERROR_MOVIE_DATA = {
        "name": "ERR_MOVIE_DATA",
        "desc": "Film verisi alınamadı!",
        "code": "216"
    }
    
    ERROR_MOVIE_URL = {
        "name": "ERR_MOVIE_URL",
        "desc": "Film URL verisi alınamadı!",
        "code": "217"
    }

class AnimeciError(Exception):
    
    def __init__(self, error_info, original_error=None, url=None):
        self.name = error_info["name"]
        self.desc = error_info["desc"]
        self.code = error_info["code"]
        self.original_error = original_error
        self.url = url
        self.timestamp = datetime.now()
        
        message = f"[{self.code}] {self.name}: {self.desc}"
        if url:
            message += f" (URL: {url})"
        if original_error:
            message += f" (Original: {str(original_error)})"
            
        super().__init__(message)

class ErrorHandler:
    
    
    def __init__(self, log_level=logging.INFO, logger_name='AnimeciAPI'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        
        # Console handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_error(self, error_info, original_error=None, url=None, raise_exception=False):
        
        error_msg = f"[{error_info['code']}] {error_info['name']}: {error_info['desc']}"
        if url:
            error_msg += f" (URL: {url})"
        if original_error:
            error_msg += f" (Original: {str(original_error)})"
            
        self.logger.error(error_msg)
        
        # Eğer exception fırlatılması isteniyorsa
        if raise_exception:
            raise AnimeciError(error_info, original_error, url)
    
    def log_warning(self, message):
        """Warning log'u"""
        self.logger.warning(message)
    
    def log_info(self, message):
        """Info log'u"""
        self.logger.info(message)
    
    def log_debug(self, message):
        """Debug log'u"""
        self.logger.debug(message)
