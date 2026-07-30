"""OpenSearch result logger plugin.

Indexes test results into an OpenSearch cluster, one document per test run.

Configuration keys (all values are strings in pavilion.yaml):
    plugin        (required) Must be "opensearch".
    host          (optional) OpenSearch host. Default: 10.200.0.254
    port          (optional) OpenSearch port. Default: 9200
    index         (optional) Index name. Default: pavilion-results
    use_ssl       (optional) "true" to use HTTPS. Default: true
    verify_certs  (optional) "true" to verify SSL certificates. Default: false
    username      (optional) HTTP Basic auth username.
    password      (optional) HTTP Basic auth password.

Example pavilion.yaml entry:
    result_loggers:
      - plugin: opensearch
        host: 10.200.0.254
        index: pavilion-results
"""

import json
import logging
from typing import Dict, Optional, TextIO

from pavilion import output
from pavilion.errors import ResultLoggerPluginError
from pavilion.result_logging.base_classes import ResultLoggerPlugin, ResultLogger

LOGGER = logging.getLogger(__file__)

_DEFAULT_HOST = '10.200.0.254'
_DEFAULT_PORT = 9200
_DEFAULT_INDEX = 'pavilion-results'


def _str_bool(val: str, default: bool) -> bool:
    if not val:
        return default
    return val.strip().lower() in ('true', '1', 'yes')


class OpenSearchLoggerFactory(ResultLoggerPlugin):
    """Factory plugin for the 'opensearch' result logger."""

    def __init__(self):
        super().__init__(
            name='opensearch',
            description='Index test results into an OpenSearch cluster.',
            priority=self.PRIO_COMMON,
        )

    def validate_config(self, config: Dict) -> None:
        if config.get('plugin') != self.name:
            raise ResultLoggerPluginError(
                "Name {} does not match plugin type {}.".format(
                    config.get('plugin'), self.name))

        port_str = config.get('port', str(_DEFAULT_PORT))
        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                raise ValueError()
        except (TypeError, ValueError):
            raise ResultLoggerPluginError(
                "opensearch 'port' must be an integer 1-65535; got: {}".format(port_str))

    def _make_logger(self,
                     config: Dict,
                     sid: str,
                     outfile: Optional[TextIO] = None) -> 'OpenSearchResultLogger':
        host = config.get('host', _DEFAULT_HOST).strip()
        port = int(config.get('port', str(_DEFAULT_PORT)))
        index = config.get('index', _DEFAULT_INDEX).strip()
        use_ssl = _str_bool(config.get('use_ssl', ''), default=True)
        verify_certs = _str_bool(config.get('verify_certs', ''), default=False)
        username = config.get('username', '').strip() or None
        password = config.get('password', '').strip() or None

        return OpenSearchResultLogger(
            host=host,
            port=port,
            index=index,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            username=username,
            password=password,
            outfile=outfile,
        )


class OpenSearchResultLogger(ResultLogger):
    """Indexes one document per test result into OpenSearch.

    Nested result fields (dicts, lists) are sent as-is so OpenSearch can
    map them as nested objects.  A '@timestamp' field is added from the
    test's 'finished' time (falling back to 'started' or 'created') so
    that time-based dashboards work out of the box.
    """

    def __init__(self,
                 host: str,
                 port: int,
                 index: str,
                 use_ssl: bool,
                 verify_certs: bool,
                 username: Optional[str],
                 password: Optional[str],
                 outfile: Optional[TextIO] = None):
        import io
        self.host = host
        self.port = port
        self.index = index
        self.use_ssl = use_ssl
        self.verify_certs = verify_certs
        self.username = username
        self.password = password
        self.outfile = outfile or io.StringIO()

    def _get_client(self):
        """Build and return an OpenSearch client."""
        from opensearchpy import OpenSearch

        kwargs = {
            'hosts': [{'host': self.host, 'port': self.port}],
            'use_ssl': self.use_ssl,
            'verify_certs': self.verify_certs,
            'ssl_show_warn': False,
        }

        if self.username and self.password:
            kwargs['http_auth'] = (self.username, self.password)

        return OpenSearch(**kwargs)

    def log(self, results: Dict) -> None:
        output.fprint(
            self.outfile,
            "{}: Indexing {} ({}) into {}...".format(
                type(self).__name__,
                results.get('name', '?'),
                results.get('result', '?'),
                self.index))

        doc = dict(results)

        # Rename 'id' → 'pav_id': the bare name 'id' conflicts with OpenSearch's
        # reserved _id field and causes mapping collisions with integer mappings.
        if 'id' in doc:
            doc['pav_id'] = str(doc.pop('id'))

        # Add @timestamp (ISO 8601) for Kibana/OpenSearch Dashboards compatibility.
        ts = doc.get('finished') or doc.get('started') or doc.get('created')
        if ts:
            try:
                from datetime import datetime, timezone
                doc['@timestamp'] = datetime.fromtimestamp(
                    float(ts), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            except (TypeError, ValueError, OSError):
                doc['@timestamp'] = str(ts)

        try:
            client = self._get_client()
            response = client.index(index=self.index, body=doc)
            output.fprint(
                self.outfile,
                "{}: Indexed as _id={} result={}".format(
                    type(self).__name__,
                    response.get('_id', '?'),
                    response.get('result', '?')))
        except Exception as err:  # pylint: disable=broad-except
            output.fprint(
                self.outfile,
                "{}: Failed to index result: {}".format(
                    type(self).__name__, err))
            LOGGER.warning("opensearch_logger: failed to index result for "
                           "test '%s': %s", results.get('name', '?'), err)
