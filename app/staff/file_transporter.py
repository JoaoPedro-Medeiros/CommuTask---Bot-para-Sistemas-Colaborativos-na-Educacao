from os import remove

class FileTransporter :
    def __init__(self) -> None:
        self.__file = None
        self.__avaliator_id = None

    async def asyncInit(self, file, avaliator = None):
        file_extension = file.filename.split('.')[-1]
        file_content = await file.read()
        file_id = file.id
        filepath = f'app\\temp_files\\{file_id}.{file_extension}'
        with open(filepath, 'wb') as temp_file:
            temp_file.write(file_content)
        self.__file = filepath
        self.__avaliator_id = avaliator
    
    async def removeFile(self) -> None:
        remove(self.__file)
    
    def getFile(self):
        return self.__file
    
    def getAvaliatorId(self):
        return self.__avaliator_id
    
    def setAvaliatorId(self, id) -> None:
        self.__avaliator_id = id