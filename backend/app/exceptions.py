from fastapi import HTTPException, status


class STException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidNameFormat(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный формат имени"


class ApplicationNotFound(STException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заявка не найдена"


class ApplicationDeleteError(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно удалить заявление"


class FileUploadError(STException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка загрузки файла"


class InvalidInputFormat(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный формат ввода"


class PasswordsNotMatch(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пароли не совпадают"


class WrongCurrentPassword(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Текущий пароль не верный"


class UserNotFound(STException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class StatementNotFound(STException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заявление не найдено"


class StatementAlreadyReviewed(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "На данное заявление уже составлено заключение"


class DocumentAlreadySigned(STException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Документ уже подписан"


class CommissionStatementNotFound(STException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Заявление комиссии не найдено"
