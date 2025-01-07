import logging
import logstash
import random
import json
import datetime
import dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

dotenv.load_dotenv()
test_logger = logging.getLogger('Service Name')
test_logger.setLevel(logging.DEBUG)
test_logger.addHandler(logstash.TCPLogstashHandler('localhost', 5959 , version=1))

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def vecotrize_log(log):
    stringified = json.dumps(log)
    log_embeddings = embeddings.embed_documents(texts=[stringified],task_type="RETRIEVAL_DOCUMENT")
    log['vector'] = log_embeddings[0]
    print(log_embeddings)
    return log

sample_stack_trace = """
    Sample stack trace string to be logged
    Traceback (most recent call last):
        File "logstash_script.py", line 90, in <module>
            test_logger.error(msg=sample_stack_trace ,extra=extra)
        File "/usr/lib/python3.8/logging/__init__.py", line 1447, in error
            self._log(ERROR, msg, args, **kwargs)
        File "/usr/lib/python3.8/logging/__init__.py", line 1511, in _log
            self.handle(record)
        File "/usr/lib/python3.8/logging/__init__.py", line 1521, in handle
            self.callHandlers(record)
        File "/usr/lib/python3.8/logging/__init__.py", line 1583, in callHandlers
            hdlr.handle(record)
        File "/usr/lib/python3.8/logging/handlers.py", line 150, in handle
            self.emit(record)
        File "/usr/lib/python3.8/logging/handlers.py", line 94, in emit
            self.send(s)
        File "/usr/lib/python3.8/logging/handlers.py", line 88, in send
            self.sock.sendall(s)
    ConnectionRefusedError: [Errno 111] Connection refused
    """

for i in range(10):
    extra = {
        "app_name": "The Debuggers",
        'time_stamp':datetime.datetime.now().isoformat(),
        'thread_count': random.randint(1, 100),
        'log_level': 'DEBUG',
        'log_type': 'logstash',
        'log_format': 'json',
        'log_message': 'Sample log message',
        'log_source': 'logstash',
    }
    
    if i <2:
        vectorized_log = vecotrize_log(extra)
        test_logger.debug("DEBUG", extra=vectorized_log)
    elif i>=2 and i<4:
        extra['log_level'] = 'INFO'
        vectorized_log = vecotrize_log(extra)
        test_logger.info('INFO', extra=vectorized_log)
    elif i>=4 and i<6:    
        extra['log_level'] = 'WARNING'
        vectorized_log = vecotrize_log(extra)
        test_logger.warning('WARNING', extra=vectorized_log)
    elif i>=6 and i<8:
        extra['log_level'] = 'ERROR'
        extra['log_message'] = sample_stack_trace
        vectorized_log = vecotrize_log(extra)
        test_logger.error('ERROR', extra=vectorized_log)
    else:
        extra['log_level'] = 'CRITICAL'
        vectorized_log = vecotrize_log(extra)
        test_logger.critical('CRITICAL', extra=vectorized_log)
