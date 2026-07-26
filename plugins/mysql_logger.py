"""MySQL result logger plugin.

Appends one row per test result into a MySQL/MariaDB table.

Connects locally with NO stored password: the OS user authenticates via the
unix_socket auth plugin, so pavilion.yaml carries no credentials.

Configuration keys (pavilion.yaml):
    plugin       (required) Must be "mysql".
    database     (required) Database name.
    table        (optional) Table name. Default: "results".
    unix_socket  (optional) Socket path. Default: "/var/lib/mysql/mysql.sock".
    host / user  (optional) For a networked server instead of the local socket.

Example pavilion.yaml entry:
    result_loggers:
      - plugin: mysql
        database: pavilion
        table: results
        unix_socket: /var/lib/mysql/mysql.sock
"""
import io
from typing import Dict, Optional, TextIO

from pavilion import output
from pavilion.errors import ResultLoggerPluginError
from pavilion.result_logging.base_classes import ResultLoggerPlugin, ResultLogger

try:
    import pymysql
except ImportError:
    pymysql = None


class MySqlLoggerFactory(ResultLoggerPlugin):
    """Factory plugin for the 'mysql' result logger."""

    def __init__(self):
        super().__init__(
            name='mysql',
            description='Log one row per test result into a MySQL/MariaDB table.',
            priority=self.PRIO_COMMON,
        )

    def validate_config(self, config: Dict) -> None:
        if config.get('plugin', '') != self.name:
            raise ResultLoggerPluginError(
                "Name {} does not match plugin type {}.".format(
                    config.get('plugin'), self.name))
        if not config.get('database'):
            raise ResultLoggerPluginError("mysql logger requires a 'database'.")
        if pymysql is None:
            raise ResultLoggerPluginError(
                "mysql logger requires the 'pymysql' package (pip install pymysql).")

    def _make_logger(self, config: Dict, sid: str,
                     outfile: Optional[TextIO] = None) -> 'MySqlResultLogger':
        return MySqlResultLogger(
            database=config['database'],
            table=config.get('table', 'results'),
            unix_socket=config.get('unix_socket', '/var/lib/mysql/mysql.sock'),
            host=config.get('host'),
            user=config.get('user'),
            outfile=outfile,
        )


class MySqlResultLogger(ResultLogger):
    """Inserts one row per test result. Passwordless local auth via unix_socket."""

    def __init__(self, database, table, unix_socket, host=None, user=None,
                 outfile: Optional[TextIO] = None):
        self.database = database
        self.table = table
        self.unix_socket = unix_socket
        self.host = host
        self.user = user
        self.outfile = outfile or io.StringIO()

    def _connect(self):
        kwargs = {'database': self.database}
        if self.host:
            kwargs['host'] = self.host
        else:
            kwargs['unix_socket'] = self.unix_socket
        if self.user:
            kwargs['user'] = self.user
        return pymysql.connect(**kwargs)

    def log(self, results: Dict) -> None:
        output.fprint(
            self.outfile,
            "MySqlResultLogger: logging {} ({}) to {}.{}...".format(
                results.get('name', '?'), results.get('result', '?'),
                self.database, self.table))

        row = (
            str(results.get('id', '')),
            str(results.get('name', '')),
            str(results.get('result', '')),
            str(results.get('sys_name', '')),
            results.get('duration'),
        )
        # Table name comes from trusted config, not test data — safe to format in.
        sql = ("INSERT INTO {} (pav_id, name, result, sys_name, duration) "
               "VALUES (%s, %s, %s, %s, %s)".format(self.table))
        try:
            conn = self._connect()
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, row)
                conn.commit()
            finally:
                conn.close()
        except Exception as err:
            # A logging failure must never break the test run — just warn and move on.
            output.fprint(self.outfile,
                          "mysql logger: skipped result ({})".format(err))
