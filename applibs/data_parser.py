from applibs.logging_utils import get_logger

logger = get_logger(__name__)


class DataParser:
    @staticmethod
    def render_token_data(token_data):
        try:
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "access_token_expiry_time": str(int(token_data["access_token_expiry_time"].total_seconds())),
                "refresh_token_expiry_time": str(int(token_data["refresh_token_expiry_time"].total_seconds()))
            }

        except Exception as e:
            logger.debug(repr(e))
            return {}


data_parser = DataParser()
