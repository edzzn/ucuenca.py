ucuenca.py
==========

|Build Status| |PyPI version|

Descripción
-----------

Librería de Python para la API de la Universidad de Cuenca.

Dependencias
------------

-  Python 3.3 o superior.
-  El paquete
   `requests <http://docs.python-requests.org/en/master/user/install/>`__
   debe estar instalado.

Instalación
-----------

Pip
~~~

::

    pip install ucuenca

Manual
~~~~~~

::

    git clone https://github.com/stsewd/ucuenca.py.git
    pip install .

Documentación
-------------

Inicio Rápido
~~~~~~~~~~~~~

.. code:: python

    from ucuenca import Ucuenca

    uc = Ucuenca(lowercase_keys=True)

    careers = uc.careers('0104926787')
    careers['malla']  # MALLA CONTABILIDAD Y AUDITORIA 2008
    careers['fecha_matricula']  # 2013-03-03 09:37:08.0

.. |Build Status| image:: https://travis-ci.com/stsewd/ucuenca.py.svg?token=tZwnW7qE7enKf3J5KbrM&branch=master
   :target: https://travis-ci.com/stsewd/ucuenca.py
.. |PyPI version| image:: https://badge.fury.io/py/ucuenca.svg
   :target: https://badge.fury.io/py/ucuenca