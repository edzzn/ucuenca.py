import time
import requests

# TODO: html parser for status requests
# TODO: upload to pypi

BASE_URL = "http://evaluacion.ucuenca.edu.ec/ucuenca-rest-ws/api/v1/"
MAX_RETRIES = 10
DELAY = 0.5


class UcuencaException(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg

    def __str__(self):
        return "status code: {status_code} - {msg}".format(
            status_code=self.status_code,
            msg=self.msg,
        )


class Ucuenca:
    def __init__(self, token=None, lowercase_keys=False):
        self.token = token
        self.lowercase_keys = lowercase_keys

    def _get(self, service_name, params=None):
        url = self._get_url(service_name)
        response = self._request(
            url,
            params
        )
        return self._parse_response(response)

    def _get_url(self, field):
        return "{}{}".format(BASE_URL, field)

    def _request(self, url, params=None):
        retries = MAX_RETRIES
        delay = DELAY

        while retries:
            try:
                return self._get_response(url, params)
            except UcuencaException as e:
                if retries == 1 or e.status_code == 404:
                    raise e
            except Exception:
                if retries == 1:
                    raise UcuencaException(1, "Unknow error.")
            retries -= 1
            time.sleep(delay)
            delay += DELAY

    def _get_response(self, url, params):
        response = requests.get(url, params)
        status_code = response.status_code
        if status_code != 200:
            raise UcuencaException(status_code, "Error")
        elif status_code == 404:
            raise UcuencaException(404, "Resource not found.")
        return response

    def _parse_response(self, response):
        headers = response.headers
        if 'json' in headers['content-type']:
            result = response.json()
            if self.lowercase_keys:
                result = [
                    self._keys_to_lower_case(r)
                    for r in result
                ]
        else:
            raise UcuencaException(2, "Unknow response.")
        return result

    @staticmethod
    def _keys_to_lower_case(dictionary):
        return {
            k.lower(): v
            for k, v in dictionary.items()
        }

    def careers(self, student_id):
        """Returns the careers that a student has taken given an id."""
        response = self._get(
            service_name='registroacademico',
            params={'idEstudiante': student_id}
        )
        return None if not response else response[0]

    def notes(self, student_id, career_id, period_id):
        """Returns the notes of a student given an id, career, and perdiod."""
        response = self._get(
            service_name='registroacademico/notas',
            params={
                'idEstudiante': student_id,
                'idCarrera': career_id,
                'idPerlec': period_id
            }
        )
        return None if not response else response[0]

    def schedule(self, student_id):
        """Returns the current schedule of a student given an id."""
        response = self._get(
            service_name='horarios',
            params={'idEstudiante': student_id}
        )
        return None if not response else response[0]

    def curriculum_progress(self, student_id, career_id, curriculum_id, career_plan):
        """Returns the curriculum progress of a student."""
        response = self._get(
            service_name='registroacademico/malla',
            params={
                'idEstudiante': student_id,
                'idCarrera': career_id,
                'idMalla': curriculum_id,
                'idPlacar': career_plan
            }
        )
        return None if not response else response
