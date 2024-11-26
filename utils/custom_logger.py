import datetime
import inspect


class CustomLogger:
    @staticmethod
    def get_dynamic_origin():
        """Obtém o nome do módulo ou função de onde o logger foi chamado."""
        frame = inspect.currentframe().f_back.f_back
        module = inspect.getmodule(frame)
        function_name = frame.f_code.co_name
        instance = frame.f_locals.get('self', None)

        module_name = module.__name__ if module else "UnkownModule"
        class_name = instance.__class__.__name__ if instance else None
        origin = f"{module_name}.{class_name}.{function_name}" if class_name else f"{module_name}.{function_name}"
        return origin

    @staticmethod
    def format_message(level, origin, message):
        """Formata a mensagem de log com data, origem e nível."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        return f"[{timestamp}][{origin}] {level} - {message}"

    @staticmethod
    def info(message, origin=None):
        """Loga uma mensagem com nível INFO."""
        origin = origin or CustomLogger.get_dynamic_origin()
        formatted_message = CustomLogger.format_message("INFO", origin, message)
        print(formatted_message)

    @staticmethod
    def warning(message, origin=None):
        """Loga uma mensagem com nível WARNING."""
        origin = origin or CustomLogger.get_dynamic_origin()
        formatted_message = CustomLogger.format_message("WARN", origin, message)
        print(formatted_message)

    @staticmethod
    def error(message, origin=None):
        """Loga uma mensagem com nível ERROR."""
        origin = origin or CustomLogger.get_dynamic_origin()
        formatted_message = CustomLogger.format_message("ERROR", origin, message)
        print(formatted_message)

    @staticmethod
    def debug(message, origin=None):
        """Loga uma mensagem com nível DEBUG."""
        origin = origin or CustomLogger.get_dynamic_origin()
        formatted_message = CustomLogger.format_message("DEBUG", origin, message)
        print(formatted_message)

    @staticmethod
    def critical(message, origin=None):
        """Loga uma mensagem com nível CRITICAL."""
        origin = origin or CustomLogger.get_dynamic_origin()
        formatted_message = CustomLogger.format_message("CRITICAL", origin, message)
        print(formatted_message)