from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_indent = 2

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if log_record.get('levelname'):
            log_record['levelname'] = log_record['levelname'].upper()
        else:
            log_record['levelname'] = record.levelname

        log_record['asctime'] = record.asctime
        log_record['message'] = record.message
        log_record['pathname'] = record.pathname
        log_record['funcName'] = record.funcName
        log_record['lineno'] = record.lineno
