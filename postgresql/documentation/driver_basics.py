##
# copyright 2009, James William Pye
# http://python.projects.postgresql.org
##
"""
`postgresql.driver`
===================

The `postgresql.driver` implements PG-API using PQ version 3.0 to connect to
PostgreSQL servers. It makes use of the protocol's extended features to provide
binary datatype transmission and protocol level prepared statements.

Connecting
----------

Connecting to PostgreSQL using `postgresql.driver` is very simple::

	>>> import postgresql.driver as pg_driver
	>>> pg_con = pg_driver.connect(user = 'usename', password = 'secret', host = 'localhost', port = 5432)

It's that easy.

NOTE: `connect` will *not* inherit parameters from the environment as
libpq-based drivers do. The `postgresql.documentation.driver_details` discusses
means of gathering standard client parameters.

Keyword parameters accepted by `connect`:

 user
  The user to connect as.
 password
  The user's password.
 database
  The database to connect to. (PostgreSQL defaults it to `user`)
 host
  The hostname or IP address to connect to.
 port
  The port on the host to connect to.
 settings
  A dictionary or key-value pair sequence stating the parameters to give to the
  database. These settings are included in the startup packet.

 connect_timeout
  Amount of time to wait for a connection to be made. (in seconds)
  Raises `postgresql.exceptions.ConnectionTimeoutError` when triggered.
 server_encoding
  Hint given to the driver to properly encode password data and some information
  in the startup packet.
  This should only be used in cases where connections cannot be made due to
  authentication failures that occur while using known-correct credentials.

 sslmode
  How do to decide whether or not to use SSL:
   'disallow'
    Don't allow SSL connections.
   'allow'
    Try without SSL, but if that doesn't work, try with.
   'prefer'
    Try SSL first, then without.
   'require'

 sslcrtfile
  Certificate file path given to `ssl.wrap_socket`.
 sslkeyfile
  Key file path given to `ssl.wrap_socket`.
 sslrootcrtfile
  Root certificate file path given to `ssl.wrap_socket`
 sslrootcrlfile
  Revocation list file path. [Throws a NotSupportedWarning]

From here on `db` will be assumed to exist and serve as the documentation's
`postresql.api.Connection` instance.

Querying
--------

Querying PostgreSQL is very easy. A statement object is created, a
`PreparedStatement` instance, using the `prepare` method on the connection
object::

	>>> my_statement = db.prepare("SELECT 'hello, world!'")

This creates a bound statement object, so it's only usable on the `db`
connection. While this may seem to be a trifle for some situations, it's very
handy to be able to pass around the statement object without having to explicitly
carry the connection object with it.

Now, to execute it::

	>>> my_results = my_statement()

Just like executing a function. In this case, invoking `my_statement` will return a
`Cursor` object to the result set.

NOTE: Don't confuse PG-API cursors with DB-API cursors. PG-API cursors are SQL
cursors and don't contain methods for executing more queries within the cursor.

Cursor objects have a couple ways to read data from them:

 ``next(my_results)``
  This fetches the next row in the cursor object. Cursors support the iterator
  protocol, you can just as easily:

 ``for nextrow in my_results:``
  This will, of course, get the ``nextrow`` in the cursor, ``my_results``, until
  the cursor is exhausted. This and the former way of reading rows use the same
  method, ``__next__``, which is part of the Iterator ABC.

 ``my_results.read(5)``
  This method name is borrowed from `file` objects, and are semantically
  similar. However, this being a cursor, rows are returned instead of bytes or
  characters. In this case, five rows are requested, but certainly only one will
  come back: ``[('hello, world!',)]``. When the number of rows returned is less
  then the number requested, it means that cursor has been exhausted, and there
  are no more rows to be read.

Cursors have other methods, but not for reading more tuples. These other methods
will be discuessed later.

As cursors have a couple methods for reading tuples, queries a few methods for
executing the prepared statement:

 ``__call__(...)``
  As shown before, statement objects can be simply invoked like a function to get a
  cursor to the statement's results.

 ``first(...)``
  For simple queries, a cursor object can be a bit tiresome to get data from,
  consider the data contained in ``my_results``, 'hello world!'. To get at this
  data directly from the ``__call__(...)`` method, it looks something like::

	>>> my_statement().read()[0][0]

  While it's certainly easy to understand, it can be quite cumbersome and
  perhaps even error prone for more complicated queries returing single values.

  To simplify access to simple data, the ``first`` method will simply return
  the "first" of the result set.

  The first value: When there is a single row with a single column, ``first()``
  will return the contents of that cell.

  The first row: When there is a single row with multiple columns, ``first()``
  will return that row.

  The first column: When there is a single column with multiple rows,
  ``first()`` will return that column as a sequence.

  The first row count: When DML--for instance, an INSERT-statement--is executed,
  ``first()`` will return the row count returned by the statement as an integer.

  The result set created by the statement determines what is actually returned.
  Naturally, a statement used with ``first()`` should be crafted with these
  rules in mind.

Statement objects can take parameters. To do this, the statement must be defined using
PostgreSQL's positional parameter notation. ``$1``, ``$2``, ``$3``, etc. If the
statement object ``my_statement`` were to be re-written to take a parameter, it would be
done simply::

	>>> my_statement = db.prepare("SELECT $1")

And, re-create the ``my_cursor``::

	>>> my_cursor = my_statement('hello, world!')

It's that easy. And using ``first()``::

	>>> 'hello, world!' == my_statement.first('hello, world!')
	True

Inserting
---------

Copying
-------

Transacting
-----------

Setting
-------
"""

__docformat__ = 'reStructured Text'
if __name__ == '__main__':
	import sys
	if (sys.argv + [None])[1] == 'dump':
		sys.stdout.write(__doc__)
	else:
		try:
			help(__package__ + '.driver_basics')
		except NameError:
			help(__name__)
