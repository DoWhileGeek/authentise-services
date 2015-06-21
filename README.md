# authentise-services
A python client for Authentise's open services.

[![Build Status](https://travis-ci.org/DoWhileGeek/authentise-services.svg?branch=master)](https://travis-ci.org/DoWhileGeek/authentise-services)

##Usage:
###User Creation:
```python
>>> from authentise_services.session import Session
>>> Session.create_user(username='my_user',
                        password='my_pass',
                        name='joe rod',
                        email='joe@domain.com')
```


###Model resource creation, upload, and download:
####Upload models on object creation:
```python
>>> from authentise_services.session import Session
>>> from authentise_services.model import Model
>>> session = Session('my_user', 'my_pass')
>>> model = Model(session, path='../stls/squirtle.stl')
>>> model.name
'squirtle.stl'
>>> model.model_uri
'http://models.authentise.com/model/some-uuid/'
>>> model.download_model('wartortle.stl')
```
####Upload models after object creation:
```python
>>> model2 = Model(session)
>>> model2.name
''
>>> model2.upload_model('../stls/charmander.stl')
>>> model2.name
'charmander.stl'
>>> model2.model_uri
'http://models.authentise.com/model/some-other-uuid/'
```
####Initialize objects with a model resource that already exists:
```python
>>> model3 = Model(session, uri='http://models.authentise.com/model/some-uuid/')
>>> model3.name
'squirtle.stl'
```
