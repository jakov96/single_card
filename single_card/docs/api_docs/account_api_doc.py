"""
@api {get} /api/v1/file-types/ Получение списка типов файлов
@apiName FileTypesList
@apiGroup FileManager
@apiVersion 1.0.0

@apiSuccessExample Пример ответа
[
    "ИНН",
    "Устав"
]

"""

"""
@api {get} /api/v1/organization-files/:id/ Получение списка файлов организации
@apiName OrganizationFilesList
@apiGroup FileManager
@apiVersion 1.0.0

@apiSuccessExample Пример ответа
[
    {
        "id": 1,
        "uuid": "259133c8-17c6-4e98-9704-8ae1dd9a6ea4",
        "name": "file1.png",
        "type_document": "Инн",
        "type_document_id": 1,
        "url": "http://account.mtt-holding.ru/1c-file/259133c8-17c6-4e98-9704-8ae1dd9a6ea4/file1.png"
    },
    {
        "id": 2,
        "uuid": "33191e61-977c-44ea-a5eb-6caeeff3e677",
        "name": "file2.png",
        "type_document": "Устав",
        "type_document_id": 2,
        "url": "http://account.mtt-holding.ru/1c-file/33191e61-977c-44ea-a5eb-6caeeff3e677/file2.png"
    }
]

@apiError detail Не найдено
@apiErrorExample Пример ошибки
{
    "detail": "Не найдено."
}

"""

"""
@api {post} /api/v1/upload-file/ Загрузка файла
@apiName UploadFile
@apiGroup FileManager
@apiVersion 1.0.0

@apiDescription Параметры передаются с помощью формы.

@apiParam {FileField} file Файл
@apiParam {Number} organization ID организации
@apiParam {String} type_document Тип документа

@apiSuccessExample Пример ответа
{
    "id": 1,
    "uuid": "5e5baab4-0a3c-4a67-9a67-2757b36bb691",
    "name": "file.png",
    "type_document": "ИНН",
    "type_document_id": 1,
    "url": "http://account.mtt-holding.ru/1c-file/5e5baab4-0a3c-4a67-9a67-2757b36bb691/file.png"
}

@apiError detail  Поле с информацией об ошибке
@apiErrorExample Пример ошибки
{
    "errors":{
    "organization": [
        "Не указан id организации"
    ]
},
    "detail": "Форма заполена не верно"
}

@apiError detail  Поле с информацией об ошибке
@apiErrorExample Пример ошибки
{
    "errors":[],
    "detail": "Файл с таким типом уже загружен. Сначала удалите его, затем загрузите заново."
}

"""

"""
@api {post} /api/v1/upload-avatar-file/ Загрузка файла аватара
@apiName UploadAvatarFile
@apiGroup FileManager
@apiVersion 1.0.0

@apiDescription Параметры передаются с помощью формы.

@apiParam {FileField} file Файл

@apiSuccessExample Пример ответа
{
    "id": 1,
    "url": "/media/avatars/avatar.png"
}

@apiError detail  Поле с информацией об ошибке
@apiErrorExample Пример ошибки
{
    "errors":{
    "file": [
        "Не был загружен файл"
    ]
},
    "detail": "Форма заполена неверно"
}

"""

"""
@api {get} /api/v1/avatar-file/:id/ Получение файла аватара
@apiName GetAvatarFile
@apiGroup FileManager
@apiVersion 1.0.0

@apiParam {Number} id ID файла

@apiSuccessExample Пример ответа
{
    "id": 1,
    "url": "/media/avatars/avatar.png"
}

@apiError detail  Поле с информацией об ошибке
@apiErrorExample Пример ошибки
{
    "detail": "Не найдено"
}

"""

"""
@api {delete} /api/v1/avatar-file/:id/ Удаление файла аватара
@apiName DeleteAvatarFile
@apiGroup FileManager
@apiVersion 1.0.0

@apiParam {Number} id ID файла

@apiSuccessExample Пример ответа
{
    "success": true
}

@apiError detail  Поле с информацией об ошибке
@apiErrorExample Пример ошибки
{
    "detail": "Не найдено"
}

"""
