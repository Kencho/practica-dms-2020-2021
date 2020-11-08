""" RestResponse class module.
"""


class RestResponse():
    """ Entity data-object class used to store the data of a response to a REST request.
    """

    def __init__(self, content: str = '', code: int = 200, mime_type: str = 'text/html'):
        """ Constructor method.

        Initializes a RestResponse instance with its immutable data.
        ---
        Parameters:
            - content: A string with the response content. Defaults to ''
            - code: An integer with the HTTP status code to use for the response.
                    Defaults to 200 (OK).
            - mime_type: The content type string. Defaults to 'text/html'
        """
        self.__content = content
        self.__code = code
        self.__mime_type = mime_type

    def get_content(self) -> str:
        """ Gets the response content.
        ---
        Returns:
            A string with the response content.
        """
        return self.__content

    def get_code(self) -> int:
        """ Gets the response HTTP status code.
        ---
        Returns:
            An integer with the response HTTP status code.
        """
        return self.__code

    def get_mime_type(self) -> str:
        """ Gets the response content type.
        ---
        Returns:
            A string with the response content/MIME type.
        """
        return self.__mime_type
