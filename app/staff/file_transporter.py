from os import remove

class FileTransporter :
    def __init__(self) -> None:
        self.__file = None
        self.__avaliator_id = None

    async def async_init(self, file, avaliator = None):
        file_extension = file.filename.split('.')[-1]
        file_content = await file.read()
        file_id = file.id
        filepath = f'app\\temp_files\\{file_id}.{file_extension}'
        with open(filepath, 'wb') as temp_file:
            temp_file.write(file_content)
        self.__file = filepath
        self.__avaliator_id = avaliator
    
    async def remove_file(self) -> None:
        remove(self.__file)
    
    def get_file(self):
        return self.__file
    
    def get_avaliator_id(self):
        return self.__avaliator_id
    
    def set_avaliator_id(self, id) -> None:
        self.__avaliator_id = id