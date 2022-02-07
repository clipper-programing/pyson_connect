##################################################
#Exception_Classes
##################################################
class ParseErrorException(Exception):
   def __str__(self):
        return "Specified resource, query string format is invalid"


class ValidationErrorException(Exception):
    def __str__(self):
        return "Specified resource, query string is invalid"


class InvalidResourceException(Exception):
    def __str__(self):
        return "Resource content is invalid"


class ClientAuthenticationErrorException(Exception):
    def __str__(self):
        return "Authentication failure"


class AccessTokenVerificationException(Exception):
    def __str__(self):
        return "Access token is invalid"


class ForbiddenErrorException(Exception):
    def __str__(self):
        return "Specified token is not authorized to access specified resource, Called API that is not authorized or Device ID is invalid"


class RateLimitExceededException(Exception):
    def __str__(self):
        return "Exceed maximum number of API calls"


class MethodNotArrowedException(Exception):
    def __str__(self):
        return "HTTP method is unsupported or invalid"


class UnsupportedMediaTypeException(Exception):
    def __str__(self):
        return "Content-Type is unsupported or invalid"


class InternalServerErrorException(Exception):
    def __str__(self):
        return "Unexpected error occurred"


class ServiceUnavailableException(Exception):
    def __str__(self):
        return "Service stopped"


class InvalidRequestException(Exception):
    def __str__(self):
        return "username, password foemat is invalid"


class InvalidGrantException(NameError):
    def __str__(self):
        return "printer email address is invalid"


class UnsupportedGrantTypeException(Exception):
    def __str__(self):
        return "grant type is invalid"


class InvalidClientException(Exception):
    def __str__(self):
        return "Authentication failed"


class UnexpectedErrorException(Exception):
    def __str__(self):
        return "Unexpected error"

class PrinterNotFoundErrorException(Exception):
    def __str__(self):
        return "subjectID is invalid or the device has been deleted from Epson Connect"


class UploadKeyErrorException(Exception):
    def __str__(self):
        return "The Key included in the upload URI is invalid"


class UploadCapacityErrorException(Exception):
    def __str__(self):
        return "Reached the upload capacity limit"


class InvalidFileErrorException(Exception):
    def __str__(self):
        return "The uploaded file is invalid"


class JobNotFoundException(Exception):
    def __str__(self):
        return "Print job ID is invalid"


class CommandNotAllowdException(Exception):
    def __str__(self):
        return "This API cannot call in current status"


class DuplicateAliasException(Exception):
    def __str__(self):
        return "Duplicated alias name"


class DestinationNotFoundErrorException(Exception):
    def __str__(self):
        return "Scan destination ID is invalid"


class MaximumNumberErrorException(Exception):
    def __str__(self):
        return "The maximum number of registrations has been exceeded"


##################################################
#Excveption_Classes
##################################################
class Errors:
    def errors(self, message=None, statusCode=None):
        if not statusCode:
            if message == "parse_error":
                raise ParseErrorException()

            elif message == "validation_error":
                raise ValidationErrorException()

            elif message == "invalid_resource":
                raise InvalidResourceException()

            elif message == "client_authentication_error":
                raise ClientAuthenticationErrorException()

            elif message == "access_token_verification_failed":
                raise AccessTokenVerificationException()

            elif message == "forbidden":
                raise ForbiddenErrorException()

            elif message == "rate_limit_exceeded":
                raise RateLimitExceededException()

            elif message == "method_not_allowed":
                raise MethodNotArrowedException()

            elif message == "unsupported_media_type":
                raise UnsupportedMediaTypeException()

            elif message == "internal_server_error":
                raise InternalServerErrorException()

            elif message == "service_unavailable":
                raise ServiceUnavailableException()

            elif message == "invalid_request":
                raise InvalidRequestException()

            elif message == "invalid_grant":
                raise InvalidGrantException()

            elif message == "unsupported_grant_type":
                raise UnsupportedGrantTypeException()

            elif message == "invalid_client":
                raise InvalidClientException()

            elif message == "printer_not_found":
                raise PrinterNotFoundErrorException()

            elif message == "job_not_found":
                raise JobNotFoundException()

            elif message == "command_not_allowed":
                raise CommandNotAllowdException()

            elif message == "Duplicated alias name":
                raise DuplicateAliasException()

            elif message == "destination_not_found":
                raise DestinationNotFoundErrorException()

            elif message == "maximum_number_error":
                raise MaximumNumberErrorException()

            else:
                raise UnexpectedErrorException()

        else:
            if statusCode == 404:
                raise UploadKeyErrorException()

            elif statusCode == 413:
                raise UploadCapacityErrorException()

            else:
                raise InvalidFileErrorException()
